# src/formations/cultural_formations.py
"""
FORMATIONS CULTURELLES DU NIGER
"""

import numpy as np
from formations.base_formations import BaseFormations

class CulturalFormations(BaseFormations):
    """Formations spécifiques à la culture du Niger."""
    
    def cross_agadez(self):
        """Croix d'Agadez simplifiée."""
        positions = np.zeros((2, self.n))
        
        # Centre
        center_robots = min(4, self.n)
        angles = np.linspace(0, 2*np.pi, center_robots, endpoint=False)
        positions[0, :center_robots] = 0.1 * np.cos(angles)
        positions[1, :center_robots] = 0.1 * np.sin(angles)
        
        # 4 branches principales
        remaining = self.n - center_robots
        if remaining > 0:
            robots_per_arm = remaining // 4
            
            for i in range(4):
                angle = i * np.pi / 2
                start_idx = center_robots + i * robots_per_arm
                end_idx = start_idx + robots_per_arm
                
                # Ligne vers l'extérieur
                r = np.linspace(0.15, 0.6, robots_per_arm)
                positions[0, start_idx:end_idx] = r * np.cos(angle)
                positions[1, start_idx:end_idx] = r * np.sin(angle)
                
        return positions

    def zebu_horns(self):
        """Cornes de Zébu (symbole d'élevage)."""
        positions = np.zeros((2, self.n))
        mid = self.n // 2
        
        # Corne gauche
        t = np.linspace(0, 1, mid)
        x_left = -0.2 - 0.5 * t
        y_left = 0.5 * t**2 + 0.2 * t
        positions[0, :mid] = x_left
        positions[1, :mid] = y_left
        
        # Corne droite
        remaining = self.n - mid
        t2 = np.linspace(0, 1, remaining)
        x_right = 0.2 + 0.5 * t2
        y_right = 0.5 * t2**2 + 0.2 * t2
        positions[0, mid:] = x_right
        positions[1, mid:] = y_right
        
        return positions
