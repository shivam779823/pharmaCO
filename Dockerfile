FROM python:3.9-alpine
LABEL maintainer="shivam"
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PORT=8080
# Define environment variables for MySQL connection
# ENV MYSQL_HOST=your-mysql-host
# ENV MYSQL_USER=your-mysql-username
# ENV MYSQL_PASSWORD=your-mysql-password
# ENV MYSQL_DB=your-mysql-database
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app


