FROM python:3.10-slim-buster

RUN pip install -U pip 

WORKDIR /app

COPY [ "predict.py", "model/pipeline.bin", "requirements.txt", "./" ]

RUN pip install -r requirements.txt
EXPOSE 9696

ENTRYPOINT [ "waitress-serve", "--listen=0.0.0.0:9696", "predict:app" ]