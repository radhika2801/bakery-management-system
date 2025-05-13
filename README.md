	System Architecture Overview:
•	The system consists of multiple services working together to provide a bakery management system. 
•	The architecture follows a microservices approach, utilizing Docker containers to separate concerns. 
•	The services are connected via Docker networking.

Components:
	PostgreSQL Database: 
•	A containerized PostgreSQL instance stores product data, including product names, prices, and images.

	Backend API: 
•	A Flask-based API handles the business logic, exposing endpoints to list products, place orders, and check order statuses.

	Frontend: 
•	A web application built with HTML, CSS, and JavaScript, connecting to the backend to display products and manage the shopping cart.

	Redis: 
•	Caching is implemented with Redis to improve performance, especially for fetching product data.

	RabbitMQ: 
•	A message queue for handling background processing of orders (e.g., order processing, notifications).

	Worker Service: 
•	A background worker service processes orders from the RabbitMQ queue.

•	Docker Compose manages all containers and ensures that they can communicate with each other seamlessly. 
•	Services such as the database, backend, frontend, and worker are all containerized and defined in the docker-compose.yml file.

	Setup Instructions
•	To set up the bakery system, follow these steps:

1)	Clone the Repository:
git clone <repository_url>
cd bakery-management-system

2)	Ensure Docker is Installed:
You need Docker and Docker Compose installed on your machine. 

3)	Set Up the Environment:
Make sure you have the .env file with the required environment variables:
DB_HOST=db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_NAME=bakery_db
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

4)	Build and Start Containers:
 	Run the following command to build and start all containers:
docker-compose up –build

5)	 Access the Application:
Frontend: Open http://localhost:3000 in your browser to view the application.
Backend API: The backend API will be available at:
GET /products: http://localhost:5000/products - Fetches a list of all bakery products available for sale.
POST /orders: http://localhost:5000/orders - Places an order by accepting product IDs and quantities.
GET /order-status/{order_id}: http://localhost:5000/order-status/{order_id} - Checks the status of an order.
GET /health: http://localhost:5000/health - Checks the health of the backend services (database, Redis, etc.).

6)	Shutdown the Application:
To stop the containers, run:
docker-compose down

7)	API Documentation
GET /products
Fetches a list of all bakery products available for sale.
URL: http://localhost:5000/products
Response: Returns a JSON array of products.
[
  {
    "id": 1,
    "name": "Cupcake",
    "price": 2.99,
    "image": "cupcake.jpg"
  },
  ...
]

8)	POST /orders
Places an order by accepting product IDs and quantities.
URL: http://localhost:5000/orders
Request Body:
{
  "items": [
    {"id": 1, "quantity": 2},
    {"id": 2, "quantity": 1}
  ]
}


9)	Response: Returns the order ID.
{
  "order_id": "abc123"
}

10)	GET /order-status/{order_id}
Checks the status of an order.
URL: http://localhost:5000/order-status/{order_id}
Response: Returns the current status of the order.
{
  "order_id": "abc123",
  "status": "Processing"
}

11)	GET /health
Checks the health of the backend services (database, Redis, etc.).
URL: http://localhost:5000/health
Response: Returns a JSON response indicating the health status.
{
  "status": "healthy"
}



	Brief Report on Design Decisions
	Design Approach

•	The architecture of this bakery management system follows a microservices model, where each service is responsible for a specific concern, and these services communicate with each other using APIs and messaging systems. This modular approach offers flexibility in scaling and maintaining the application in the future.
•	Frontend: The frontend is built with standard web technologies (HTML, CSS, JavaScript) to keep the user interface simple and responsive. It communicates with the backend API to fetch products and manage the cart.
•	Backend: A Flask-based backend is used due to its simplicity and flexibility. The backend exposes APIs to interact with the frontend, handles orders, and interacts with the PostgreSQL database and Redis for caching. Flask is a lightweight framework, which is ideal for our microservice architecture.
•	Database: PostgreSQL is used as the relational database management system to store product and order data. It provides consistency, scalability, and is a reliable choice for our application's data needs.
•	Redis: Redis is integrated to cache product data, reducing database load and improving response times. Caching helps ensure the frontend displays data quickly and efficiently.
•	RabbitMQ: RabbitMQ is chosen for message queuing to decouple services. The worker service processes orders asynchronously, ensuring the application can handle high traffic and provide real-time updates without blocking the main application.
•	Worker: The worker service listens to RabbitMQ queues and processes orders in the background, which helps avoid overloading the main API and keeps the system responsive.
•	Containerization: Docker is used for containerizing all components (backend, frontend, database, Redis, RabbitMQ, and worker). Docker allows easy deployment, scaling, and consistent environments across different stages of development and production. Docker Compose is used for orchestrating the services and ensuring they can communicate with each other.

	Why These Choices Were Made

•	Flask: Chosen for its lightweight and fast development capabilities.
•	PostgreSQL: A robust relational database for structured data.
•	Redis: Provides fast caching for frequently requested data, reducing database load.
•	RabbitMQ: Enables decoupling of services, allowing for efficient background processing.
•	Docker: Ensures consistency between development, staging, and production environments, making deployment simpler.


