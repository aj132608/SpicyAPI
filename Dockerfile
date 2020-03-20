FROM python:3.7.6-stretch

# Set /app as the Current Working Directory
WORKDIR /app

# Dynamically set the port for the Flask app
ARG PORT
ENV PORT $PORT
ENV HOST 0.0.0.0

# Copy the contents into the container
COPY . .

RUN pip install -r requirements.txt

# Run the API
ENTRYPOINT ["python3"]
CMD ["spicy_api.py"]