from gtts import gTTS
import PyPDF2
import os
from pydub import AudioSegment

def pdf_to_audio(pdf_path, audio_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    
    if not text:
        print("No text could be extracted from the PDF.")
        return
    
    tts = gTTS(text=text, lang='en')
    
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    temp_audio_path = 'temp_audio.mp3'
    tts.save(temp_audio_path)
    
    audio = AudioSegment.from_mp3(temp_audio_path)
    
    audio.export(audio_path, format='mp3')
    
    os.remove(temp_audio_path)
    
    print(f'The audio file has been saved at: {audio_path}')

pdf_path = 'your pdf path'
audio_path = os.path.join(os.getcwd(), 'audio_output.mp3')

pdf_to_audio(pdf_path, audio_path)
