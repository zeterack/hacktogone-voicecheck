import pandas as pd
from typing import List, Dict

class CsvHandler:
    """Gestion des imports/exports CSV"""
    
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
        for _, row in df.iterrows():
            telephone = str(row['telephone']).strip()
            
            # Si le numéro ne commence pas par '+', l'ajouter
            if not telephone.startswith('+'):
                telephone = '+' + telephone
            
            contact = {
                'nom': str(row['nom']).strip(),
                'prenom': str(row['prenom']).strip(),
                'telephone': telephone
            }
            contacts.append(contact)
        
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
