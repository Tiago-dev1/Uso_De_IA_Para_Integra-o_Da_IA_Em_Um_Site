import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@app.route("/")
def pagina_inicial():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def enviar_para_openrouter():
    pergunta_do_usuario = request.form.get("mensagem")
    
    try:
        resposta_da_api = client.chat.completions.create(
            model="openrouter/auto",
            messages=[
                {"role": "system", "content": "Você é um assistente prestativo e responde em português."},
                {"role": "user", "content": pergunta_do_usuario}
            ],
            extra_body={
                "models": ["free"]
            }
        )
        resultado = resposta_da_api.choices[0].message.content
    except Exception as erro:
        resultado = f"Erro ao chamar o OpenRouter: {erro}"

    return render_template("index.html", resposta=resultado)

if __name__ == "__main__":
    app.run(debug=True)