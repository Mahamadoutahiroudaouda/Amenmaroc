# run_project_01.py
"""
Script pour lancer le Projet #1: ANEM en Lumière
"""

import sys
import os
import io

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter le dossier src au path Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importer la fonction de démo
from demo_all_projects import run_project_01_full

if __name__ == "__main__":
    print("=" * 60)
    print("PROJET #1: ANEM EN LUMIERE")
    print("Naissance d'une Nation - Spectacle Cinematique 3D")
    print("=" * 60)
    print()
    
    # Lancer le projet
    run_project_01_full()

