USE retail_sales_db;
INSERT INTO customers (customer_id,full_name,email,city,region,signup_date) VALUES
(1,'Aarav Sharma','aarav@example.com','Hyderabad','South','2024-01-12'),
(2,'Diya Reddy','diya@example.com','Bengaluru','South','2024-02-20'),
(3,'Kabir Mehta','kabir@example.com','Mumbai','West','2024-03-03'),
(4,'Ananya Rao','ananya@example.com','Chennai','South','2024-03-18'),
(5,'Ishaan Das','ishaan@example.com','Kolkata','East','2024-04-05'),
(6,'Meera Patel','meera@example.com','Pune','West','2024-05-14'),
(7,'Rohan Kumar','rohan@example.com','Hyderabad','South','2024-06-01'),
(8,'Sara Khan','sara@example.com','Delhi','North','2024-06-21');

INSERT INTO stores (store_id,store_name,city,region) VALUES
(1,'Hyderabad Central','Hyderabad','South'),(2,'Bengaluru Market','Bengaluru','South'),
(3,'Mumbai West','Mumbai','West'),(4,'Delhi North','Delhi','North');

INSERT INTO products (product_id,product_name,category,unit_cost,list_price) VALUES
(1,'Wireless Mouse','Electronics',450,799),(2,'Mechanical Keyboard','Electronics',1800,2999),
(3,'Notebook Pack','Stationery',90,199),(4,'Office Chair','Furniture',3200,4999),
(5,'Water Bottle','Lifestyle',180,399),(6,'USB-C Hub','Electronics',950,1599),
(7,'Desk Lamp','Furniture',650,1199),(8,'Pen Set','Stationery',70,149);

INSERT INTO orders (order_id,customer_id,store_id,order_date,status) VALUES
(1,1,1,'2025-01-05','completed'),(2,2,2,'2025-01-12','completed'),
(3,3,3,'2025-02-03','completed'),(4,1,1,'2025-02-19','completed'),
(5,4,2,'2025-03-08','completed'),(6,5,4,'2025-03-15','completed'),
(7,6,3,'2025-04-02','completed'),(8,7,1,'2025-04-17','completed'),
(9,2,2,'2025-05-09','completed'),(10,8,4,'2025-05-21','completed'),
(11,3,3,'2025-06-04','completed'),(12,4,2,'2025-06-18','cancelled'),
(13,1,1,'2025-07-07','completed'),(14,6,3,'2025-07-22','completed'),
(15,7,1,'2025-08-11','completed'),(16,5,4,'2025-08-26','completed'),
(17,2,2,'2025-09-10','completed'),(18,8,4,'2025-09-28','completed'),
(19,3,3,'2025-10-06','completed'),(20,1,1,'2025-10-20','completed');

INSERT INTO order_items (order_id,product_id,quantity,unit_price,discount_pct) VALUES
(1,1,2,799,5),(1,3,3,199,0),(2,2,1,2999,10),(2,8,2,149,0),
(3,4,1,4999,5),(3,5,2,399,0),(4,6,1,1599,0),(4,1,1,799,10),
(5,3,5,199,0),(5,8,4,149,5),(6,7,2,1199,10),(6,5,3,399,0),
(7,2,1,2999,0),(7,6,2,1599,5),(8,4,1,4999,15),(8,3,2,199,0),
(9,1,3,799,5),(9,5,2,399,0),(10,6,1,1599,0),(10,8,6,149,0),
(11,4,1,4999,10),(11,7,1,1199,0),(12,2,1,2999,0),
(13,1,2,799,0),(13,6,1,1599,5),(14,5,4,399,10),(14,3,2,199,0),
(15,2,1,2999,5),(15,8,3,149,0),(16,7,2,1199,0),(16,5,1,399,0),
(17,6,2,1599,10),(17,1,1,799,0),(18,4,1,4999,5),(18,3,3,199,0),
(19,2,1,2999,0),(19,8,5,149,10),(20,1,2,799,5),(20,7,1,1199,0);

INSERT INTO payments (order_id,payment_date,amount,payment_method,payment_status) VALUES
(1,'2025-01-05',2450,'upi','paid'),(2,'2025-01-12',3296,'card','paid'),
(3,'2025-02-03',6000,'card','paid'),(4,'2025-02-19',2200,'upi','paid'),
(5,'2025-03-08',1500,'cash','paid'),(6,'2025-03-15',3500,'card','paid'),
(7,'2025-04-02',6000,'upi','paid'),(8,'2025-04-17',4500,'card','paid'),
(9,'2025-05-09',3500,'upi','paid'),(10,'2025-05-21',2500,'cash','paid'),
(11,'2025-06-04',5500,'card','paid'),(12,'2025-06-18',2999,'card','refunded'),
(13,'2025-07-07',3000,'upi','paid'),(14,'2025-07-22',1800,'cash','paid'),
(15,'2025-08-11',3200,'card','paid'),(16,'2025-08-26',2500,'upi','paid'),
(17,'2025-09-10',4000,'card','paid'),(18,'2025-09-28',5500,'upi','paid'),
(19,'2025-10-06',3500,'card','paid'),(20,'2025-10-20',3000,'upi','paid');
