# src/animations/color_animations.py
"""
SYSTÈME D'ANIMATION DES COULEURS - FOCUS DRAPEAU NIGER
"""

import numpy as np
import colorsys
from utils.config import config

class ColorAnimator:
    """Gère les animations de couleurs avec focus drapeau Niger."""
    
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
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    # src/animations/color_animations.py
# CORRIGEZ LA MÉTHODE get_drapeau_color
# Dans src/animations/color_animations.py - AJOUTER LA GESTION DES VAGUES
    def get_vague_color(self, robot_index, total_robots, time_val, amplitude):
        """Retourne la couleur pour les vagues selon l'amplitude."""
        # Gradient bleu selon l'amplitude
        if amplitude < 0.2:
            return self.colors['bleu_profond']      # Bleu marine profond
        elif amplitude < 0.4:
            return self.colors['bleu_profond']      # Bleu océan
        elif amplitude < 0.6:
            return self.colors['turquoise']         # Turquoise
        elif amplitude < 0.8:
            return self.colors['ciel_bleu']         # Cyan
        else:
            return self.colors['blanc_pure']        # Écume blanche

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - AVEC VAGUES."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            return self.colors['bleu_profond']
        
        # GESTION DES VAGUES
        if "vague" in phase_name.lower() or "ocean" in phase_name.lower() or "tempete" in phase_name.lower() or "tsunami" in phase_name.lower():
            # Calculer l'amplitude locale pour ce robot
            if robot_index < positions.shape[1]:
                y_pos = positions[1, robot_index]
                # Amplitude relative (normalisée)
                amplitude = (y_pos - positions[1, :].min()) / (positions[1, :].max() - positions[1, :].min() + 1e-8)
                return self.get_vague_color(robot_index, total_robots, time_val, amplitude)
            return self.colors['bleu_profond']
        
        # ... reste du code existant pour les autres phases ...
    # Dans src/animations/color_animations.py - AJOUTER LA GESTION DES FEUX D'ARTIFICE
    def get_firework_color(self, robot_index, time_val, phase_name):
        """Retourne la couleur pour les feux d'artifice."""
        # Couleurs du drapeau nigérien pour les feux d'artifice
        colors_drapeau = [self.colors['orange_niger'], self.colors['blanc_pure'], self.colors['vert_espoir']]
        
        if "lancement" in phase_name.lower():
            return self.colors['blanc_pure']  # Fusées blanches
        
        elif "explosion" in phase_name.lower():
            # Alternance orange/blanc/vert
            color_idx = (robot_index // (self.n // 3)) % 3
            return colors_drapeau[color_idx]
        
        elif "pluie" in phase_name.lower():
            # Dégradé selon la position
            return self.gradient_effect(colors_drapeau, time_val + robot_index*0.1, 3)
        
        elif "multiple" in phase_name.lower():
            # Arc-en-ciel pour les feux multiples
            hue = (time_val * 2 + robot_index * 0.01) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            return self.rgb_to_hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        
        elif "finale" in phase_name.lower():
            # Blanc éclatant pour la finale
            pulse = 0.7 + 0.3 * np.sin(2*np.pi*5*time_val)
            r, g, b = self.hex_to_rgb(self.colors['blanc_pure'])
            r = int(r * pulse)
            g = int(g * pulse)
            b = int(b * pulse)
            return self.rgb_to_hex(r, g, b)
        
        return self.colors['or_soleil']

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - AVEC FEUX D'ARTIFICE."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            return self.colors['blanc_pure']
        
        # GESTION DES FEUX D'ARTIFICE
        if any(firework in phase_name.lower() for firework in ['feu', 'artifice', 'fusee', 'explosion', 'pluie', 'finale']):
            return self.get_firework_color(robot_index, time_val, phase_name)
    # Dans src/animations/color_animations.py - AJOUTER LA GESTION FIBONACCI
    def get_fibonacci_color(self, robot_index, time_val, distance_from_center):
        """Retourne la couleur pour la spirale Fibonacci."""
        # Dégradé or → cuivre → bronze
        colors_gold = [self.colors['or_soleil'], '#D4AF37', '#B08D57', '#CD7F32']
        
        # Couleur basée sur la distance du centre
        color_index = min(int(distance_from_center * len(colors_gold)), len(colors_gold)-1)
        base_color = colors_gold[color_index]
        
        # Effet de brillance
        brilliance = 0.8 + 0.2 * np.sin(2*np.pi*0.3*time_val + robot_index*0.1)
        r, g, b = self.hex_to_rgb(base_color)
        
        r = int(r * brilliance)
        g = int(g * brilliance)
        b = int(b * brilliance)
        
        return self.rgb_to_hex(r, g, b)

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - AVEC FIBONACCI."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            return self.colors['or_soleil']
        
        # GESTION FIBONACCI
        if any(math_term in phase_name.lower() for math_term in ['fibonacci', 'spirale', 'dor', 'golden', 'rotation', 'pulsation', 'transformation']):
            if robot_index < positions.shape[1]:
                # Calculer la distance du centre
                x, y = positions[0, robot_index], positions[1, robot_index]
                distance = np.sqrt(x**2 + y**2)
                return self.get_fibonacci_color(robot_index, time_val, distance)
            return self.colors['or_soleil']
        
        # ... reste du code existant ...
    # AJOUT DANS src/animations/color_animations.py

    def get_faune_color(self, animal_type, robot_index, time_val):
        """Retourne la couleur appropriée pour chaque animal."""
        colors_animaux = {
            'girafe': ['#D4AF37', '#B08D57', '#8B6914'],  # Jaune ocre → brun
            'elephant': ['#A9A9A9', '#696969', '#808080'],  # Gris cendré
            'addax': ['#F5F5DC', '#DEB887', '#F0E68C'],  # Blanc crème → beige
            'dromadaire': ['#F4A460', '#D2B48C', '#CD853F']  # Beige sable
        }
        
        base_colors = colors_animaux.get(animal_type, ['#FFFFFF'])
        color_index = robot_index % len(base_colors)
        base_color = base_colors[color_index]
        
        # Effet de vie
        vitality = 0.9 + 0.1 * np.sin(2*np.pi*0.2*time_val + robot_index*0.05)
        r, g, b = self.hex_to_rgb(base_color)
        
        r = int(r * vitality)
        g = int(g * vitality)
        b = int(b * vitality)
        
        return self.rgb_to_hex(r, g, b)

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - AVEC FAUNE."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            return self.colors['or_soleil']
        
        # GESTION FAUNE DU NIGER
        if any(animal in phase_name.lower() for animal in ['girafe', 'elephant', 'addax', 'dromadaire']):
            animal_type = None
            if 'girafe' in phase_name.lower():
                animal_type = 'girafe'
            elif 'elephant' in phase_name.lower():
                animal_type = 'elephant'
            elif 'addax' in phase_name.lower():
                animal_type = 'addax'
            elif 'dromadaire' in phase_name.lower():
                animal_type = 'dromadaire'
            
            if animal_type:
                return self.get_faune_color(animal_type, robot_index, time_val)
        
        # ... reste du code existant pour Fibonacci ...    
        # ... reste du code existant ...
    # AJOUT DANS src/animations/color_animations.py
    # AJOUT DANS src/animations/color_animations.py

    def get_architecture_color(self, robot_index, time_val, building_type):
        """Retourne la couleur appropriée pour chaque type d'architecture."""
        colors_architecture = {
            'case': ['#A0522D', '#8B4513', '#D2691E'],      # Terre d'adobe
            'mosquee': ['#CD853F', '#D2B48C', '#F4A460'],   # Ocre rouge
            'palais': ['#8B7355', '#A0522D', '#DEB887'],    # Pierre et bois
            'village': ['#D2B48C', '#BC8F8F', '#F5DEB3']    # Terre battue
        }
        
        base_colors = colors_architecture.get(building_type, ['#A0522D'])
        color_index = robot_index % len(base_colors)
        base_color = base_colors[color_index]
        
        # Effet de texture naturelle
        texture = 0.85 + 0.15 * np.sin(2*np.pi*0.1*time_val + robot_index*0.1)
        r, g, b = self.hex_to_rgb(base_color)
        
        r = int(r * texture)
        g = int(g * texture)
        b = int(b * texture)
        
        return self.rgb_to_hex(r, g, b)

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - AVEC ARCHITECTURE."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            return self.colors['or_soleil']
        
        # GESTION PATRIMOINE ARCHITECTURAL
        if any(arch_term in phase_name.lower() for arch_term in 
               ['case', 'mosquee', 'sultanat', 'village', 'architectural']):
            
            building_type = 'case'  # défaut
            if 'case' in phase_name.lower():
                building_type = 'case'
            elif 'mosquee' in phase_name.lower():
                building_type = 'mosquee'
            elif 'sultanat' in phase_name.lower():
                building_type = 'palais'
            elif 'village' in phase_name.lower():
                building_type = 'village'
            
            return self.get_architecture_color(robot_index, time_val, building_type)
        
        # ... reste du code existant ...

    def get_parade_color(self, robot_index, time_val, tableau_name):
        """Retourne la couleur appropriée pour chaque tableau de la parade."""
        colors_parade = {
            'militaire': ['#2C3E50', '#34495E', '#7F8C8D'],  # Gris militaire
            'tempete': ['#D35400', '#E67E22', '#F39C12'],    # Orange sable
            'vagues': ['#1B4F72', '#2874A6', '#3498DB'],     # Bleu océan
            'spirale': ['#6C3483', '#8E44AD', '#AF7AC5'],    # Violet hypnotique
            'artifice': ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF'],  # Arc-en-ciel
            'geometrique': ['#27AE60', '#2ECC71', '#58D68D'], # Vert géométrique
            'coeur': ['#E74C3C', '#EC7063', '#F1948A']       # Rouge cœur
        }
        
        # Identifier le tableau
        tableau_key = 'militaire'  # défaut
        if 'militaire' in tableau_name.lower():
            tableau_key = 'militaire'
        elif 'tempete' in tableau_name.lower():
            tableau_key = 'tempete'
        elif 'vagues' in tableau_name.lower():
            tableau_key = 'vagues'
        elif 'spirale' in tableau_name.lower():
            tableau_key = 'spirale'
        elif 'artifice' in tableau_name.lower():
            tableau_key = 'artifice'
        elif 'geometrique' in tableau_name.lower():
            tableau_key = 'geometrique'
        elif 'coeur' in tableau_name.lower():
            tableau_key = 'coeur'
        
        base_colors = colors_parade.get(tableau_key, ['#FFFFFF'])
        color_index = robot_index % len(base_colors)
        base_color = base_colors[color_index]
        
        # Effets spéciaux selon le tableau
        if tableau_key == 'artifice':
            # Couleurs changeantes pour les feux d'artifice
            hue = (time_val * 0.5 + robot_index * 0.1) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            return self.rgb_to_hex(*[int(c*255) for c in rgb])
        elif tableau_key == 'spirale':
            # Effet psychédélique
            hue = (time_val * 0.3 + robot_index * 0.02) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            return self.rgb_to_hex(*[int(c*255) for c in rgb])
        elif tableau_key == 'coeur':
            # Pulsation rouge
            pulse = 0.8 + 0.2 * np.sin(2*np.pi*0.8*time_val)
            r, g, b = self.hex_to_rgb(base_color)
            r = int(r * pulse)
            return self.rgb_to_hex(r, g, b)
        else:
            # Couleur de base avec légère variation
            variation = 0.9 + 0.1 * np.sin(2*np.pi*0.2*time_val + robot_index*0.05)
            r, g, b = self.hex_to_rgb(base_color)
            r = int(r * variation)
            g = int(g * variation)
            b = int(b * variation)
            return self.rgb_to_hex(r, g, b)

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - AVEC PARADE."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            return self.colors['or_soleil']
        
        # GESTION GRANDE PARADE
        if any(parade_term in phase_name.lower() for parade_term in 
               ['militaire', 'tempete', 'vagues', 'spirale', 'artifice', 'geometrique', 'coeur', 'parade']):
            return self.get_parade_color(robot_index, time_val, phase_name)
        
        # ... reste du code existant ...
    def get_drapeau_color(self, robot_index, total_robots, time_val=0):
        """Retourne la couleur du drapeau Niger selon la position du robot."""
        # 3 bandes égales : Orange, Blanc, Vert
        bande_size = total_robots // 3
        bande = min(2, robot_index // bande_size)  # 0=orange, 1=blanc, 2=vert
        
        base_color = self.drapeau_colors[bande]
        
        # Effet de pulsation douce pour le blanc seulement
        if bande == 1:  # Bande blanche
            pulse = 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * time_val)
            r, g, b = self.hex_to_rgb(base_color)
            r = int(r * pulse)
            g = int(g * pulse)
            b = int(b * pulse)
            return self.rgb_to_hex(r, g, b)
        
        return base_color

    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - VERSION CORRIGÉE."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            # Couleur par défaut si pas d'index spécifique
            return self.colors['orange_niger']
        
        if "pluie" in phase_name.lower():
            return self.get_pluie_color(robot_index, total_robots, time_val)
        
        elif "drapeau" in phase_name.lower():
            # CORRECTION: Bien répartir en 3 bandes égales
            bande_size = total_robots // 3
            bande = min(2, robot_index // bande_size)
            return self.drapeau_colors[bande]
        
        elif "anem" in phase_name.lower() or "niger" in phase_name.lower():
            # Or pulsant pour les lettres
            pulse = 0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * time_val)
            r, g, b = self.hex_to_rgb(self.colors['or_soleil'])
            r = int(r * pulse)
            g = int(g * pulse) 
            b = int(b * pulse)
            return self.rgb_to_hex(r, g, b)
        
        elif "carte" in phase_name.lower():
            # Terre d'Agadez pour la carte
            return self.colors['terre_agadez']
        
        elif "finale" in phase_name.lower():
            # Arc-en-ciel dynamique pour la finale
            hue = (time_val * 1.5 + robot_index * 0.02) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            return self.rgb_to_hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        
        else:
            return self.drapeau_colors[robot_index % 3]
        
    def get_pluie_color(self, robot_index, total_robots, time_val):
        """Couleurs pour l'effet pluie drapeau."""
        # Alternance cyclique des 3 couleurs
        cycle_speed = 2.0  # Vitesse de changement
        color_index = int((time_val * cycle_speed + robot_index * 0.1)) % 3
        return self.drapeau_colors[color_index]
    
    def get_phase_color(self, positions, phase_name, time_val, robot_index=None):
        """Retourne la couleur appropriée pour chaque phase - VERSION AMÉLIORÉE."""
        total_robots = positions.shape[1] if positions is not None else 50
        
        if robot_index is None:
            # Couleur par défaut si pas d'index spécifique
            return self.colors['orange_niger']
        
        if "pluie" in phase_name.lower():
            return self.get_pluie_color(robot_index, total_robots, time_val)
        
        elif "drapeau" in phase_name.lower():
            return self.get_drapeau_color(robot_index, total_robots, time_val)
        
        elif "anem" in phase_name.lower() or "niger" in phase_name.lower():
            # Or pulsant pour les lettres
            pulse = 0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * time_val)
            r, g, b = self.hex_to_rgb(self.colors['or_soleil'])
            r = int(r * pulse)
            g = int(g * pulse) 
            b = int(b * pulse)
            return self.rgb_to_hex(r, g, b)
        
        elif "carte" in phase_name.lower():
            # Terre d'Agadez pour la carte
            return self.colors['terre_agadez']
        
        elif "finale" in phase_name.lower():
            # Arc-en-ciel dynamique pour la finale
            hue = (time_val * 1.5 + robot_index * 0.02) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
            return self.rgb_to_hex(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        
        else:
            return self.drapeau_colors[robot_index % 3]