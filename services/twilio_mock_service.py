import random
import time
from typing import Dict

class TwilioMockService:
    """Service mock simulant Twilio pour les tests"""
    
    def __init__(self):
        self.call_counter = 0
    
    def make_call(self, to_number: str, contact_id: str) -> str:
        """Simule l'initiation d'un appel"""
        self.call_counter += 1
        call_sid = f"MOCK_CALL_{self.call_counter}_{int(time.time())}"
        
        # Simulation d'un délai réseau
        time.sleep(0.5)
        
        return call_sid
    
    def simulate_consent_response(self) -> Dict:
        """Simule la réponse au consentement DTMF"""
        # 70% acceptent, 20% refusent, 10% pas de réponse
        rand = random.random()
        
        if rand < 0.7:
            return {
                'consent': True,
                'dtmf': '1',
                'no_response': False
            }
        elif rand < 0.9:
            return {
                'consent': False,
                'dtmf': '2',
                'no_response': False
            }
        else:
            return {
                'consent': None,
                'dtmf': None,
                'no_response': True
            }
    
    def simulate_identity_confirmation(self) -> Dict:
        """Simule la réponse de confirmation d'identité vocale"""
        # 80% confirment, 15% refusent, 5% pas de réponse
        rand = random.random()
        
        responses_yes = ["oui", "oui c'est moi", "oui confirme", "c'est bien moi"]
        responses_no = ["non", "non ce n'est pas moi", "non pas moi"]
        
        if rand < 0.8:
            return {
                'identity_confirmed': True,
                'transcription': random.choice(responses_yes),
                'no_response': False
            }
        elif rand < 0.95:
            return {
                'identity_confirmed': False,
                'transcription': random.choice(responses_no),
                'no_response': False
            }
        else:
            return {
                'identity_confirmed': None,
                'transcription': '',
                'no_response': True
            }
    
    def generate_consent_twiml(self) -> str:
        """Génère un TwiML mock"""
        return "<?xml version='1.0' encoding='UTF-8'?><Response><Gather>MOCK TWIML</Gather></Response>"
    
    def generate_identity_twiml(self, nom: str, prenom: str) -> str:
        """Génère un TwiML mock"""
        return f"<?xml version='1.0' encoding='UTF-8'?><Response><Say>MOCK: Êtes-vous {prenom} {nom}?</Say></Response>"
    
    def generate_thank_you_twiml(self) -> str:
        """Génère un TwiML mock"""
        return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>MOCK: Merci</Say></Response>"
    
    def generate_goodbye_twiml(self) -> str:
        """Génère un TwiML mock"""
        return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>MOCK: Au revoir</Say></Response>"
