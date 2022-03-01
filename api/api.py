from flask import Flask, request, Response, jsonify
import requests
from urllib.parse import urljoin


app = Flask(__name__)

links = {
    "1": "https://mail.ru",
    "12": "https://google.com",
    "123": "https://vk.com"
}


@app.route('/', methods=['GET'])
def index():
    return "hello"


@app.route('/api/v1/short', methods=['GET'])
def make_short_link():
    print(request.args.to_dict())
    if not request.args:
        return "no args"
    return "done"

@app.route('/api/v1/full', methods=['GET'])
def get_short_link():
    print(request.args.to_dict())
    if request.args not in links:
        return "error"
    return "done"


"""@app.route('/<path:path>', methods=["GET", "POST", "DELETE"])
def proxy(path):
    global SITE_NAME
    all_args = request.args.to_dict()
    if request.method == 'GET':
        url = urljoin(SITE_NAME, path)
        resp = requests.get(url=url, params=all_args)
        resp.raise_for_status()
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers,)
        return response"""

if __name__ == '__main__':
    app.run()