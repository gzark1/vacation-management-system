FROM python:3.10.12

WORKDIR /app

# Set PYTHONPATH to allow absolute imports
ENV PYTHONPATH=/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run tests, but ensure the server starts even if tests fail
CMD (python -m unittest discover -s tests; python core/app.py)
