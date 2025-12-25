# src/animations/motion_animations.py
"""
ANIMATIONS DE MOUVEMENT
"""

import numpy as np

class MotionAnimator:
    """Gestionnaire de mouvements dynamiques."""
    
    def __init__(self):
        pass
        
    def wave(self, positions, time_val, amplitude=0.1, frequency=1.0, direction='x'):
        """Applique une ondulation aux positions."""
        new_pos = positions.copy()
        
        if direction == 'x':
            # Ondulation verticale basée sur x
            offset = amplitude * np.sin(2 * np.pi * frequency * time_val + positions[0])
            new_pos[1] += offset
        else:
            # Ondulation horizontale basée sur y
            offset = amplitude * np.sin(2 * np.pi * frequency * time_val + positions[1])
            new_pos[0] += offset
            
        return new_pos

    def jitter(self, positions, magnitude=0.01):
        """Ajoute un bruit aléatoire (tremblement)."""
        noise = np.random.uniform(-magnitude, magnitude, positions.shape)
        return positions + noise
    
    def rotate(self, positions, angle, center=(0, 0)):
        """Bascule les positions d'un angle donné autour d'un centre."""
        rx = positions[0] - center[0]
        ry = positions[1] - center[1]
        
        new_x = rx * np.cos(angle) - ry * np.sin(angle)
        new_y = rx * np.sin(angle) + ry * np.cos(angle)
        
        return np.array([new_x + center[0], new_y + center[1]])
