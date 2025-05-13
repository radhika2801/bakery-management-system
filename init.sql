CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(6,2) NOT NULL,
    image TEXT NOT NULL
);

INSERT INTO products (name, price, image) VALUES
('Cupcake', 2.99, 'cupcake.jpg'),
('Donut', 1.99, 'donut.jpg'),
('Cookie', 1.49, 'cookie.jpg'),
('Brownie', 2.49, 'brownie.jpg'),
('Croissant', 2.79, 'croissant.jpg'),
('Muffin', 2.29, 'muffin.jpg'),
('Cake', 15.00, 'cake.jpg');

-- Table to store orders that will be processed by the worker
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
