from io import StringIO
import json
import pandas as pd

from flask import Flask, request, jsonify, render_template, abort
# noinspection PyPackageRequirements
from werkzeug.exceptions import HTTPException

from learn import Train, Predict
from db_manager import DBManager
from config import DATABASE

import logging

logging.basicConfig(filename="sample.log", level=logging.DEBUG)
log = logging.getLogger("main")


db = DBManager(DATABASE)

app = Flask(__name__)

BROWSER = 'from_browser'


@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = json.dumps({
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }})
        response.content_type = "application/json"
    else:
        response = {"error": e.args[0]}

    return response


@app.route('/')
def instructions():
    if BROWSER == 'from_browser':
        return render_template('index.html'), 200
    else:
        return jsonify({"instructions": "to make DB go to /create_db"})


@app.route('/create_db')
def create():
    try:
        result = db.create_db()
    except Exception as exc:
        abort(500, f"Error while creating DB: {exc}")
        return
    return {"create_db": f"{result}"}


@app.route('/ann')
def easter_egg():
    abort(418)
    return


@app.route('/train', methods=['POST'])
def train():
    if request.form.get('source') == BROWSER:
        args = json.loads(request.form.get('json'))
    else:
        args = request.get_json()

    try:  # read data
        data = pd.read_csv(StringIO(args['data']), delimiter=',')
        target = str(args['target'])
        n_folds = int(args['n_folds'])
        fit_intercept = bool(args['fit_intercept'])
        l2_coef = list(args['l2_coef'])
    except Exception as exc:
        abort(400, f"Error: {exc}")
        return

    try:  # train model and add results to DB
        model = Train(data, target, n_folds, fit_intercept, l2_coef)
        model_info = model.model_info

        model_id = db.add_model(model_info)

    except Exception as exc:
        abort(500, f"Error: {exc}")
        return

    if request.form.get('source') == BROWSER:
        return f'''<h1>Your model ID is {model_id}<h1>
                   <form action="/model/{model_id}" method="get">
                   <button type="submit" class="btn tm-btn-submit" name="source" value="from_browser">
                   go to model info</button></form>''', 200
    else:
        return jsonify({"model_id": model_id})


@app.route('/model/<int:model_id>', methods=['GET'])
def get_model(model_id):
    try:
        found = db.get_model(model_id)
    except Exception as exc:
        abort(500, f"Error: {exc}")
        return
    if len(request.args) > 0:
        if request.args['source'] == BROWSER:
            return render_template('predict.html', model_id=model_id), 200
    else:
        return jsonify({"model": found.model, "cv_results": found.cv_results})


@app.route('/model/<int:model_id>/predict', methods=['Post'])
def predict(model_id):
    if request.form.get('source') == BROWSER:
        args = json.loads(request.form.get('json'))
    else:
        args = request.get_json()
    try:
        data = pd.read_csv(StringIO(args['data']), delimiter=',')

        found = db.get_model(model_id)

        results = Predict(found, data).results_

    except Exception as exc:
        abort(400, f"Error: {exc}")
        return

    return jsonify({"result": results})


app.run()
