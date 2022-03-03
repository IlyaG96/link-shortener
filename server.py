import requests
from flask import request, redirect, jsonify, send_from_directory, render_template, Flask, abort
from hashlib import sha256
from urllib.parse import urljoin
from app_factory import create_app
from werkzeug.exceptions import HTTPException
from flask_redis import Redis
import validators
import os
import re

app = create_app()
redis = Redis()


class Responses:
    NO_SUCH_SHORT_LINK = {'message': 'no such short link in database'}
    NOT_QUERY_PARAMS = {'message': 'have not got query params'}
    INCORRECT_QUERY_PARAMS = {'message': 'incorrect query params'}
    WRONG_QUERY_PARAMS = {'message': 'incorrect query params'}
    INCORRECT_LINK = {'message': 'incorrect link'}
    NAME_ERROR = {'message': 'this name is already exists or have errors (use only nums and latin symbols)'}


def check_name(link_name):

    pattern = '[0-9A-Za-z]'
    if re.match(pattern, link_name):
        return not redis.hget(link_name, link_name)


def check_link(full_link):

    if not validators.url(full_link):
        return False
    try:
        response = requests.get(full_link, timeout=2)
        response.raise_for_status()
        return response.ok or response.is_redirect

    except requests.RequestException:
        return False


def write_link_db(full_link, link_name):

    link_id = link_name

    redis.hset(link_id, link_id, full_link)
    redis.hset(full_link, full_link, link_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')


@app.route('/show_link', methods=['GET', 'POST'])
def show_link():
    full_link = request.form.get('link')
    link_name = request.form.get('link-name').replace(' ', '')

    if not link_name:
        link_name = sha256(full_link.encode()).hexdigest()[:8]
        is_link_correct = check_link(full_link)
        if not is_link_correct:
            context = f'Ошибка в написании ссылки "{full_link}".'
            return render_template('main.html', context=context)

        write_link_db(full_link, link_name)
        context = urljoin('http://localhost:5000', link_name)

        return render_template('main.html', context=context)

    if not check_name(link_name):
        context = f'имя "{link_name}" занято или в имени используются недопустимые символы. ' \
                  f'Используйте только латинские символы'

        return render_template('main.html', context=context)

    is_link_correct = check_link(full_link)

    if not is_link_correct:
        context = f'Ошибка в написании ссылки "{full_link}".'
        return render_template('main.html', context=context)

    write_link_db(full_link, link_name)
    context = urljoin('http://localhost:5000', link_name)

    return render_template('main.html', context=context)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<link_id>')
def redirect_to_other_domain(link_id):

    url = redis.hget(link_id, link_id)

    if not url:
        return jsonify(Responses.NO_SUCH_SHORT_LINK)

    return redirect(url.decode())


@app.route('/api/custom', methods=['GET'])
def make_custom_link():
    if not request.args:
        return jsonify(Responses.NOT_QUERY_PARAMS)

    query_params = request.args.to_dict()

    full_link = query_params.get('link')

    link_name = query_params.get('name')

    if not full_link or not link_name:
        return jsonify(Responses.WRONG_QUERY_PARAMS)

    link_name = link_name.replace(' ', '')

    if not check_name(link_name):
        return jsonify(Responses.NAME_ERROR)

    if not check_link(full_link):
        return jsonify(Responses.INCORRECT_LINK)

    write_link_db(full_link, link_name)

    return jsonify({'message': f'127.0.0.1:5000/{link_name}'})


@app.route('/api/make-short', methods=['GET'])
def make_short_link():
    if not request.args:
        return jsonify(Responses.NOT_QUERY_PARAMS)

    query_params = request.args.to_dict()
    full_link = query_params.get('link')

    if not full_link:
        return jsonify(Responses.WRONG_QUERY_PARAMS)

    if not check_link(full_link):
        return jsonify(Responses.INCORRECT_LINK)

    link_name = sha256(full_link.encode()).hexdigest()[:8]
    write_link_db(full_link, link_name)

    return f'127.0.0.1:5000/{link_name}'


@app.route('/api/get-short', methods=['GET'])
def get_short_link():
    if not request.args:
        return jsonify(Responses.NOT_QUERY_PARAMS)
    query_params = request.args.to_dict()
    full_link = query_params.get('link')

    if not full_link:
        return jsonify(Responses.WRONG_QUERY_PARAMS)

    link_name = redis.hget(full_link, full_link).decode()

    if not link_name:
        return jsonify(Responses.NO_SUCH_SHORT_LINK)

    return jsonify({full_link: link_name})


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }

    return jsonify(response)


def main():
    app.run(use_reloader=True)


if __name__ == '__main__':
    main()
