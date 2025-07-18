# Credit Approval System

A robust backend API system for credit approval and loan management. This system helps financial institutions evaluate customer creditworthiness and manage loan applications efficiently.

👉 [GitHub Repository](https://github.com/Kushagra888/Credit-Approval-System)

👉 [Click to watch demo video](https://drive.google.com/file/d/1265K_M07atwfeh9hqeZYwl5wTdiVXDQz/view?usp=sharing)


## Project Structure

The project follows a modular structure:

```
src/
├── api/            # API routes and controllers
├── models/         # Database models
├── services/       # Business logic services
├── utils/          # Utility functions
└── tests/          # Unit tests
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- PostgreSQL 13 or higher

### Installation

1. Clone the repository

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database:
   ```
   python init_postgres_db.py
   ```

4. Initialize the database with data:
   ```
   python init_database.py
   ```

5. Run the application:
   ```
   python -m src.app
   ```

6. The API will be available at `http://127.0.0.1:5000`

### Docker Setup

1. Build and run using Docker Compose:
   ```
   docker-compose up --build
   ```

## API Endpoints

### 1. Register Customer

- **URL**: `/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "age": 35,
    "monthly_income": 60000,
    "phone_number": "9876543211"
  }
  ```

### 2. Check Loan Eligibility

- **URL**: `/check-eligibility`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10.0,
    "tenure": 12
  }
  ```

### 3. Create Loan

- **URL**: `/create-loan`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10.0,
    "tenure": 12
  }
  ```

### 4. View Loan

- **URL**: `/view-loan/<loan_id>`
- **Method**: `GET`

### 5. View Customer Loans

- **URL**: `/view-loans/<customer_id>`
- **Method**: `GET`


## Features

- Customer registration with automatic credit limit calculation
- Credit score calculation based on multiple factors
- Loan eligibility assessment
- Loan creation and management
- Comprehensive loan viewing capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
