FROM python:3.8-alpine
LABEL authors="Fred Assi"
LABEL maintainer="trainingfred2023@gmail.com"
WORKDIR /app
COPY rest_app.py /app
COPY config.py /app
COPY db_connector.py /app
COPY requirements.txt /app
RUN apk --no-cache add curl
RUN apk update && apk upgrade
RUN pip install --user -r /app/requirements.txt
EXPOSE 5003
VOLUME /app/logs
CMD ["python3", "rest_app.py"]