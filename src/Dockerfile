# Stage 1: Build stage
FROM python:3.12-alpine as builder

# set working directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


# Stage 2: Final stage
FROM python:3.12-alpine

# set working directory
# WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the installed dependencies from the previous stage
COPY --from=builder /usr/local /usr/local
ENV PATH=/usr/local/bin:$PATH

WORKDIR /usr/src

# Copy your app code
COPY ./app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
