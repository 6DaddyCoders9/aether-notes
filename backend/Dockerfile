# === Builder stage: Download the model ===
# Use a full Python image to handle the download, as 'slim' might lack build tools or full pip functionality
FROM python:3.11 as builder

# Set the cache directory for Hugging Face models *within this builder stage*
ENV HF_HOME="/cache/huggingface"
ENV EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2"

# Install only sentence-transformers here, to isolate its dependencies for model download
# We don't copy the full requirements.txt because we only need sentence-transformers for this step.
RUN pip install --no-cache-dir sentence-transformers

# Create the cache directory and force the model download into HF_HOME.
# This layer will only be rebuilt if EMBEDDING_MODEL_NAME or the sentence-transformers package change.
RUN mkdir -p ${HF_HOME}/hub && python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('${EMBEDDING_MODEL_NAME}')"

# === Production stage: Build the final application image ===
# Use a smaller base image for the final, slimmed-down application
FROM python:3.11-slim

# Set the working directory for the application
WORKDIR /app

# Copy and install all runtime Python dependencies.
# This layer caches if requirements.txt doesn't change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pre-downloaded model from the builder stage's cache.
# This copies the entire /cache/huggingface from the builder to /app/.cache/huggingface in the final image.
COPY --from=builder ${HF_HOME} ${WORKDIR}/.cache/huggingface

# Set the HF_HOME environment variable in the final image
# This tells sentence-transformers (and other Hugging Face libraries) where to find the model at runtime.
ENV HF_HOME="${WORKDIR}/.cache/huggingface"
ENV EMBEDDING_MODEL_NAME="all-MiniLM-L6-v2" 

# Copy the rest of your application code
# This is done last to leverage caching for previous layers during development.
COPY . .

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]