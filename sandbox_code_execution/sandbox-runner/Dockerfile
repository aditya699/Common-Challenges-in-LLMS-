# ✅ Step 1: Use a clean Python base image
FROM python:3.11-slim

# ✅ Step 2: Install pandas
RUN pip install --no-cache-dir pandas matplotlib numpy seaborn

# ✅ Step 3: Set working directory inside the container
WORKDIR /app

# ✅ Step 4: This is what will run when container starts
CMD ["python", "code.py"]
