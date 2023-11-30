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
COPY model_xgb_reg_v_1.json /app
COPY random_forest_regressor.ml /app
COPY model_md_fnn_v2_2.h5 /app
COPY dataset_config.json /app
COPY model_md_fnn_v3_0.h5 /app

EXPOSE 5571

CMD ["python", "app.py"]