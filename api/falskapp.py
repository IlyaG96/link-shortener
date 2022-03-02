from flask import request, redirect, jsonify
from hashlib import sha256
from api import app, redis
from enum import Enum


class Responses(Enum):
    NO_SUCH_SHORT_LINK = {'message': 'no such short link in database'}
    NOT_QUERY_PARAMS = {'message': 'have not got query params'}
    INCORRECT_QUERY_PARAMS = {'message': 'incorrect query params'}


def write_custom_link_db(full_link, link_name):

    link_id = link_name

    redis.hset(link_id, link_id, full_link)
    redis.hset(full_link, full_link, link_id)

    return link_id


def write_link_db(full_link):
    link_id = sha256(full_link.encode()).hexdigest()[:8]
    redis.hset(link_id, link_id, full_link)
    redis.hset(full_link, full_link, link_id)

    return link_id


@app.route('/<link_id>', methods=['GET'])
def redirect_to_other_domain(link_id):
    url = redis.hget(link_id, link_id).decode()
    if not url:
        return jsonify(Responses.NO_SUCH_SHORT_LINK)
    return redirect(url)


@app.route('/api/custom', methods=['GET'])
def make_custom_link():
    if not request.args:
        return jsonify(Responses.NOT_QUERY_PARAMS)

    query_params = request.args.to_dict()
    full_link = query_params.get('link')
    link_name = query_params.get('name')
    link_id = write_custom_link_db(full_link, link_name)

    return f'127.0.0.1:5000/{link_id}'


@app.route('/api/make-short', methods=['GET'])
def make_short_link():
    if not request.args:
        return jsonify(Responses.NOT_QUERY_PARAMS)

    query_params = request.args.to_dict()
    full_link = query_params.get('link')
    link_id = write_link_db(full_link)

    return f'127.0.0.1:5000/{link_id}'


@app.route('/api/get-short', methods=['GET'])
def get_short_link():
    if not request.args:
        return jsonify(Responses.NOT_QUERY_PARAMS)
    query_params = request.args.to_dict()
    full_link = query_params.get('link')
    link_id = redis.hget(full_link, full_link).decode()

    if not link_id:
        return jsonify(Responses.NO_SUCH_SHORT_LINK)
    return jsonify({full_link: link_id})


def main():
    app.run()


if __name__ == '__main__':
    main()

