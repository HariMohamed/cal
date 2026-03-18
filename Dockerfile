FROM python:3.12-slim

WORKDIR /cal

RUN pip install flask

COPY Calculator.py app.py ./

CMD ["python", "app.py"]