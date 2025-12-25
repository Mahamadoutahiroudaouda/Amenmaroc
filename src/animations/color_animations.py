# src/animations/color_animations.py
"""
SYSTÈME D'ANIMATION DES COULEURS - VERSION COMPLÈTE
Includes light effects for Project 1 ceremony
"""

import numpy as np
import colorsys
from utils.config import config

class ColorAnimator:
    """Gère les animations de couleurs avec effets lumineux artistiques."""
    
    def __init__(self):
        self.colors = config.COLORS
        # Couleurs drapeau Niger en ordre
        self.drapeau_colors = [
            self.colors['orange_niger'],
            self.colors['blanc_pure'], 
            self.colors['vert_espoir']
        ]
    
    def hex_to_rgb(self, hex_color):
        """Convertit une couleur hex en RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r, g, b):
        """Convertit RGB en hex."""
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    # ========== LIGHT EFFECTS ==========
    
    def blackout_effect(self, base_color, progress):
        """Fade to black effect (progress 0->1)."""
        r, g, b = self.hex_to_rgb(base_color)
        factor = 1.0 - progress
        return self.rgb_to_hex(int(r * factor), int(g * factor), int(b * factor))
    
    def progressive_lightup(self, base_color, progress):
        """Fade from black effect (progress 0->1)."""
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * progress), int(g * progress), int(b * progress))
    
    def sweep_effect(self, base_color, robot_index, total_robots, sweep_progress):
        """Horizontal sweep effect."""
        position_ratio = robot_index / max(1, total_robots - 1)
        if abs(position_ratio - sweep_progress) < 0.2:
            # Bright area following sweep
            intensity = 1.2
        else:
            intensity = 0.7
        
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * intensity), int(g * intensity), int(b * intensity))
    
    def pulsation_effect(self, base_color, time_val, frequency=0.5):
        """Breathing pulsation effect."""
        pulse = 0.7 + 0.3 * np.sin(2 * np.pi * frequency * time_val)
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * pulse), int(g * pulse), int(b * pulse))
    
    def intensity_buildup(self, base_color, progress):
        """Progressive intensity crescendo (progress 0->1)."""
        intensity = 0.3 + 0.7 * progress
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * intensity), int(g * intensity), int(b * intensity))
    
    def breathing_light(self, base_color, time_val):
        """Subtle breathing effect for text."""
        breath = 0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * time_val)
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * breath), int(g * breath), int(b * breath))
    
    # ========== FLAG RAIN COLORS ==========
    
    def get_pluie_drapeau_color(self, positions, robot_index, time_val):
        """Colors for flag rain - strict separation by lines."""
        if robot_index >= positions.shape[1]:
            return self.colors['orange_niger']
        
        y_pos = positions[1, robot_index]
        
        # Determine band based on Y position
        if y_pos > 0.3:
            return self.colors['orange_niger']  # Top: Orange
        elif y_pos > -0.3:
            return self.colors['blanc_pure']     # Middle: White
        else:
            return self.colors['vert_espoir']    # Bottom: Green
    
    # ========== FLOATING FLAG COLORS ==========
    
    def get_drapeau_flottant_color(self, positions, robot_index, time_val):
        """Colors for floating flag with wave effect."""
        if robot_index >= positions.shape[1]:
            return self.colors['orange_niger']
        
        y_pos = positions[1, robot_index]
        x_pos = positions[0, robot_index]
        
        # Determine band based on Y position
        if y_pos > 0.25:
            base_color = self.colors['orange_niger']
        elif y_pos > -0.25:
            base_color = self.colors['blanc_pure']
            # Add sun detection for white band center
            if abs(x_pos) < 0.15 and abs(y_pos) < 0.15:
                base_color = self.colors['or_soleil']  # Sun in center
        else:
            base_color = self.colors['vert_espoir']
        
        # Add fabric shimmer effect
        shimmer = 0.9 + 0.1 * np.sin(2 * np.pi * 0.5 * time_val + x_pos * 3)
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * shimmer), int(g * shimmer), int(b * shimmer))
    
    # ========== TEXT FORMATION COLORS ==========
    
    def get_text_color(self, phase_name, time_val, effect_type='gold'):
        """Colors for text formations with various effects."""
        if effect_type == 'gold':
            base_color = self.colors['or_soleil']
        elif effect_type == 'orange':
            base_color = self.colors['orange_niger']
        elif effect_type == 'white':
            base_color = self.colors['blanc_pure']
        else:
            base_color = self.colors['or_soleil']
        
        # Default: breathing effect
        return self.breathing_light(base_color, time_val)
    
    # ========== OTHER PROJECT COLORS ==========
    
    def get_carte_color(self, robot_index, time_val):
        """Color for Niger map."""
        # Alternate between flag colors for different regions
        region = robot_index % 3
        base_color = self.drapeau_colors[region]
        
        # Subtle variation
        variation = 0.9 + 0.1 * np.sin(2 * np.pi * 0.2 * time_val + robot_index * 0.05)
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * variation), int(g * variation), int(b * variation))
    
    def get_finale_color(self, robot_index, time_val):
        """Dynamic rainbow for finale."""
        hue = (time_val * 0.5 + robot_index * 0.01) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
        return self.rgb_to_hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    
    # ========== MAIN COLOR DISPATCHER ==========
    
    def get_tempête_color(self, robot_index, time_val):
        """Couleurs pour la tempête de sable (Orange terreux avec variations)."""
        # Mélange de orange Niger et de terre d'Agadez
        r1, g1, b1 = self.hex_to_rgb(self.colors['orange_niger'])
        r2, g2, b2 = self.hex_to_rgb(self.colors['terre_agadez'])
        
        # Variation aléatoire par drone et par temps
        mix = 0.5 + 0.5 * np.sin(time_val * 2 + robot_index * 0.1)
        r = int(r1 * mix + r2 * (1 - mix))
        g = int(g1 * mix + g2 * (1 - mix))
        b = int(b1 * mix + b2 * (1 - mix))
        
        # Effet de poussière (plus ou moins sombre)
        brilliance = 0.7 + 0.3 * np.random.rand()
        return self.rgb_to_hex(int(r * brilliance), int(g * brilliance), int(b * brilliance))

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """
        Main color dispatcher for all phases - VERSION CINÉMA 3D.
        """
        if positions is None or robot_index is None:
            return self.colors['orange_niger']
        
        if robot_index >= positions.shape[1]:
            return self.colors['orange_niger']
        
        phase_lower = phase_name.lower()
        
        # TABLEAU #1: NAISSANCE D'UNE NATION (CINÉMA)
        if "tempête" in phase_lower:
            return self.get_tempête_color(robot_index, time_val)
        
        elif "vert" in phase_lower:
            # Émergence progressive du vert
            return self.colors['vert_espoir']
            
        elif "blanc" in phase_lower:
            # Apparition du blanc
            return self.colors['blanc_pure']
            
        elif "soleil" in phase_lower:
            # Soleil qui pulse
            return self.pulsation_effect(self.colors['or_soleil'], time_val, frequency=1.0)
            
        elif "ondulant" in phase_lower or "flottant" in phase_lower:
            return self.get_drapeau_flottant_color(positions, robot_index, time_val)
            
        elif "niger" in phase_lower:
            # NIGER 3D - Or brillant
            return self.breathing_light(self.colors['or_soleil'], time_val)
        
        # PROJETS GÉNÉRIQUES (COMPATIBILITÉ)
        elif "pluie" in phase_lower and "drapeau" in phase_lower:
            return self.get_pluie_drapeau_color(positions, robot_index, time_val)
        
        elif any(text in phase_lower for text in ['anem', 'jcn', 'edition', 'fes', 'meknes']):
            return self.get_text_color(phase_name, time_val, 'gold')
        
        elif "carte" in phase_lower:
            return self.get_carte_color(robot_index, time_val)
        
        elif "finale" in phase_lower or "etoile" in phase_lower:
            return self.get_finale_color(robot_index, time_val)
        
        # Default: orange
        return self.colors['orange_niger']
    
    # ========== HELPER METHODS FOR OTHER PROJECTS ==========
    
    def _get_wave_color(self, positions, robot_index, time_val):
        """Wave color gradient."""
        y_pos = positions[1, robot_index]
        y_range = positions[1, :].max() - positions[1, :].min()
        if y_range > 0:
            amplitude = (y_pos - positions[1, :].min()) / y_range
        else:
            amplitude = 0.5
        
        if amplitude < 0.3:
            return self.colors['bleu_profond']
        elif amplitude < 0.6:
            return self.colors['turquoise']
        else:
            return self.colors['ciel_bleu']
    
    def _get_firework_color(self, robot_index, time_val):
        """Firework colors."""
        color_idx = (robot_index // 50) % 3
        return self.drapeau_colors[color_idx]
    
    def _get_fibonacci_color(self, positions, robot_index, time_val):
        """Fibonacci spiral color."""
        x, y = positions[0, robot_index], positions[1, robot_index]
        distance = np.sqrt(x**2 + y**2)
        
        colors_gold = ['#FFD700', '#D4AF37', '#B08D57', '#CD7F32']
        color_index = min(int(distance * 2), len(colors_gold)-1)
        base_color = colors_gold[color_index]
        
        brilliance = 0.8 + 0.2 * np.sin(2*np.pi*0.3*time_val)
        r, g, b = self.hex_to_rgb(base_color)
        return self.rgb_to_hex(int(r * brilliance), int(g * brilliance), int(b * brilliance))
    
    def _get_faune_color(self, phase_name, robot_index, time_val):
        """Fauna colors."""
        colors_animaux = {
            'girafe': '#D4AF37',
            'elephant': '#A9A9A9',
            'addax': '#F5F5DC',
            'dromadaire': '#F4A460'
        }
        
        for animal, color in colors_animaux.items():
            if animal in phase_name.lower():
                return color
        
        return self.colors['terre_agadez']
    
    def _get_parade_color(self, robot_index, time_val):
        """Parade dynamic colors."""
        hue = (time_val * 0.3 + robot_index * 0.02) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
        return self.rgb_to_hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))