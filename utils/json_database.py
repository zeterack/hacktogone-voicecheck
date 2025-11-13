import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

class JsonDatabase:
    """Gestion de la base de données JSON"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.contacts_file = os.path.join(data_dir, "contacts.json")
        self.results_file = os.path.join(data_dir, "results.json")
        self._ensure_files()
        logger.info(f"JsonDatabase initialisée - contacts: {self.contacts_file}, results: {self.results_file}")
    
    def _ensure_files(self):
        """Crée les fichiers s'ils n'existent pas"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w') as f:
                json.dump([], f)
    
    def load_contacts(self) -> List[Dict]:
        """Charge tous les contacts"""
        with open(self.contacts_file, 'r') as f:
            return json.load(f)
    
    def save_contacts(self, contacts: List[Dict]):
        """Sauvegarde tous les contacts"""
        with open(self.contacts_file, 'w') as f:
            json.dump(contacts, f, indent=2)
    
    def add_contacts(self, new_contacts: List[Dict]):
        """Ajoute de nouveaux contacts"""
        contacts = self.load_contacts()
        for contact in new_contacts:
            contact['id'] = self._generate_id(contacts)
            contact['created_at'] = datetime.now().isoformat()
            contact['status'] = 'pending'
            contacts.append(contact)
        self.save_contacts(contacts)
    
    def update_contact_status(self, contact_id: str, status: str):
        """Met à jour le statut d'un contact"""
        logger.info(f"📝 Mise à jour du statut du contact {contact_id} -> {status}")
        
        contacts = self.load_contacts()
        found = False
        for contact in contacts:
            if contact['id'] == contact_id:
                contact['status'] = status
                contact['updated_at'] = datetime.now().isoformat()
                found = True
                logger.info(f"✅ Contact {contact_id} mis à jour: {contact['prenom']} {contact['nom']} -> {status}")
                break
        
        if not found:
            logger.warning(f"⚠️ Contact {contact_id} non trouvé lors de la mise à jour du statut")
        
        self.save_contacts(contacts)
    
    def get_pending_contacts(self) -> List[Dict]:
        """Récupère les contacts en attente"""
        contacts = self.load_contacts()
        return [c for c in contacts if c.get('status') == 'pending']
    
    def load_results(self) -> List[Dict]:
        """Charge tous les résultats"""
        with open(self.results_file, 'r') as f:
            return json.load(f)
    
    def save_result(self, result: Dict):
        """Sauvegarde un résultat d'appel"""
        logger.info(f"💾 Début de la sauvegarde du résultat pour contact_id: {result.get('contact_id')}")
        logger.debug(f"Résultat à sauvegarder: {result}")
        
        results = self.load_results()
        result['timestamp'] = datetime.now().isoformat()
        results.append(result)
        
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"✅ Résultat sauvegardé dans {self.results_file} (total: {len(results)} résultats)")
    
    def get_statistics(self) -> Dict:
        """Calcule les statistiques"""
        results = self.load_results()
        contacts = self.load_contacts()
        
        total_contacts = len(contacts)
        total_calls = len(results)
        
        consent_given = len([r for r in results if r.get('consent') == True])
        consent_refused = len([r for r in results if r.get('consent') == False])
        
        identity_confirmed = len([r for r in results if r.get('identity_confirmed') == True])
        identity_rejected = len([r for r in results if r.get('identity_confirmed') == False])
        
        no_response = len([r for r in results if r.get('no_response') == True])
        
        return {
            'total_contacts': total_contacts,
            'total_calls': total_calls,
            'pending': len([c for c in contacts if c.get('status') == 'pending']),
            'completed': len([c for c in contacts if c.get('status') == 'completed']),
            'consent_given': consent_given,
            'consent_refused': consent_refused,
            'identity_confirmed': identity_confirmed,
            'identity_rejected': identity_rejected,
            'no_response': no_response
        }
    
    def _generate_id(self, contacts: List[Dict]) -> str:
        """Génère un ID unique"""
        if not contacts:
            return "1"
        max_id = max([int(c['id']) for c in contacts if c.get('id', '').isdigit()], default=0)
        return str(max_id + 1)
