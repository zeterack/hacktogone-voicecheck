import openai
from utils.config import Config

class SpeechService:
    """Service de reconnaissance vocale avec OpenAI Whisper"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
    
    def transcribe_audio(self, audio_url: str) -> str:
        """Transcrit un fichier audio"""
        # Note: En production, il faudrait télécharger l'audio depuis l'URL
        # et l'envoyer à l'API Whisper
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_url
        )
        
        return response['text'].lower().strip()
    
    def analyze_response(self, transcription: str) -> bool:
        """Analyse la réponse vocale pour détecter oui/non"""
        transcription = transcription.lower()
        
        # Mots-clés positifs
        positive_keywords = ['oui', 'yes', 'confirme', 'exact', "c'est moi", 'correct']
        
        # Mots-clés négatifs
        negative_keywords = ['non', 'no', 'pas moi', 'jamais', 'faux']
        
        # Vérifie les mots-clés positifs
        if any(keyword in transcription for keyword in positive_keywords):
            return True
        
        # Vérifie les mots-clés négatifs
        if any(keyword in transcription for keyword in negative_keywords):
            return False
        
        # Par défaut, considère comme non confirmé
        return False
