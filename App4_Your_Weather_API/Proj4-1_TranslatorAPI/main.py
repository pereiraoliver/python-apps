import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

df = pd.read_csv("downloads/dictionary.csv")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<word>")
def translate(word):
    definition = df.loc[df["word"] == word]["definition"].squeeze()
    return {"definition": definition, "word": word}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
