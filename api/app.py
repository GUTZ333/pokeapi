from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/search", methods=["GET", "POST"])
def buscarpokemom():
    metodo_de_formulario = request.method
    match metodo_de_formulario:
        case "GET":
            nome_enviado_usuario = request.args.get("name-pokemom")
            api_link = f"https://pokeapi.co/api/v2/pokemon/{nome_enviado_usuario.lower()}"
            response = requests.get(url=api_link)
            conexao_api = response.status_code
            match conexao_api:
                case 200:
                    dados_api_pokemom = response.json()
                    nome_pokemon = dados_api_pokemom["name"]
                    imagem_pokemon = dados_api_pokemom["sprites"]["other"]["official-artwork"]["front_default"]
                    base_experiencia = dados_api_pokemom["base_experience"]
                    altura = dados_api_pokemom["height"]
                    peso = dados_api_pokemom["weight"]
                    ordem_oficial = dados_api_pokemom["order"]
                    habilidades_url = f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon}/abilities"
                    return render_template(
                        template_name_or_list="search.html",
                        title=nome_pokemon,
                        nome=nome_pokemon,
                        img=imagem_pokemon,
                        base_experience=base_experiencia,
                        altura=altura,
                        peso=peso,
                        ordem_oficial=ordem_oficial,
                        url_habilidades=habilidades_url
                    )
                case _:
                    flash(message="* This Pokemon was not found.", category="not-found")
                    return redirect(url_for("home"))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)