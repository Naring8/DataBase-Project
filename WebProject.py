from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
