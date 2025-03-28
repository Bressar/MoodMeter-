# MoodMeter
# Front End
""" 
criado em: 28/03/2025
atualizado em:
By Doug Bressar 
"""

# app.py
from flask import Flask, render_template, request, jsonify
from backend import BackEnd  # Importando a classe de backend

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    URL = request.form['youtube_url']
    
    # Instanciar a classe BackEnd e processar o vídeo
    backend = BackEnd(URL)
    emotion_report = backend.process_video()

    # Retornar o relatório ao usuário
    return render_template('report.html', emotion_report=emotion_report)

if __name__ == "__main__":
    app.run(debug=True)
