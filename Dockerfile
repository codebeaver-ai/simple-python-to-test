FROM python:3.12

COPY . .

CMD ["python", "-c", "raise Exception('Intentional crash for testing')"]