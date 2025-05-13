import os
import redis
import psycopg2
import pika
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis and DB connection setup
r = redis.Redis.from_url(os.getenv("REDIS_URL"))
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
channel = None

# Setup RabbitMQ connection
def setup_rabbitmq():
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_URL", "rabbitmq")
    ))
    channel = connection.channel()
    channel.queue_declare(queue="order_queue")

# Dummy task for illustration - to be processed by worker
def process_order(ch, method, properties, body):
    try:
        order_data = body.decode("utf-8")
        logger.info(f"Processing order: {order_data}")

        # Here you'd add logic to update the DB based on the order received
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (product_id, quantity)
            VALUES (%s, %s)
        """, (order_data["product_id"], order_data["quantity"]))
        conn.commit()
        logger.info(f"Order {order_data['id']} has been processed.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing order: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Start the worker and listen for new orders
def start_worker():
    setup_rabbitmq()
    logger.info("Worker started and connected to DB and Redis.")
    channel.basic_consume(queue="order_queue", on_message_callback=process_order)
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
