from typing import Dict, List
from utils.json_database import JsonDatabase

class AnalysisService:
    """Service d'analyse des résultats"""
    
    def __init__(self, db: JsonDatabase):
        self.db = db
    
    def get_campaign_summary(self) -> Dict:
        """Résumé de la campagne"""
        stats = self.db.get_statistics()
        
        # Calcul des taux
        total_calls = stats['total_calls']
        
        if total_calls > 0:
            consent_rate = (stats['consent_given'] / total_calls) * 100
            identity_rate = (stats['identity_confirmed'] / total_calls) * 100
            success_rate = (stats['identity_confirmed'] / total_calls) * 100
            no_response_rate = (stats['no_response'] / total_calls) * 100
        else:
            consent_rate = identity_rate = success_rate = no_response_rate = 0
        
        return {
            'total_contacts': stats['total_contacts'],
            'total_calls': total_calls,
            'pending': stats['pending'],
            'completed': stats['completed'],
            'consent_given': stats['consent_given'],
            'consent_refused': stats['consent_refused'],
            'consent_rate': round(consent_rate, 2),
            'identity_confirmed': stats['identity_confirmed'],
            'identity_rejected': stats['identity_rejected'],
            'identity_rate': round(identity_rate, 2),
            'no_response': stats['no_response'],
            'no_response_rate': round(no_response_rate, 2),
            'success_rate': round(success_rate, 2)
        }
    
    def get_detailed_results(self) -> List[Dict]:
        """Résultats détaillés de tous les appels"""
        return self.db.load_results()
    
    def get_contacts_to_recall(self) -> List[Dict]:
        """Liste des contacts à rappeler (répondeur détecté, pas de consentement, ou identité non confirmée)"""
        results = self.db.load_results()
        contacts = self.db.load_contacts()
        
        # IDs des contacts à rappeler
        to_recall_ids = set()
        
        for result in results:
            # Rappeler si:
            # - Répondeur détecté (consent=false, identity_confirmed=false, reasoning contient "répondeur")
            # - Pas de réponse (no_response=true)
            # - Consentement refusé (consent=false et pas répondeur)
            # - Identité non confirmée (identity_confirmed=false)
            # - Consentement ou identité null (pas de réponse claire)
            
            reasoning = result.get('reasoning') or ''
            is_voicemail = 'répondeur' in reasoning.lower() or 'boîte vocale' in reasoning.lower()
            
            consent = result.get('consent')
            identity = result.get('identity_confirmed')
            no_response = result.get('no_response', False)
            
            should_recall = (
                no_response or  # Pas de réponse
                is_voicemail or  # Répondeur détecté
                consent is False or  # Consentement refusé
                consent is None or  # Consentement non obtenu
                identity is False or  # Identité rejetée
                identity is None  # Identité non confirmée
            )
            
            if should_recall:
                to_recall_ids.add(result.get('contact_id'))
        
        # Récupère les informations complètes des contacts
        return [c for c in contacts if c.get('id') in to_recall_ids]
