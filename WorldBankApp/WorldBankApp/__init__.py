from flask import Flask

app = Flask(__name__)

from WorldBankApp import routes
