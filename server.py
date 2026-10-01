import random
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "pendu_secret"

with open("dictionnaire.txt", "r", encoding="utf-8") as fichier:
    mots = fichier.read().splitlines()


@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":
        session["nom"] = request.form["nom"]
        session["mot"] = random.choice(mots).split(";")[0] 
        mot_indice = "_ " * len(session["mot"])
        session["vies"] = 5
        return render_template("jeu.html", nom=session["nom"], mot_indice=mot_indice, vies=session["vies"])
        
    return render_template("hello.html")