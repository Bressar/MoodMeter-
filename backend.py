# backend.py
from pytube import YouTube
import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter
import os

class BackEnd:
    def __init__(self, URL):
        self.URL = URL
        self.video_path = 'static/downloaded_video.mp4'
        self.emotions = []

    def download_video(self):
        """ Função para baixar o vídeo do YouTube """
        try:
            video = YouTube(self.URL)
            stream = video.streams.filter(progressive=True, file_extension="mp4").first()
            stream.download(filename=self.video_path)
            return True
        except Exception as e:
            print(f"Erro ao baixar vídeo: {e}")
            return False

    def process_video(self):
        """ Função principal para processar o vídeo e gerar o relatório """
        if not self.download_video():
            return {"error": "Erro ao baixar o vídeo"}

        # Processar o vídeo
        emotions = self.process_emotions(self.video_path)
        
        # Gerar o relatório de emoções
        emotion_report = self.generate_report(emotions)
        
        return emotion_report

    def process_emotions(self, video_path):
        """ Função para processar o vídeo e detectar emoções em cada frame """
        cap = cv2.VideoCapture(video_path)
        emotions = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Detectar a emoção no frame
            emotion = self.detect_emotion(frame)
            emotions.append(emotion)

        cap.release()
        return emotions

    def detect_emotion(self, frame):
        """ Função para detectar a emoção utilizando DeepFace """
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            return analysis[0]['dominant_emotion']
        except Exception as e:
            print(f"Erro ao analisar emoção: {e}")
            return "unknown"

    def generate_report(self, emotions):
        """ Função para gerar o gráfico e o relatório das emoções """
        emotion_counts = Counter(emotions)

        # Gerar gráfico das emoções
        labels, values = zip(*emotion_counts.items())
        plt.bar(labels, values)
        plt.xlabel('Emoções')
        plt.ylabel('Frequência')
        plt.title('Frequência das Emoções Detectadas')

        # Criar pasta 'static' caso não exista
        if not os.path.exists('static'):
            os.makedirs('static')

        plt.savefig('static/emotion_report.png')
        plt.close()

        return emotion_counts
