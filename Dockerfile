FROM python:3.12

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-c", "raise Exception('Intentional crash for testing')"]