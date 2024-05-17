from typing import Literal

from app import app
from flask import abort, flash, jsonify, redirect, render_template, request, Response, send_from_directory, session, url_for
from tasks import background_task_email, long_task


@app.route('/favicon.ico')
# @app.route('/robots.txt')
def from_root_url() -> Response:
    path = request.path[1:]
    return send_from_directory(app.static_folder, path)


@app.route('/', methods=['GET', 'POST'])
def index() -> (str | Response):
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    elif request.method == 'POST':
        email = request.form['email']
        session['email'] = email
        if request.form['submit'] == 'Send':
            # send right away
            # send_email()
            background_task_email.delay(email)
            flash(f'Sending email to {email}')
        else:
            # send in one minute
            background_task_email.apply_async(args=[email], countdown=10)
            flash(f'An email will be sent to {email} in 10 seconds')

        return redirect(url_for('index'))
    else:
        return abort(405)


@app.route('/longtask', methods=['POST'])
def longtask() -> tuple[Response, Literal[202], dict[str, str]]:
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id) -> Response:
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
                    'state': task.state,
                    'current': 0,
                    'total': 1,
                    'status': 'Ожидает...'
                    }
    elif task.state != 'FAILURE':
        response = {
                    'state': task.state,
                    'current': task.info.get('current', 0),
                    'total': task.info.get('total', 1),
                    'status': task.info.get('status', '')
                    }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
                    'state': task.state,
                    'current': 0,
                    'total': 1,
                    'status': str(task.info),  # this is the exception raised
                    }
    return jsonify(response)
