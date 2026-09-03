from flask import Flask,render_template

app =Flask(__name__,static_folder="estilos")

rutina=[
     {"nombre":"pecho","ejercicios":5},
    {"nombre":"pierna","ejercicios":8},
    {"nombre":"brazo","ejercicios":12},
    {"nombre":"pecho","ejercicios":6},
]
   


@app.route("/")
def inicio():
    return render_template("index.html",rutina=rutina)


if __name__=="__main__":
    app.run(debug=True)

