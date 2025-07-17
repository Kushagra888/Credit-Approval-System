from datetime import datetime
from src.database import db

class Customer:
    __tablename__ = 'customers'
    
    id = None
    first_name = None
    last_name = None
    age = None
    phone_number = None
    monthly_salary = None
    approved_limit = None
    loans = None
    
    def __repr__(self):
        return f"<Customer {self.id}: {self.first_name} {self.last_name}>"

class Loan:
    __tablename__ = 'loans'
    
    id = None
    customer_id = None
    loan_amount = None
    tenure = None
    interest_rate = None
    monthly_payment = None
    emis_paid_on_time = None
    date_of_approval = None
    end_date = None
    
    def __repr__(self):
        return f"<Loan {self.id}: Amount {self.loan_amount} for Customer {self.customer_id}>"

def setup_models(db_instance=None):
    
    class CustomerModel(db.Model):
        __tablename__ = 'customers'
        
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        age = db.Column(db.Integer, nullable=False)
        phone_number = db.Column(db.String(20), nullable=False)
        monthly_salary = db.Column(db.Float, nullable=False)
        approved_limit = db.Column(db.Float, nullable=False)
        
        loans = db.relationship('LoanModel', backref='customer', lazy=True)
        
        def __repr__(self):
            return f"<Customer {self.id}: {self.first_name} {self.last_name}>"
    
    class LoanModel(db.Model):
        __tablename__ = 'loans'
        
        id = db.Column(db.Integer, primary_key=True)
        customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
        loan_amount = db.Column(db.Float, nullable=False)
        tenure = db.Column(db.Integer, nullable=False)
        interest_rate = db.Column(db.Float, nullable=False)
        monthly_payment = db.Column(db.Float, nullable=False)
        emis_paid_on_time = db.Column(db.Integer, default=0)
        date_of_approval = db.Column(db.DateTime, default=datetime.utcnow)
        end_date = db.Column(db.DateTime, nullable=False)
        
        def __repr__(self):
            return f"<Loan {self.id}: Amount {self.loan_amount} for Customer {self.customer_id}>"
    
    global Customer, Loan
    Customer = CustomerModel
    Loan = LoanModel
    
    return CustomerModel, LoanModel