from WorldBankApp import app

import json, plotly
from flask import render_template, request, Response, jsonify
from data import graph


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    figures = graph()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
