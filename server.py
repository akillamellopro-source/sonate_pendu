import random
import unicodedata
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "pendu_secret"
pendu = [
    """
 +---+
 |   |
     |
     |
     |
     |
=======""",

    """
 +---+
 |   |
 O   |
     |
     |
     |
=======""",

    """
 +---+
 |   |
 O   |
 |   |
     |
     |
=======""",

    """
 +---+
 |   |
 O   |
/|   |
     |
     |
=======""",

    """
 +---+
 |   |
 O   |
/|\\  |
/    |
     |
=======""",

    """
 +---+
 |   |
 O   |
/|\\  |
/ \\  |
     |
======="""
]

def sans_accent(texte):
    texte = unicodedata.normalize("NFD", texte)
    return "".join(
        caractere for caractere in texte
        if unicodedata.category(caractere) != "Mn"
    )

with open("dictionnaire.txt", "r", encoding="utf-8") as fichier:
    mots = fichier.read().splitlines()


@app.route("/",methods=["GET","POST"])
def home():
    if request.method == "POST":
        session["nom"] = request.form["nom"]
        session["mot"] = random.choice(mots).split(";")[0]
        mot_indice = ""

        for caractere in session["mot"]:
            if caractere == "'":
                mot_indice += "' "
            else:
                mot_indice += "_ "
        session["vies"] = 5
        session["lettres_trouvees"] = []
        session["lettres_jouees"] = []
        return render_template("jeu.html", nom=session["nom"], mot_indice=mot_indice, vies=session["vies"])
    
    return render_template("hello.html")
      
@app.route("/jeu", methods=["POST"])
def jeu():
    lettre = request.form["lettre"]

    lettres_jouees = session["lettres_jouees"]
    lettres_jouees.append(lettre)
    session["lettres_jouees"] = lettres_jouees

    if lettre in sans_accent(session["mot"]).upper():
        message = "Bonne lettre"

        lettres_trouvees = session["lettres_trouvees"]
        lettres_trouvees.append(lettre)
        session["lettres_trouvees"] = lettres_trouvees
    else:
        message = "Mauvaise lettre"
        session["vies"] -=1

        if session["vies"] == 0:
            return render_template(
                "perdu.html",
                  mot=session["mot"],
                  dessin=pendu[5]
                  )

    mot_indice = ""

    for caractere in session["mot"]:
        if caractere == "'":
            mot_indice += "' "
        elif sans_accent(caractere).upper() in session["lettres_trouvees"]:
            mot_indice += caractere + " "
        else:
            mot_indice += "_ "

    if "_" not in mot_indice:
        return render_template(
            "gagne.html",
            nom=session["nom"],
            mot=session["mot"]
        )

    return render_template(
        "jeu.html",
        nom=session["nom"],
        mot_indice=mot_indice,
        vies=session["vies"],
        message=message,
        lettres_jouees=session["lettres_jouees"],
        dessin=pendu[5 - session["vies"]],
    )
   