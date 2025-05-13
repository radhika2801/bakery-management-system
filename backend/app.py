from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import redis
import os
import logging
import pika

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "bakery_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "yourpassword")
    )

# Redis setup
try:
    redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    redis_client.ping()
    redis_ready = True
except redis.exceptions.ConnectionError:
    redis_ready = False
    logger.warning("Redis is not ready yet.")

# RabbitMQ setup for publishing orders
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_URL", "rabbitmq")
    ))
    return connection.channel()

# Health check route
@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy"}), 500

# Products route - returns list of bakery products
@app.route("/products")
def get_products():
    try:
        if redis_ready:
            cached = redis_client.get("products")
            if cached:
                return jsonify(eval(cached.decode())), 200

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, image FROM products;")
        products = [
            {"id": row[0], "name": row[1], "price": float(row[2]), "image": row[3]}
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()

        if redis_ready:
            redis_client.set("products", str(products), ex=60)

        return jsonify(products), 200
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({"error": "Failed to fetch products"}), 500

# Place Order route - adds order to DB and sends it to RabbitMQ for worker processing
@app.route("/place_order", methods=["POST"])
def place_order():
    # Assuming you're receiving an order object with product ID and quantity
    order_data = request.get_json()  # e.g., {"product_id": 1, "quantity": 2}
    
    try:
        # Save order in DB as 'pending'
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (product_id, quantity, status)
            VALUES (%s, %s, 'pending')
            RETURNING id
        """, (order_data["product_id"], order_data["quantity"]))
        order_id = cursor.fetchone()[0]
        conn.commit()

        # Send the order to RabbitMQ
        channel = get_rabbitmq_channel()
        channel.basic_publish(
            exchange='',
            routing_key='order_queue',
            body=str({"id": order_id, "product_id": order_data["product_id"], "quantity": order_data["quantity"]})
        )
        return jsonify({"order_id": order_id, "status": "Order placed and being processed."}), 200
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return jsonify({"error": "Failed to place order"}), 500

# Check Order Status route
@app.route("/order_status", methods=["GET"])
def check_order_status():
    order_id = request.args.get("order_id")
    if not order_id:
        return jsonify({"error": "Order ID is required"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders WHERE id = %s;", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if order:
            return jsonify({"order_id": order_id, "status": order[0]}), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        logger.error(f"Error checking order status: {e}")
        return jsonify({"error": "Failed to check order status"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
