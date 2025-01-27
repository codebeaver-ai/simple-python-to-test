FROM node:22.13.1-slim

COPY . .

CMD ["python -c 'raise Exception('Intentional crash for testing')'"]