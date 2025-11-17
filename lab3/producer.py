from kafka import KafkaProducer
from flask import Flask, request
import json
import csv

app = Flask(__name__)

# Настройки подключения к Kafka
KAFKA_SERVER = "localhost:9092"  # Заменить на данные препода
TOPIC_NAME = "etl_topic"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@app.route('/')
def index():
    return """
    <h3>ETL Producer</h3>
    <form method="post" action="/send">
        Table: <input type="text" name="table" required><br>
        Columns: <input type="text" name="columns" required><br>
        Data: <textarea name="data" required></textarea><br>
        <button>Send to Kafka</button>
    </form>
    <hr>
    <form method="post" action="/upload" enctype="multipart/form-data">
        Table: <input type="text" name="table" required><br>
        File: <input type="file" name="file" required><br>
        <button>Upload CSV/JSON</button>
    </form>
    """


@app.route('/send', methods=['POST'])
def send():
    try:
        table = request.form['table']
        columns = request.form['columns'].split(',')
        data = [row.split(',') for row in request.form['data'].split('\n') if row.strip()]

        message = {
            "table_name": table,
            "columns": columns,
            "data": data
        }

        producer.send(TOPIC_NAME, message)
        return "Data sent to Kafka"
    except:
        return "Error"


@app.route('/upload', methods=['POST'])
def upload():
    try:
        table = request.form['table']
        file = request.files['file']

        if file.filename.endswith('.csv'):
            data = file.read().decode('utf-8').splitlines()
            reader = csv.reader(data)
            rows = list(reader)
            columns = rows[0]
            data_rows = rows[1:]
        else:  # json
            data = json.loads(file.read())
            columns = list(data[0].keys())
            data_rows = [list(item.values()) for item in data]

        message = {
            "table_name": table,
            "columns": columns,
            "data": data_rows
        }

        producer.send(TOPIC_NAME, message)
        return "File data sent to Kafka"
    except:
        return "Error"


if __name__ == '__main__':
    app.run(debug=True)