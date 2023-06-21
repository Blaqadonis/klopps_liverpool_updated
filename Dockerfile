FROM python:3.10-slim

RUN pip install -U pip 

WORKDIR /app

COPY [ "predict.py", "tree.bin", "vectorizer.bin", "requirements.txt", "./" ]

RUN pip install -r requirements.txt
EXPOSE 9696

ENTRYPOINT [ "waitress-serve", "--listen=0.0.0.0:9696", "predict:app" ]