import pandas as pd
from src.models.models import Customer, Loan
from src.database import db
from src.app import app
from datetime import datetime

def load_customer_data(file_path='customer_data.xlsx'):
    df = pd.read_excel(file_path)
    
    for _, row in df.iterrows():
        customer = Customer(
            id=row['Customer ID'],
            first_name=row['First Name'],
            last_name=row['Last Name'],
            age=row['Age'],
            phone_number=str(row['Phone Number']),
            monthly_salary=float(row['Monthly Salary']),
            approved_limit=float(row['Approved Limit'])
        )
        
        db.session.merge(customer)
    
    db.session.commit()
    print(f"Loaded {len(df)} customers into the database")

def load_loan_data(file_path='loan_data.xlsx'):
    df = pd.read_excel(file_path)
    
    for _, row in df.iterrows():
        loan = Loan(
            id=row['Loan ID'],
            customer_id=row['Customer ID'],
            loan_amount=float(row['Loan Amount']),
            tenure=int(row['Tenure']),
            interest_rate=float(row['Interest Rate']),
            monthly_payment=float(row['Monthly payment']),
            emis_paid_on_time=int(row['EMIs paid on Time']),
            date_of_approval=row['Date of Approval'],
            end_date=row['End Date']
        )
        
        db.session.merge(loan)
    
    db.session.commit()
    print(f"Loaded {len(df)} loans into the database")

def init_db():
    with app.app_context():
        db.create_all()
        
        load_customer_data()
        load_loan_data()
        
        from sqlalchemy import text
        db.session.execute(text("SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));"))
        db.session.execute(text("SELECT setval('loans_id_seq', (SELECT MAX(id) FROM loans));"))
        db.session.commit()
        
        print("Database initialized successfully")

if __name__ == '__main__':
    init_db()
