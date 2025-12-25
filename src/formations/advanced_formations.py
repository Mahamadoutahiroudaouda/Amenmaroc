# src/formations/advanced_formations.py
"""
FORMATIONS AVANCÉES
"""

import numpy as np
from formations.base_formations import BaseFormations

class AdvancedFormations(BaseFormations):
    """Formations géométriques avancées et complexes."""
    
    def polygon(self, n_sides=3, radius=0.8, rotation=0):
        """Polygone régulier (triangle, carré, pentagone...)."""
        angles = np.linspace(0 + rotation, 2*np.pi + rotation, n_sides, endpoint=False)
        vertices_x = radius * np.cos(angles)
        vertices_y = radius * np.sin(angles)
        
        # Interpoler les robots le long des côtés
        positions = []
        robots_per_side = self.n // n_sides
        remaining = self.n % n_sides
        
        for i in range(n_sides):
            start_x, start_y = vertices_x[i], vertices_y[i]
            end_x, end_y = vertices_x[(i+1)%n_sides], vertices_y[(i+1)%n_sides]
            
            n_robots = robots_per_side + (1 if i < remaining else 0)
            
            x_line = np.linspace(start_x, end_x, n_robots, endpoint=False)
            y_line = np.linspace(start_y, end_y, n_robots, endpoint=False)
            
            positions.extend(zip(x_line, y_line))
            
        return np.array(positions[:self.n]).T

    def dna_helix(self, turns=2):
        """Double hélice d'ADN projetée en 2D."""
        t = np.linspace(0, turns * 2*np.pi, self.n)
        
        # Strand 1
        x1 = np.linspace(-1.0, 1.0, self.n)
        y1 = 0.5 * np.sin(t)
        
        # Pour une double hélice, on divise les robots en 2 groupes ?
        # Ou on fait juste une sinusoïde pour l'instant
        
        positions = np.array([x1, y1])
        return positions

    def lissajous(self, a=3, b=2, delta=np.pi/2):
        """Courbe de Lissajous."""
        t = np.linspace(0, 2*np.pi, self.n)
        x = 0.8 * np.sin(a * t + delta)
        y = 0.8 * np.sin(b * t)
        return np.array([x, y])

    def heart(self):
        """Forme de coeur."""
        t = np.linspace(0, 2*np.pi, self.n)
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        
        # Normaliser
        x = x / 20.0
        y = y / 20.0
        
        return np.array([x, y])
