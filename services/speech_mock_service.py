import random
import time

class SpeechMockService:
    """Service mock simulant OpenAI Whisper"""
    
    def __init__(self):
        self.positive_responses = [
            "oui",
            "oui c'est moi",
            "oui confirme",
            "c'est bien moi",
            "oui c'est exact",
            "confirme",
            "yes"
        ]
        
        self.negative_responses = [
            "non",
            "non ce n'est pas moi",
            "non pas moi",
            "ce n'est pas moi",
            "jamais",
            "pas du tout"
        ]
    
    def transcribe_audio(self, audio_url: str) -> str:
        """Simule la transcription d'un fichier audio"""
        # Simulation d'un délai de traitement
        time.sleep(1)
        
        # 80% de réponses positives, 20% négatives
        if random.random() < 0.8:
            return random.choice(self.positive_responses)
        else:
            return random.choice(self.negative_responses)
    
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
