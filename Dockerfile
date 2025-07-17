FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Add wait-for-it script to wait for PostgreSQL to be ready
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh && \
    sed -i 's/\r$//' /wait-for-it.sh

# Command to run when container starts
CMD ["/bin/sh", "-c", "/wait-for-it.sh db:5432 -- python init_database.py && python -m src.app"]