import streamlit as st

class Config:
    """Configuration centralisée de l'application
    
    Utilise st.secrets pour la compatibilité avec Streamlit Cloud.
    Les secrets sont définis dans .streamlit/secrets.toml (local)
    ou dans les paramètres de l'app sur Streamlit Cloud.
    """
    
    @staticmethod
    def get_secret(key: str, default: str = '') -> str:
        """Récupère un secret depuis st.secrets avec fallback
        
        Args:
            key: Nom de la clé du secret
            default: Valeur par défaut si le secret n'existe pas
            
        Returns:
            La valeur du secret ou la valeur par défaut
        """
        try:
            return st.secrets.get(key, default)
        except (FileNotFoundError, KeyError, AttributeError):
            # Si secrets.toml n'existe pas ou st.secrets n'est pas initialisé
            return default
    
    # OpenAI
    @property
    def OPENAI_API_KEY(self) -> str:
        return self.get_secret('OPENAI_API_KEY', '')
    
    # Bland AI (remplace Twilio)
    @property
    def BLEND_API_KEY(self) -> str:
        return self.get_secret('BLEND_API_KEY', '')
    
    @property
    def BLEND_ENDPOINT(self) -> str:
        return self.get_secret('BLEND_ENDPOINT', 'https://api.bland.ai/v1/calls')
