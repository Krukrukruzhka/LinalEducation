
FROM python:3.10-alpine

COPY requirements.txt .
RUN pip3 install --upgrade -r requirements.txt

WORKDIR /LinalEducation
COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV APPLICATION_ENV=DOCKER
ENV LOG_LEVEL=DEBUG
ENV PYTHONPATH="/LinalEducation"

CMD ["python3", "app/main.py"]
