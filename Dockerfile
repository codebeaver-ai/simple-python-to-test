FROM python:3.12

COPY . .

ENTRYPOINT ["sh", "-c", "sleep 2 && echo 'i am a nasty error' && exit 1"]