# src/animations/transition_manager.py
"""
GESTIONNAIRE DE TRANSITIONS - VERSION COMPLÈTE
"""

import numpy as np

class TransitionManager:
    """Gère les transitions fluides entre différentes formations."""
    
    def __init__(self):
        self.transition_functions = {
            'linear': self._linear,
            'ease_in_out': self._ease_in_out,
            'bounce': self._bounce,
            'elastic': self._elastic
        }
    
    def _linear(self, t):
        """Transition linéaire simple."""
        return t
    
    def _ease_in_out(self, t):
        """Transition avec accélération/décélération (courbe en S)."""
        return t * t * (3 - 2 * t)
    
    def _bounce(self, t):
        """Transition avec effet de rebond."""
        if t < 0.5:
            return 4 * t * t
        else:
            return 1 - 4 * (t - 1) * (t - 1)
    
    def _elastic(self, t):
        """Transition élastique (oscillation amortie)."""
        if t == 0 or t == 1:
            return t
        return np.sin(13 * np.pi / 2 * t) * np.power(2, -10 * t)
    
    def interpolate_positions(self, start_pos, end_pos, duration, 
                            transition_type='ease_in_out', fps=30):
        """
        Génère des positions intermédiaires pour une transition fluide.
        """
        steps = int(duration * fps)
        transition_func = self.transition_functions[transition_type]
        
        for step in range(steps):
            t = step / steps
            progress = transition_func(t)
            
            # Interpolation linéaire des positions
            current_pos = start_pos + (end_pos - start_pos) * progress
            yield current_pos