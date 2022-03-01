from flask import Flask, request, Response, jsonify, redirect
import requests
from urllib.parse import urljoin
from hashlib import sha256

app = Flask(__name__)

links = {
    "1": "https://mail.ru",
    "12": "https://google.com",
    "123": "https://vk.com"
}


def make_link_short(full_link):

    global links
    link_id = sha256(full_link.encode()).hexdigest()[:8]
    links.update({link_id: full_link})

    return link_id


@app.route('/<path>', methods=['GET'])
def redirect_to_other_domain(path):
    url = links.get(path)
    if not url:
        return "not url"
    return redirect(url)


@app.route('/api/v1/short', methods=['GET'])
def make_short_link():
    if not request.args:
        return "no args"
    query_params = request.args.to_dict()
    full_link = query_params.get('link')
    short_link = make_link_short(full_link)

    return short_link


@app.route('/api/v1/full', methods=['GET'])
def get_short_link():
    if not request.args:
        return "error"
    query_params = request.args.to_dict()
    link_id = query_params.get('id')
    short_link = links.get(link_id)
    if not short_link:
        return "error"
    return short_link


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