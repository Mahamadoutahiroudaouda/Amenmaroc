# src/formations/base_formations.py
"""
FORMATIONS GÉOMÉTRIQUES DE BASE - VERSION COMPLÈTE
"""

import numpy as np
from utils.config import config

class BaseFormations:
    """Bibliothèque de formations géométriques fondamentales."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.zone = config.safe_zone
    
    def grid(self, rows=5, cols=10):
        """Grille rectangulaire parfaite."""
        x = np.linspace(self.zone['x_min'], self.zone['x_max'], cols)
        y = np.linspace(self.zone['y_min'], self.zone['y_max'], rows)
        xx, yy = np.meshgrid(x, y)
        
        positions = np.array([xx.flatten(), yy.flatten()])
        return positions[:, :self.n]
    
    def circle(self, radius=0.7, center=(0, 0)):
        """Cercle parfait."""
        angles = np.linspace(0, 2*np.pi, self.n, endpoint=False)
        x = center[0] + radius * np.cos(angles)
        y = center[1] + radius * np.sin(angles)
        return np.array([x, y])
    
    def spiral(self, a=0.1, b=0.3, turns=3):
        """Spirale logarithmique."""
        theta = np.linspace(0, turns * 2*np.pi, self.n)
        r = a * np.exp(b * theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([x, y])
    
    def random_positions(self):
        """Positions aléatoires dans la zone sûre."""
        x = np.random.uniform(self.zone['x_min'], self.zone['x_max'], self.n)
        y = np.random.uniform(self.zone['y_min'], self.zone['y_max'], self.n)
        return np.array([x, y])
    
    def line(self, start=(-1.0, 0), end=(1.0, 0)):
        """Ligne droite entre deux points."""
        x = np.linspace(start[0], end[0], self.n)
        y = np.linspace(start[1], end[1], self.n)
        return np.array([x, y])
    
    def star(self, n_points=5, outer_radius=0.8, inner_radius=0.4):
        """Étoile à n branches."""
        angles = np.linspace(0, 2*np.pi, 2*n_points, endpoint=False)
        radii = [outer_radius if i % 2 == 0 else inner_radius for i in range(2*n_points)]
        
        positions = []
        robots_per_segment = max(1, self.n // (2 * n_points))
        
        for i in range(2 * n_points):
            next_i = (i + 1) % (2 * n_points)
            
            segment_x = np.linspace(
                radii[i] * np.cos(angles[i]),
                radii[next_i] * np.cos(angles[next_i]),
                robots_per_segment,
                endpoint=False
            )
            segment_y = np.linspace(
                radii[i] * np.sin(angles[i]),
                radii[next_i] * np.sin(angles[next_i]),
                robots_per_segment,
                endpoint=False
            )
            positions.extend(zip(segment_x, segment_y))
        
        positions = np.array(positions[:self.n]).T
        return positions