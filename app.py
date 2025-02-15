from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse
import re
from json import loads
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from collections import defaultdict

def entrar_pagina(url="https://www.youtube.com/playlist?list=PLLD-rQdLK4I36gBOf-eWmXc4Is5DRUA2W"):
    try:
        b.get(url)
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao entrar na página: {e}")

tempo = 0.01

def pegar_videos():
    try:
        y_l = b.find_elements(By.TAG_NAME, 'ytd-playlist-video-renderer') 
        lista = []
        for y in y_l:
            b.execute_script("arguments[0].scrollIntoView(true);", y)
            y = y.find_element(By.TAG_NAME, 'a')
            y = y.get_attribute("href")
            lista.append(y)
            time.sleep(tempo)
        return lista
    except Exception as e:
        print(f"Erro ao pegar vídeos: {e}")
        return []

def extrair_transcricao(video_url):
    try:
        video_id = re.search(r"v=([a-zA-Z0-9_-]+)", video_url).group(1)
        transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        transcricao_por_tempo = defaultdict(str)

        for item in transcricao:
            minuto_segundo = f"{int(item['start'] // 60):02}:{int(item['start'] % 60):02}"
            transcricao_por_tempo[minuto_segundo] += " " + item['text']

        return dict(transcricao_por_tempo)
    except TranscriptsDisabled:
        print(f"Transcrição desativada para o vídeo: {video_url}")
        return {}
    except Exception as e:
        print(f"Erro ao extrair transcrição do vídeo {video_url}: {e}")
        return {}

def salvar_transcricoes_em_txt(lista_links):
    try:
        with open('transcricoes.txt', 'w', encoding='utf-8') as arquivo:
            for video_url in lista_links:
                try:
                    b.get(video_url)
                    time.sleep(1)
                    titulo_video = b.title
                    transcricao = extrair_transcricao(video_url)

                    if not transcricao:
                        continue

                    arquivo.write(f"Título: {titulo_video}\n\n")
                    for tempo, texto in transcricao.items():
                        arquivo.write(f"{tempo}: {texto}\n")
                    arquivo.write("\n" + "="*50 + "\n\n")
                except Exception as e:
                    print(f"Erro ao processar o vídeo {video_url}: {e}")
    except Exception as e:
        print(f"Erro ao salvar transcrições: {e}")

b = Chrome()
entrar_pagina()
lista_videos_links = pegar_videos()
salvar_transcricoes_em_txt(lista_videos_links)
