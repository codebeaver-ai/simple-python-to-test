FROM python:3.12

COPY . .

ENTRYPOINT ["sh", "-c", "sleep 2 && exit 1"]