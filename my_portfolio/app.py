from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    projects = [
        "Plan de cuotas",
        "Hotel",
        "Psicologo"
    ]

    return render_template(

        "index.html",
        name="<h1>hola</h1>",
        degree="Software engineer student",
        projects=projects
    )

@app.route("/Menu")
def menu():
    menu_items = [
        "Choripan",
        "Majadito",
        "Saice",
        "Sopa de Kawi"
    ]
    
    return render_template(
        "Menu/index.html",
        menu_items=menu_items
    )

if __name__ == "__main__":
    app.run(debug=True)