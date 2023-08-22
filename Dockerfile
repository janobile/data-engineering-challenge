# Step 1: Use official lightweight Python image as base OS.
FROM python:3.9-slim

# Step 2. Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Step 3. Install production dependencies.
RUN pip install -r requirements.txt

# Step 4: Run the web service on container startup using unicorn webserver.
CMD exec uvicorn main:app --host 0.0.0.0 --port 8000
