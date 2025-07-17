from flask import request, jsonify
from src.models.models import Customer, Loan
from src.services.credit_service import calculate_credit_score, check_loan_eligibility, calculate_monthly_installment
from datetime import datetime, timedelta
from src.database import db

def register_routes(app):
    
    @app.route('/register', methods=['POST'])
    def register_customer():
        data = request.json
        
        required_fields = ['first_name', 'last_name', 'age', 'monthly_income', 'phone_number']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        try:
            monthly_salary = data['monthly_income']
            approved_limit = round(monthly_salary * 36 / 100000) * 100000
            
            customer = Customer(
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                phone_number=str(data['phone_number']),
                monthly_salary=float(monthly_salary),
                approved_limit=float(approved_limit)
            )
            
            db.session.add(customer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
        return jsonify({
            'customer_id': customer.id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': customer.age,
            'monthly_income': customer.monthly_salary,
            'approved_limit': customer.approved_limit,
            'phone_number': customer.phone_number
        }), 201
    
    @app.route('/check-eligibility', methods=['POST'])
    def check_eligibility():
        data = request.json
        
        required_fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        credit_score = calculate_credit_score(customer.id)
        
        approval, corrected_interest_rate = check_loan_eligibility(
            customer.id, 
            data['loan_amount'], 
            data['interest_rate'], 
            data['tenure'], 
            credit_score
        )
        
        monthly_installment = calculate_monthly_installment(
            data['loan_amount'], 
            corrected_interest_rate, 
            data['tenure']
        )
        
        return jsonify({
            'customer_id': customer.id,
            'approval': approval,
            'interest_rate': corrected_interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': data['tenure'],
            'monthly_installment': monthly_installment
        }), 200
    
    @app.route('/create-loan', methods=['POST'])
    def create_loan():
        data = request.json
        
        required_fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        credit_score = calculate_credit_score(customer.id)
        
        approval, corrected_interest_rate = check_loan_eligibility(
            customer.id, 
            data['loan_amount'], 
            data['interest_rate'], 
            data['tenure'], 
            credit_score
        )
        
        if not approval:
            return jsonify({
                'loan_id': None,
                'customer_id': customer.id,
                'loan_approved': False,
                'message': 'Loan not approved based on eligibility criteria',
                'monthly_installment': 0
            }), 200
        
        monthly_installment = calculate_monthly_installment(
            data['loan_amount'], 
            corrected_interest_rate, 
            data['tenure']
        )
        
        end_date = datetime.utcnow() + timedelta(days=30 * data['tenure'])
        loan = Loan(
            customer_id=customer.id,
            loan_amount=data['loan_amount'],
            tenure=data['tenure'],
            interest_rate=corrected_interest_rate,
            monthly_payment=monthly_installment,
            date_of_approval=datetime.utcnow(),
            end_date=end_date
        )
        
        db.session.add(loan)
        db.session.commit()
        
        return jsonify({
            'loan_id': loan.id,
            'customer_id': customer.id,
            'loan_approved': True,
            'message': 'Loan approved',
            'monthly_installment': monthly_installment
        }), 201
    
    @app.route('/view-loan/<int:loan_id>', methods=['GET'])
    def view_loan(loan_id):
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        customer = Customer.query.get(loan.customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        return jsonify({
            'loan_id': loan.id,
            'customer': {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone_number': customer.phone_number,
                'age': customer.age
            },
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_payment,
            'tenure': loan.tenure
        }), 200
    
    @app.route('/view-loans/<int:customer_id>', methods=['GET'])
    def view_customer_loans(customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        loans = Loan.query.filter_by(customer_id=customer_id).all()
        
        loan_list = []
        for loan in loans:
            total_emis = loan.tenure
            paid_emis = loan.emis_paid_on_time
            repayments_left = total_emis - paid_emis
            
            loan_list.append({
                'loan_id': loan.id,
                'loan_amount': loan.loan_amount,
                'interest_rate': loan.interest_rate,
                'monthly_installment': loan.monthly_payment,
                'repayments_left': repayments_left
            })
        
        return jsonify(loan_list), 200
