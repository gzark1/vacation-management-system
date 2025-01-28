FROM python:3.10.12

WORKDIR /server

# Copy only necessary files first
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else (avoiding unnecessary files using .dockerignore)
COPY . .

# Set the command to run the backend
CMD ["python", "server.py"]
