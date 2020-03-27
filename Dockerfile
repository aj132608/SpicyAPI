FROM python:3.7.6-stretch

# Set /app as the Current Working Directory
WORKDIR /app

# Copy the contents into the container
COPY . .

# Dynamically set the port for the Flask app
ARG PORT
ENV PORT $PORT
ENV HOST 0.0.0.0
ENV GOOGLE_APPLICATION_CREDENTIALS creds/pub-sub132608-fe8b88422b10.json
ENV PROJECT pub-sub132608

RUN pip install -r requirements.txt

# Run the API
ENTRYPOINT ["python3"]
CMD ["spicy_api.py"]