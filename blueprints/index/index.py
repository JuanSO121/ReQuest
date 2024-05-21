from flask import Blueprint, render_template, redirect

index_bp = Blueprint("index", __name__, template_folder="templates")

@index_bp.route("/")
def index():
    return "Hello World!"

@index_bp.route("/hello")
def hello():
    return "Hello world again!"

@index_bp.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}!"