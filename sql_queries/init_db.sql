CREATE DATABASE finance_dw;

\c finance_dw;

CREATE TYPE quarter_type AS ENUM ('Q1', 'Q2', 'Q3', 'Q4');

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    date TIMESTAMP NOT NULL,
    amount REAL,
    type VARCHAR(255),
    merchant_id INT
);

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    dob TIMESTAMP,
    country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_accounts (
    account_id INT PRIMARY KEY, 
    customer_id INT NOT NULL REFERENCES Customers(customer_id),
    account_type VARCHAR(255),
    balance REAL
);

CREATE TABLE IF NOT EXISTS dim_merchants (
    merchant_id INT PRIMARY KEY, 
    name VARCHAR(255),
    category VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_time (
    time_id SERIAL PRIMARY KEY,
    date_value TIMESTAMP UNIQUE,
    day INT,
    month INT,
    year INT,
    quarter quarter_type
);