CREATE DATABASE IF NOT EXISTS retail_sales_db;
USE retail_sales_db;

CREATE TABLE IF NOT EXISTS customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE,
  city VARCHAR(80),
  region VARCHAR(80),
  signup_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS stores (
  store_id INT PRIMARY KEY AUTO_INCREMENT,
  store_name VARCHAR(100) NOT NULL,
  city VARCHAR(80) NOT NULL,
  region VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  product_id INT PRIMARY KEY AUTO_INCREMENT,
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(80) NOT NULL,
  unit_cost DECIMAL(10,2) NOT NULL,
  list_price DECIMAL(10,2) NOT NULL,
  CHECK (unit_cost >= 0), CHECK (list_price >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  store_id INT NOT NULL,
  order_date DATE NOT NULL,
  status ENUM('completed','cancelled','returned') NOT NULL DEFAULT 'completed',
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (store_id) REFERENCES stores(store_id),
  INDEX idx_orders_date_status (order_date, status),
  INDEX idx_orders_customer (customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
  order_item_id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  discount_pct DECIMAL(5,2) NOT NULL DEFAULT 0,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  CHECK (quantity > 0), CHECK (unit_price >= 0),
  CHECK (discount_pct >= 0 AND discount_pct <= 100),
  INDEX idx_items_product (product_id)
);

CREATE TABLE IF NOT EXISTS payments (
  payment_id INT PRIMARY KEY AUTO_INCREMENT,
  order_id INT NOT NULL,
  payment_date DATE NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  payment_method ENUM('card','cash','upi','net_banking') NOT NULL,
  payment_status ENUM('paid','pending','refunded') NOT NULL DEFAULT 'paid',
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  INDEX idx_payments_order (order_id)
);
