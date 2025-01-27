FROM node:22.13.1-slim

COPY . .

CMD ["jest"]