from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    return jsonify({'data: ': data}), 200

if __name__ == '__main__':
    app.run(port=5000)