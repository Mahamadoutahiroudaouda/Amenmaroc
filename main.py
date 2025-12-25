# robotarium_anem_2025/main.py
"""
POINT D'ENTRÉE PRINCIPAL - TEST RAPIDE
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Ajouter le dossier src au path Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_simple():
    """Test simple sans les imports complexes."""
    print("[TEST] TEST SIMPLE DU SYSTEME")
    
    # Configuration basique
    N_ROBOTS = 50
    FPS = 30
    
    # Créer une figure
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.0, 1.0)
    ax.set_facecolor('black')
    ax.set_title("ANEM 2025 - TEST SIMPLE", color='white', fontsize=16)
    
    # Couleurs ANEM
    colors = {
        'orange': '#E05206',
        'vert': '#0DB02B', 
        'blanc': '#FFFFFF'
    }
    
    # Test 1: Points aléatoires
    print("[TEST] Test 1: Points aleatoires")
    for i in range(100):  # 100 frames
        x = np.random.uniform(-1.4, 1.4, N_ROBOTS)
        y = np.random.uniform(-0.85, 0.85, N_ROBOTS)
        
        ax.clear()
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.0, 1.0)
        ax.set_facecolor('black')
        
        ax.scatter(x, y, c=colors['orange'], s=80, alpha=0.8)
        ax.set_title(f"ANEM 2025 - Frame {i}", color='white')
        
        plt.pause(0.01)
    
    print("[OK] Test reussi !")
    plt.show()

if __name__ == "__main__":
    test_simple()