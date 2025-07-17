from src.models.models import Customer, Loan
from sqlalchemy import func
import math

def calculate_credit_score(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return 0
    
    loans = Loan.query.filter_by(customer_id=customer_id).all()
    
    if not loans:
        limit_score = min(40, customer.approved_limit / 250000)
        age_score = min(30, customer.age / 2)
        income_score = min(30, customer.monthly_salary / 100000 * 30)
        
        return limit_score + age_score + income_score
    
    total_emis = sum(loan.tenure for loan in loans)
    emis_paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    
    if total_emis > 0:
        payment_history_score = min(30, (emis_paid_on_time / total_emis) * 30)
    else:
        payment_history_score = 0
    
    completed_loans = sum(1 for loan in loans if loan.emis_paid_on_time >= loan.tenure)
    loan_activity_score = min(20, completed_loans * 5)
    
    current_loans = [loan for loan in loans if loan.emis_paid_on_time < loan.tenure]
    if current_loans:
        current_loan_amount = sum(loan.loan_amount for loan in current_loans)
        loan_to_income_ratio = current_loan_amount / (customer.monthly_salary * 12)
        
        # Lower ratio is better (0.5 or less is ideal)
        if loan_to_income_ratio <= 0.5:
            loan_to_income_score = 20
        elif loan_to_income_ratio <= 1:
            loan_to_income_score = 15
        elif loan_to_income_ratio <= 2:
            loan_to_income_score = 10
        else:
            loan_to_income_score = 5
    else:
        loan_to_income_score = 20  # No current loans is good
    
    # 4. Credit utilization (15 points)
    # Lower utilization is better
    if current_loans:
        current_loan_amount = sum(loan.loan_amount for loan in current_loans)
        credit_utilization = current_loan_amount / customer.approved_limit
        
        if credit_utilization <= 0.3:
            credit_utilization_score = 15
        elif credit_utilization <= 0.5:
            credit_utilization_score = 10
        elif credit_utilization <= 0.7:
            credit_utilization_score = 5
        else:
            credit_utilization_score = 0
    else:
        credit_utilization_score = 15
    
    age_score = min(15, customer.age / 4)
    
    credit_score = (
        payment_history_score + 
        loan_activity_score + 
        loan_to_income_score + 
        credit_utilization_score + 
        age_score
    )
    
    return credit_score

def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure, credit_score=None):
    customer = Customer.query.get(customer_id)
    if not customer:
        return False, interest_rate
    
    if credit_score is None:
        credit_score = calculate_credit_score(customer_id)
    
    current_loans = Loan.query.filter_by(customer_id=customer_id).all()
    current_loan_amount = sum(loan.loan_amount for loan in current_loans if loan.emis_paid_on_time < loan.tenure)
    
    if current_loan_amount + loan_amount > customer.approved_limit:
        return False, interest_rate
    
    # Determine approval based on credit score
    if credit_score >= 50:  # Good credit score
        approval = True
    elif credit_score >= 30:  # Moderate credit score
        # Approve if loan amount is not too high
        approval = loan_amount <= customer.approved_limit * 0.5
    else:  # Poor credit score
        # Approve only small loans
        approval = loan_amount <= customer.approved_limit * 0.2
    
    corrected_interest_rate = interest_rate
    
    if credit_score >= 80:
        corrected_interest_rate = max(interest_rate - 2, 0)
    elif credit_score >= 60:
        corrected_interest_rate = max(interest_rate - 1, 0)
    elif credit_score >= 40:
        corrected_interest_rate = interest_rate
    elif credit_score >= 20:
        corrected_interest_rate = interest_rate + 1
    else:
        corrected_interest_rate = interest_rate + 2
    
    return approval, corrected_interest_rate

def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    monthly_interest_rate = interest_rate / (12 * 100)
    
    if monthly_interest_rate > 0:
        emi = loan_amount * monthly_interest_rate * math.pow(1 + monthly_interest_rate, tenure) / (math.pow(1 + monthly_interest_rate, tenure) - 1)
    else:
        emi = loan_amount / tenure
    
    return round(emi, 2)
