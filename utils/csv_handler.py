import pandas as pd
import re
from typing import List, Dict

class CsvHandler:
    """Gestion des imports/exports CSV"""
    
    @staticmethod
    def format_phone_number(phone: str) -> str:
        """
        Formate un numéro de téléphone au format international
        Exemples:
        - '0612345678' -> '+33612345678'
        - '06 12 34 56 78' -> '+33612345678'
        - '33612345678' -> '+33612345678'
        - '+33612345678' -> '+33612345678'
        """
        # Nettoyer: enlever espaces, points, tirets, parenthèses
        phone = re.sub(r'[\s\.\-\(\)]', '', phone.strip())
        
        # Si le numéro commence par '00', remplacer par '+'
        if phone.startswith('00'):
            phone = '+' + phone[2:]
        
        # Si le numéro commence par '0' (numéro français local)
        elif phone.startswith('0') and not phone.startswith('00'):
            # Enlever le 0 et ajouter +33
            phone = '+33' + phone[1:]
        
        # Si le numéro commence par un chiffre (pas de +), ajouter +
        elif phone[0].isdigit() and not phone.startswith('+'):
            phone = '+' + phone
        
        # Validation basique: doit commencer par + et contenir au moins 10 chiffres
        if not phone.startswith('+') or len(re.sub(r'\D', '', phone)) < 10:
            raise ValueError(f"Format de téléphone invalide: {phone}")
        
        return phone
    
    @staticmethod
    def import_contacts(file) -> List[Dict]:
        """Importe des contacts depuis un fichier CSV"""
        # Force la colonne 'telephone' à être lue comme string pour conserver le '+'
        df = pd.read_csv(file, dtype={'telephone': str})
        
        # Validation des colonnes requises
        required_columns = ['nom', 'prenom', 'telephone']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Le CSV doit contenir les colonnes : {', '.join(required_columns)}")
        
        contacts = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                telephone = CsvHandler.format_phone_number(str(row['telephone']))
                
                contact = {
                    'nom': str(row['nom']).strip(),
                    'prenom': str(row['prenom']).strip(),
                    'telephone': telephone
                }
                contacts.append(contact)
            except ValueError as e:
                errors.append(f"Ligne {idx + 2}: {str(e)}")
        
        if errors:
            raise ValueError("Erreurs de formatage:\n" + "\n".join(errors))
        
        return contacts
    
    @staticmethod
    def export_results(results: List[Dict]) -> pd.DataFrame:
        """Exporte les résultats vers un DataFrame"""
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Ajouter des colonnes calculées pour une meilleure lisibilité
        df['refus_explicite'] = df.apply(lambda row: 
            row.get('consent') == False and 
            row.get('reasoning') and 
            'répondeur' not in str(row.get('reasoning', '')).lower(),
            axis=1
        )
        
        df['repondeur'] = df.apply(lambda row:
            'répondeur' in str(row.get('reasoning', '')).lower() or
            'boîte vocale' in str(row.get('reasoning', '')).lower(),
            axis=1
        )
        
        # Sélection et ordre des colonnes
        columns = [
            'timestamp', 'contact_id', 'nom', 'prenom', 'telephone',
            'consent', 'refus_explicite', 'identity_confirmed', 
            'repondeur', 'no_response', 'reasoning'
        ]
        
        # Ajouter les colonnes manquantes
        for col in columns:
            if col not in df.columns:
                df[col] = None
        
        result_df = df[columns].copy()
        
        # Renommer les colonnes en français pour l'affichage
        result_df = result_df.rename(columns={
            'timestamp': 'Date/Heure',
            'contact_id': 'ID Contact',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'telephone': 'Téléphone',
            'consent': 'Consentement',
            'refus_explicite': 'Refus explicite',
            'identity_confirmed': 'Identité confirmée',
            'repondeur': 'Répondeur détecté',
            'no_response': 'Pas de réponse',
            'reasoning': 'Raison'
        })
        
        return result_df
    
    @staticmethod
    def create_sample_csv(filename: str):
        """Crée un fichier CSV d'exemple"""
        sample_data = {
            'nom': ['Dupont', 'Martin', 'Durand'],
            'prenom': ['Jean', 'Marie', 'Pierre'],
            'telephone': ['+33612345678', '+33687654321', '+33698765432']
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(filename, index=False)
