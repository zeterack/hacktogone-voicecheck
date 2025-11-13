import streamlit as st
import time
import logging
from utils.config import Config
from utils.json_database import JsonDatabase
from utils.csv_handler import CsvHandler
from services.twilio_service import BlendService
from services.openai_service import OpenAIService
from services.analysis_service import AnalysisService

# Configuration du logger pour l'app
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/app.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Configuration de la page
st.set_page_config(
    page_title="VoiceCheck AI",
    page_icon="📞",
    layout="wide"
)

# Initialisation de la base de données
db = JsonDatabase()
analysis = AnalysisService(db)

# Initialisation des services
twilio_service = BlendService()
openai_service = OpenAIService()

# Titre
st.title("📞 VoiceCheck AI")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📞 Campagne", "📥 Export"])

# TAB 1: Dashboard
with tab1:
    st.header("Tableau de bord")
    
    # Récupération des statistiques
    summary = analysis.get_campaign_summary()
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Contacts totaux", summary['total_contacts'])
        st.metric("En attente", summary['pending'])
    
    with col2:
        st.metric("Appels effectués", summary['total_calls'])
        st.metric("Complétés", summary['completed'])
    
    with col3:
        st.metric("Consentements", summary['consent_given'])
        st.metric("Taux", f"{summary['consent_rate']}%")
    
    with col4:
        st.metric("Identités confirmées", summary['identity_confirmed'])
        st.metric("Taux de succès", f"{summary['success_rate']}%")
    
    # Graphiques de répartition
    st.subheader("Répartition des résultats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Consentements**")
        consent_data = {
            'Acceptés': summary['consent_given'],
            'Refusés': summary['consent_refused']
        }
        st.bar_chart(consent_data)
    
    with col2:
        st.write("**Identités**")
        identity_data = {
            'Confirmées': summary['identity_confirmed'],
            'Rejetées': summary['identity_rejected'],
            'Pas de réponse': summary['no_response']
        }
        st.bar_chart(identity_data)
    
    # Résultats détaillés
    st.subheader("Résultats détaillés")
    results = analysis.get_detailed_results()
    
    if results:
        # Utiliser CsvHandler pour formater les colonnes avec les noms en français
        df = CsvHandler.export_results(results)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun résultat pour le moment")

# TAB 2: Campagne
with tab2:
    st.header("Gestion de campagne")
    
    # Import de contacts
    st.subheader("1. Importer des contacts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choisir un fichier CSV",
            type=['csv'],
            help="Le CSV doit contenir les colonnes : nom, prenom, telephone"
        )
        
        if uploaded_file is not None:
            try:
                contacts = CsvHandler.import_contacts(uploaded_file)
                st.success(f"✅ {len(contacts)} contacts importés")
                
                if st.button("Ajouter à la base"):
                    db.add_contacts(contacts)
                    st.success("Contacts ajoutés à la base de données")
                    st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de l'import : {str(e)}")
    
    with col2:
        st.write("**Format CSV requis:**")
        st.code("""nom,prenom,telephone
Dupont,Jean,+33612345678
Martin,Marie,+33687654321""")
        st.info("ℹ️ Les numéros doivent être au format international (+33...)")
        st.info("💡 Téléchargez `exemple_contacts.csv` pour un modèle")
    
    # Liste des contacts en attente
    st.subheader("2. Contacts en attente")
    
    pending_contacts = db.get_pending_contacts()
    
    if pending_contacts:
        st.write(f"**{len(pending_contacts)} contact(s) en attente**")
        st.dataframe(pending_contacts, use_container_width=True)
    else:
        st.info("Aucun contact en attente")
    
    # Lancement des appels
    st.subheader("3. Lancer les appels")
    
    if pending_contacts:
        if st.button("🚀 Lancer la campagne d'appels", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total = len(pending_contacts)
            
            for i, contact in enumerate(pending_contacts):
                status_text.text(f"Appel en cours : {contact['prenom']} {contact['nom']}...")
                
                try:
                    # Appel RÉEL avec Blend AI + OpenAI
                    logger.info(f"Début appel RÉEL pour {contact['prenom']} {contact['nom']} ({contact['telephone']})")
                    
                    # Construire le prompt de tâche
                    task_prompt = twilio_service.build_task_prompt(
                        nom=contact['nom'],
                        prenom=contact['prenom']
                    )
                    
                    # Initier l'appel via Blend
                    call_response = twilio_service.make_call(
                        to_number=contact['telephone'],
                        contact_id=contact['id'],
                        task_prompt=task_prompt,
                        first_sentence="Bonjour, je suis une assistante virtuelle de VoiceCheck AI.",
                        language="fr"
                    )
                    
                    if call_response.get('error'):
                        error_msg = f"Erreur Blend: {call_response.get('message')}"
                        logger.error(f"{error_msg} - Response: {call_response}")
                        st.error(error_msg)
                        st.error(f"Détails: Status {call_response.get('status_code')} - Voir logs/blend_api.log pour plus d'infos")
                        continue
                    
                    call_id = call_response.get('call_id') or call_response.get('id')
                    
                    # Attendre que l'appel se termine (polling)
                    status_text.text(f"⏳ Appel en cours avec {contact['prenom']} {contact['nom']}... (attente du transcript)")
                    
                    max_attempts = 60  # 60 tentatives = ~5 minutes max
                    attempt = 0
                    call_completed = False
                    transcript = ""
                    
                    while attempt < max_attempts and not call_completed:
                        time.sleep(5)  # Attendre 5 secondes entre chaque vérification
                        attempt += 1
                        
                        logger.info(f"⏳ Polling tentative {attempt}/{max_attempts} pour call_id: {call_id}")
                        
                        # Récupérer le statut de l'appel
                        call_status = twilio_service.fetch_call_result(call_id)
                        
                        if call_status.get('error'):
                            logger.error(f"❌ Erreur lors de la récupération du statut: {call_status.get('message')}")
                            break
                        
                        # Vérifier si l'appel est terminé
                        status = call_status.get('status', '').lower()
                        logger.debug(f"Status actuel: {status}")
                        
                        if status in ['completed', 'done', 'finished']:
                            call_completed = True
                            # Bland.ai utilise 'concatenated_transcript'
                            transcript = call_status.get('concatenated_transcript', '') or call_status.get('transcript', '') or call_status.get('transcription', '')
                            logger.info(f"✅ Appel terminé! Transcript récupéré (longueur: {len(transcript)} caractères)")
                            logger.debug(f"Transcript complet: {transcript[:500]}..." if len(transcript) > 500 else f"Transcript complet: {transcript}")
                            break
                    
                    if not call_completed:
                        logger.warning(f"⚠️ Timeout: Appel non terminé après {max_attempts} tentatives ({max_attempts * 5} secondes)")
                    
                    if not transcript:
                        logger.warning(f"⚠️ Aucun transcript disponible pour call_id: {call_id}")
                    
                    if not call_completed or not transcript:
                        # Pas de transcript disponible
                        logger.info(f"📝 Création du résultat avec no_response=True pour contact {contact['id']}")
                        result = {
                            'contact_id': contact['id'],
                            'nom': contact['nom'],
                            'prenom': contact['prenom'],
                            'telephone': contact['telephone'],
                            'call_sid': call_id,
                            'consent': None,
                            'identity_confirmed': None,
                            'no_response': True,
                            'transcription': ''
                        }
                    else:
                        # Analyser le transcript avec OpenAI
                        logger.info(f"🤖 Début de l'analyse OpenAI pour {contact['prenom']} {contact['nom']}")
                        status_text.text(f"🤖 Analyse du transcript avec OpenAI pour {contact['prenom']} {contact['nom']}...")
                        
                        try:
                            analysis_result = openai_service.analyze_consent_and_identity(
                                transcript=transcript,
                                nom=contact['nom'],
                                prenom=contact['prenom']
                            )
                            
                            logger.info(f"✅ Analyse OpenAI terminée: consent={analysis_result.get('consent')}, identity={analysis_result.get('identity_confirmed')}")
                            logger.debug(f"Reasoning: {analysis_result.get('reasoning', 'N/A')}")
                            
                            result = {
                                'contact_id': contact['id'],
                                'nom': contact['nom'],
                                'prenom': contact['prenom'],
                                'telephone': contact['telephone'],
                                'call_sid': call_id,
                                'consent': analysis_result.get('consent'),
                                'identity_confirmed': analysis_result.get('identity_confirmed'),
                                'no_response': False,
                                'transcription': transcript,
                                'reasoning': analysis_result.get('reasoning', '')
                            }
                        except Exception as e:
                            logger.error(f"❌ Erreur lors de l'analyse OpenAI: {str(e)}")
                            logger.exception(e)
                            result = {
                                'contact_id': contact['id'],
                                'nom': contact['nom'],
                                'prenom': contact['prenom'],
                                'telephone': contact['telephone'],
                                'call_sid': call_id,
                                'consent': None,
                                'identity_confirmed': None,
                                'no_response': True,
                                'transcription': transcript,
                                'error': str(e)
                            }
                    
                    # Sauvegarder le résultat
                    logger.info(f"💾 Sauvegarde du résultat pour contact {contact['id']}")
                    db.save_result(result)
                    
                    # Mettre à jour le statut du contact
                    if result.get('identity_confirmed') and result.get('consent'):
                        logger.info(f"✅ Contact {contact['id']} marqué comme 'completed' (consent + identity OK)")
                        db.update_contact_status(contact['id'], 'completed')
                    else:
                        logger.info(f"⏸️ Contact {contact['id']} reste en 'pending' (consent={result.get('consent')}, identity={result.get('identity_confirmed')})")
                        db.update_contact_status(contact['id'], 'pending')
                    
                    progress_bar.progress((i + 1) / total)
                    
                except Exception as e:
                    st.error(f"Erreur pour {contact['nom']} : {str(e)}")
            
            status_text.text("✅ Campagne terminée !")
            st.success(f"{total} appel(s) effectué(s)")
            time.sleep(2)
            st.rerun()
    else:
        st.warning("Aucun contact en attente. Importez des contacts d'abord.")
    
    # Relances manuelles
    st.subheader("4. Relances manuelles")
    
    to_recall = analysis.get_contacts_to_recall()
    
    if to_recall:
        st.write(f"**{len(to_recall)} contact(s) à rappeler**")
        st.dataframe(to_recall, use_container_width=True)
        
        if st.button("📞 Relancer ces contacts"):
            try:
                # Remettre les contacts en statut pending
                count = 0
                for contact in to_recall:
                    contact_id = contact.get('id')
                    if contact_id:
                        logger.info(f"🔄 Remise en file d'attente du contact {contact_id}: {contact.get('prenom')} {contact.get('nom')}")
                        db.update_contact_status(contact_id, 'pending')
                        count += 1
                    else:
                        logger.error(f"❌ Contact sans ID: {contact}")
                
                st.success(f"✅ {count} contact(s) remis en file d'attente")
                logger.info(f"✅ Relance terminée: {count} contacts remis en pending")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                logger.error(f"❌ Erreur lors de la relance: {str(e)}")
                st.error(f"Erreur: {str(e)}")
    else:
        st.info("Aucun contact à rappeler")

# TAB 3: Export
with tab3:
    st.header("Export des résultats")
    
    results = analysis.get_detailed_results()
    
    if results:
        st.write(f"**{len(results)} résultat(s) disponible(s)**")
        
        # Aperçu
        df = CsvHandler.export_results(results)
        st.dataframe(df, use_container_width=True)
        
        # Bouton de téléchargement
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name="voicecheck_results.csv",
            mime="text/csv"
        )
    else:
        st.info("Aucun résultat à exporter")

# Footer
st.divider()
st.caption("VoiceCheck AI - Hackathon 2024 - Vérification automatisée des contacts")
