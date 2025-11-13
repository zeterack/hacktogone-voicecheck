#!/bin/bash
# Script pour suivre les logs en temps réel et faciliter le débogage

echo "🔍 VoiceCheck AI - Suivi des logs Blend AI"
echo "=========================================="
echo ""
echo "Mode d'emploi:"
echo "1. Laissez ce terminal ouvert"
echo "2. Dans un autre terminal, lancez: streamlit run app.py"
echo "3. Effectuez un appel dans l'interface"
echo "4. Les logs s'afficheront ici en temps réel"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""
echo "Logs en cours..."
echo "=========================================="
echo ""

# Créer le dossier logs s'il n'existe pas
mkdir -p logs

# Suivre le fichier de log
tail -f logs/blend_api.log
