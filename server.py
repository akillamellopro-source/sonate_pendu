import random
from flask import Flask, render_template, request

app = Flask(__name__)
with open("dictionnaire.txt", "r", encoding="utf-8") as fichier:
    mots = fichier.read().splitlines()


@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":
        nom = request.form["nom"]
        mot = random.choice(mots).split(";")[0]      
        
    return render_template("hello.html")