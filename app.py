# MoodMeter
""" 
criado em: 28/03/2025
atualizado em:
By Doug Bressar 
"""

from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter

app = Flask(__name__)
  
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    URL = request.form['youtube_url']
       
        
class back_end:
    def __init__(self):
        # Extrair vídeo usando pytube
        self.video = YouTube(URL)
        self.stream = self.video.streams.filter(progressive=True, file_extension="mp4").first()
        self.video_path = 'downloaded_video.mp4'
        self.stream.download(filename=self.video_path)

        # Processar vídeo
        self.emotions = self.process_emotions(self.video_path)

        # Gerar o relatório de emoções
        self.emotion_report = self.generate_report(self.emotions)
        
        return render_template('report.html', emotion_report=self.emotion_report)

    def process_emotions(self, video_path):
        # Carregar o vídeo com OpenCV
        cap = cv2.VideoCapture(video_path)
        self.emotions = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Detectar emoções no frame
            self.emotion = self.detect_emotion(frame)
            self.emotions.append(self.emotion)
        
        cap.release()
        return self.emotions

    def detect_emotion(self, frame):
        # Analisar a emoção usando DeepFace
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return analysis[0]['dominant_emotion']

    
    def generate_report(self, emotions):
        # Contabilizar as emoções
        emotion_counts = Counter(emotions)

        # Gerar gráfico
        labels, values = zip(*emotion_counts.items())
        plt.bar(labels, values)
        plt.xlabel('Emoções')
        plt.ylabel('Frequência')
        plt.title('Frequência das Emoções Detectadas')
        plt.savefig('static/emotion_report.png')
        
        return emotion_counts


if __name__ == "__main__":
    app.run(debug=True)
