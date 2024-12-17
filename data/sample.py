import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Constants
NUM_CUSTOMERS = 100
NUM_ACCOUNTS = 150
NUM_MERCHANTS = 50
NUM_TRANSACTIONS = 1000

# Generate Customers
def generate_customers(num_customers):
    customers = []
    for _ in range(num_customers):
        customer_id = fake.uuid4()[:8]
        name = fake.name()
        email = fake.email()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        country = fake.country()
        customers.append([customer_id, name, email, dob, country])
    return pd.DataFrame(customers, columns=["customer_id", "name", "email", "dob", "country"])

# Generate Accounts
def generate_accounts(customers, num_accounts):
    accounts = []
    for _ in range(num_accounts):
        account_id = fake.uuid4()[:8]
        customer_id = random.choice(customers["customer_id"])
        account_type = random.choice(["Savings", "Checking", "Credit"])
        balance = round(random.uniform(100, 10000), 2)
        accounts.append([account_id, customer_id, account_type, balance])
    return pd.DataFrame(accounts, columns=["account_id", "customer_id", "account_type", "balance"])

# Generate Merchants
def generate_merchants(num_merchants):
    merchants = []
    for _ in range(num_merchants):
        merchant_id = fake.uuid4()[:8]
        name = fake.company()
        category = random.choice(["Retail", "Food", "Entertainment", "Travel", "Electronics"])
        location = fake.city()
        merchants.append([merchant_id, name, category, location])
    return pd.DataFrame(merchants, columns=["merchant_id", "name", "category", "location"])

# Generate Transactions
def generate_transactions(accounts, merchants, num_transactions):
    transactions = []
    for _ in range(num_transactions):
        transaction_id = fake.uuid4()[:8]
        account_id = random.choice(accounts["account_id"])
        date = fake.date_time_between(start_date="-2y", end_date="now")
        amount = round(random.uniform(5, 500), 2)
        transaction_type = random.choice(["Debit", "Credit"])
        merchant_id = random.choice(merchants["merchant_id"])
        transactions.append([transaction_id, account_id, date, amount, transaction_type, merchant_id])
    return pd.DataFrame(transactions, columns=["transaction_id", "account_id", "date", "amount", "type", "merchant_id"])

# Generate Time Dimension
def generate_time_dimension(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date)
    time_data = []
    for date in dates:
        day = date.day
        month = date.month
        year = date.year
        quarter = (month - 1) // 3 + 1
        time_data.append([date, day, month, year, f"Q{quarter}"])
    return pd.DataFrame(time_data, columns=["date", "day", "month", "year", "quarter"])

# Generate Data
customers = generate_customers(NUM_CUSTOMERS)
accounts = generate_accounts(customers, NUM_ACCOUNTS)
merchants = generate_merchants(NUM_MERCHANTS)
transactions = generate_transactions(accounts, merchants, NUM_TRANSACTIONS)
time_dimension = generate_time_dimension("2022-01-01", "2024-12-31")

# Save to CSV
customers.to_csv("raw/customers.csv", index=False)
accounts.to_csv("raw/accounts.csv", index=False)
merchants.to_csv("raw/merchants.csv", index=False)
transactions.to_csv("raw/transactions.csv", index=False)
time_dimension.to_csv("raw/time.csv", index=False)

print("Synthetic data generated and saved to 'data/' directory.")
