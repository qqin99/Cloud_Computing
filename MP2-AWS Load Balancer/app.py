from flask import Flask, request

app = Flask(__name__)

# default seed is 0
seed = 0


@app.route('/', methods=['POST', 'GET'])
def login():
    global seed
    if request.method == 'POST':
        # seed = request.json['num']
        # print(seed)
        req_data = request.get_json(force=True)
        seed = req_data['num']
        return 'Received:' + str(seed)

    if request.method == 'GET':
        return str(seed)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # default is 5000 if you are using 5000 u dont have to specify port number
