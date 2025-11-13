#!/usr/bin/env python3
"""
Script pour afficher les logs de Blend AI en temps réel
Usage: python view_logs.py [--tail] [--errors-only]
"""

import sys
import time
import os

def view_logs(tail=False, errors_only=False):
    log_file = 'logs/blend_api.log'
    
    if not os.path.exists(log_file):
        print(f"❌ Fichier {log_file} introuvable")
        print("Lancez d'abord l'application pour générer des logs.")
        return
    
    if tail:
        # Mode tail -f
        print(f"📄 Suivi des logs en temps réel ({log_file})")
        print("=" * 80)
        
        with open(log_file, 'r') as f:
            # Aller à la fin du fichier
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    if errors_only:
                        if 'ERROR' in line or 'ERREUR' in line or '❌' in line:
                            print(line.strip())
                    else:
                        print(line.strip())
                else:
                    time.sleep(0.1)
    else:
        # Affichage complet
        print(f"📄 Contenu du fichier {log_file}")
        print("=" * 80)
        
        with open(log_file, 'r') as f:
            for line in f:
                if errors_only:
                    if 'ERROR' in line or 'ERREUR' in line or '❌' in line:
                        print(line.strip())
                else:
                    print(line.strip())

def show_last_error():
    """Affiche la dernière erreur détaillée"""
    log_file = 'logs/blend_api.log'
    
    if not os.path.exists(log_file):
        print(f"❌ Fichier {log_file} introuvable")
        return
    
    print("🔍 Dernière erreur détectée:")
    print("=" * 80)
    
    lines = []
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Chercher la dernière erreur
    error_block = []
    in_error = False
    
    for i, line in enumerate(lines):
        if '❌' in line or 'ERROR' in line:
            in_error = True
            error_block = [line]
        elif in_error:
            if line.strip() and not line.startswith('2'):  # Continuer si ce n'est pas un timestamp
                error_block.append(line)
            else:
                in_error = False
    
    if error_block:
        for line in error_block:
            print(line.strip())
    else:
        print("Aucune erreur trouvée dans les logs")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualiseur de logs Blend AI')
    parser.add_argument('--tail', '-t', action='store_true', help='Suivre les logs en temps réel')
    parser.add_argument('--errors-only', '-e', action='store_true', help='Afficher uniquement les erreurs')
    parser.add_argument('--last-error', '-l', action='store_true', help='Afficher la dernière erreur')
    
    args = parser.parse_args()
    
    if args.last_error:
        show_last_error()
    else:
        try:
            view_logs(tail=args.tail, errors_only=args.errors_only)
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt du suivi des logs")
