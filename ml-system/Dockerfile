FROM python:3.9.12
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r ./requirements.txt

COPY app.py /app
COPY model.py /app
COPY preprocessor.py /app
COPY trans_2_5.h5 /app
COPY .flaskenv /app
COPY .env /app

CMD ["python", "app.py"]