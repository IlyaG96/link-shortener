from flask import Flask, request, redirect
from environs import Env
from hashlib import sha256
from flask_redis import Redis

app = Flask(__name__)

env = Env()
env.read_env()
redis_host = env.str('REDIS_HOST')
redis_port = env.str('REDIS_PORT')
redis_password = env.str('REDIS_PASSWORD')
app.config['REDIS_HOST'] = redis_host
app.config['REDIS_PORT'] = redis_port
app.config['REDIS_PASSWORD'] = redis_password

redis = Redis(app)

links = {}


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

    return f'http://127.0.0.1/{link_id}'


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

