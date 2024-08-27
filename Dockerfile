## Chainguard Python Dockerfile 
## Doc link: https://images.chainguard.dev/directory/image/python/overview
FROM cgr.dev/chainguard/python:latest-dev AS build-env

USER root
RUN apk update && apk add openssl

USER nonroot
WORKDIR /app
RUN python -m venv venv
ENV PATH="/app/venv/bin":$PATH
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Generate self-signed certificates
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=VA/L=Ashburn/O=Bmo/OU=BmoOU/CN=localhost"

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY main.py .
COPY --from=build-env /app/venv /app/venv
COPY --from=build-env /app/key.pem /app/key.pem
COPY --from=build-env /app/cert.pem /app/cert.pem

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 5002

# Use Uvicorn to run the FastAPI app with HTTPS
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002", "--reload", "--ssl-keyfile", "./key.pem", "--ssl-certfile", "./cert.pem"]
