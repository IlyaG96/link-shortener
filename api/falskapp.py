from flask import request, redirect
from hashlib import sha256
from api import app, redis


def write_link_db(full_link):
    link_id = sha256(full_link.encode()).hexdigest()[:8]
    redis.hset('test', link_id, full_link)

    return link_id


@app.route('/<link_id>', methods=['GET'])
def redirect_to_other_domain(link_id):
    url = redis.hget('test', link_id).decode()
    if not url:
        return 'not url'
    return redirect(url)


# @app.route('/api/v1/short/custom', methods=['GET']) TODO custom link


@app.route('/api/v1/short', methods=['GET'])
def make_short_link():
    if not request.args:
        return 'no args'

    query_params = request.args.to_dict()
    full_link = query_params.get('link')
    link_id = write_link_db(full_link)

    return f'127.0.0.1:5000/{link_id}'


@app.route('/api/v1/full', methods=['GET'])
def get_short_link():
    if not request.args:
        return 'error'
    query_params = request.args.to_dict()
    link_id = query_params.get('id')
    short_link = redis.hget('test', link_id)
    if not short_link:
        return 'error'
    return short_link


def main():
    app.run()


if __name__ == '__main__':
    main()

