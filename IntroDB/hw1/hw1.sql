-- Active: 1728012550964@@127.0.0.1@3306@hw1
CREATE TABLE customers(  
    customer_id varchar(50),
    customer_unique_id varchar(50),
    customer_zip_code_prefix int,
    customer_city varchar(50),
    customer_state varchar(50),
    PRIMARY KEY (customer_id)
);

CREATE TABLE geolocation(  
    geolocation_zip_code_prefix varchar(50),
    geolocation_lat float,
    geolocation_lng float,
    geolocation_city varchar(50),
    geolocation_state varchar(50),
    PRIMARY KEY (geolocation_lat, geolocation_lng)
);

load data local infile 'geolocation.csv'
into table geolocation
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

CREATE TABLE order_items(  
    order_id varchar(50),
    order_item_id int DEFAULT 0,
    product_id varchar(50),
    seller_id varchar(50),
    shipping_limit_date datetime,
    price float,
    freight_value float,
    PRIMARY KEY (order_id,order_item_id)
);

CREATE TABLE orders(  
    order_id varchar(50),
    customer_id varchar(50),
    order_status varchar(50),
    order_purchase_timestamp datetime,
    order_approved_at datetime,
    order_delivered_carrier_date datetime,
    order_delivered_customer_date datetime,
    order_delivered_delivery_date datetime,
    PRIMARY KEY (order_id)
);

CREATE TABLE payments(  
    order_id varchar(50),
    payment_sequential int DEFAULT 0,
    payment_type varchar(50),
    payment_installments int DEFAULT 0,
    payment_value float,
    PRIMARY KEY (order_id)
);

load data local infile 'payments.csv'
into table payments
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

CREATE TABLE products(  
    product_id varchar(50),
    product_category varchar(50),
    product_name_length int DEFAULT 0,
    product_decription_length int DEFAULT 0,
    product_photos_qty int DEFAULT 0,
    product_weight_g int DEFAULT 0,
    product_length_cm int DEFAULT 0,
    product_height_cm int DEFAULT 0,
    product_width_cm int DEFAULT 0,
    PRIMARY KEY (product_id)
);

CREATE TABLE sellers(  
    seller_id varchar(50),
    seller_zip_code_prefix int DEFAULT 0,
    seller_city varchar(50),
    seller_state varchar(50),
    PRIMARY KEY (seller_id)
);