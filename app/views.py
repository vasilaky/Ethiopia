from app import app
from flask import render_template, request, redirect, g
from psycopg2 import connect, extras
#from config import *

@app.route("/", methods=["GET","POST"])
def index():
	return "HEllo"
