# 1. Start with an official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variable for the model name
ENV EMBEDDING_MODEL_NAME "all-MiniLM-L6-v2"
# Create a directory for HuggingFace models
RUN mkdir -p /root/.cache/huggingface/hub
# Use Python to programmatically download the model.
# This prevents the need to run the script in container for first time.
# It will be cached inside the image.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('${EMBEDDING_MODEL_NAME}')"
# --------------------------------------------------------

# Copy the rest of your application code
COPY . /app

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application code into the container
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]