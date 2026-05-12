from faker import Faker
import csv
import random
import uuid
import os

# Initialize Faker
fake = Faker()

# Set seed for reproducible data
Faker.seed(42)
random.seed(42)

# Number of mock transactions
NUM_TRANSACTIONS = 100000

# Output folder and file path
OUTPUT_FOLDER = "data"
OUTPUT_FILE = "mock_credit_card_transactions.csv"
OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

# Merchant categories
merchant_categories = [
    "Groceries",
    "Restaurants",
    "Gas",
    "Travel",
    "Online Shopping",
    "Entertainment",
    "Healthcare",
    "Utilities",
    "Education",
    "Electronics",
    "Clothing",
    "Insurance",
    "Subscription",
    "Hotel",
    "Pharmacy"
]

# Currencies
currencies = ["USD", "EUR", "GBP", "INR", "CAD"]

# Create data folder if it does not exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Generate CSV file
with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow([
        "transaction_id",
        "user_id",
        "timestamp",
        "merchant_category",
        "amount",
        "currency"
    ])

    # Generate transaction rows
    for _ in range(NUM_TRANSACTIONS):
        transaction_id = str(uuid.uuid4())
        user_id = f"USER_{fake.random_int(min=1000, max=9999)}"
        timestamp = fake.date_time_between(start_date="-1y", end_date="now")
        merchant_category = random.choice(merchant_categories)
        amount = round(random.uniform(1.00, 5000.00), 2)
        currency = random.choice(currencies)

        writer.writerow([
            transaction_id,
            user_id,
            timestamp,
            merchant_category,
            amount,
            currency
        ])

print(f"CSV file created successfully: {OUTPUT_PATH}")
print(f"Total transactions generated: {NUM_TRANSACTIONS}")
