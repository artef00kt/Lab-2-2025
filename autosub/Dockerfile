FROM python:3.10-slim

WORKDIR /app

# Install git and ffmpeg (system package)
RUN apt-get update && apt-get install -y git ffmpeg && rm -rf /var/lib/apt/lists/*

# Install dependencies
# We need 'ffmpeg-python' wrapper for auto-subtitle, NOT just 'ffmpeg' system package
RUN pip install --no-cache-dir fastapi uvicorn ffmpeg-python git+https://github.com/m1guelpf/auto-subtitle.git

# Install torch CPU version explicitely to speed up build
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy app code
COPY app.py .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
