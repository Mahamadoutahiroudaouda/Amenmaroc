# src/projects/project_04_constellations.py
"""
PROJET #4: CONSTELLATION VIVANTE
Robotarium Swarm - ANEM 2025
Formation dynamique de constellations célèbres avec transitions fluides
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project04Constellations:
    """Implémentation du projet Constellation Vivante."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_grande_ourse': 60,      # 0:00-1:00
            '2_orion': 60,             # 1:00-2:00
            '3_croix_sud': 60,         # 2:00-3:00
            '4_spirale_galactique': 60 # 3:00-4:00
        }
        
        # Données astronomiques réelles
        self.constellations = {
            'grande_ourse': [
                {"nom": "Dubhe", "pos": (0.5, 0.8), "mag": 1.8, "type": "K"},
                {"nom": "Merak", "pos": (0.7, 0.6), "mag": 2.4, "type": "A"},
                {"nom": "Phecda", "pos": (0.9, 0.5), "mag": 2.4, "type": "A"},
                {"nom": "Megrez", "pos": (1.0, 0.7), "mag": 3.3, "type": "A"},
                {"nom": "Alioth", "pos": (1.2, 0.9), "mag": 1.8, "type": "A"},
                {"nom": "Mizar", "pos": (1.4, 1.0), "mag": 2.2, "type": "A"},
                {"nom": "Alkaid", "pos": (1.6, 0.8), "mag": 1.9, "type": "B"}
            ],
            'orion': [
                {"nom": "Bételgeuse", "pos": (-0.8, 0.6), "mag": 0.5, "type": "M"},
                {"nom": "Rigel", "pos": (0.9, -0.7), "mag": 0.1, "type": "B"},
                {"nom": "Bellatrix", "pos": (-0.5, 0.4), "mag": 1.6, "type": "B"},
                {"nom": "Mintaka", "pos": (0.0, 0.0), "mag": 2.2, "type": "O"},
                {"nom": "Alnilam", "pos": (0.1, 0.1), "mag": 1.7, "type": "B"},
                {"nom": "Alnitak", "pos": (0.2, 0.2), "mag": 1.9, "type": "O"}
            ],
            'croix_sud': [
                {"nom": "Acrux", "pos": (0.0, 0.6), "mag": 0.8, "type": "B"},
                {"nom": "Mimosa", "pos": (0.3, 0.3), "mag": 1.3, "type": "B"},
                {"nom": "Gacrux", "pos": (0.0, -0.6), "mag": 1.6, "type": "M"},
                {"nom": "Imai", "pos": (-0.3, 0.0), "mag": 2.8, "type": "B"}
            ]
        }
        
        # Couleurs stellaires selon la température
        self.couleurs_etoiles = {
            "O": "#9BB0FF",  # Très chaude (bleu)
            "B": "#AABFFF",  # Chaude (bleu-blanc)
            "A": "#CAD7FF",  # Blanc
            "F": "#F8F7FF",  # Blanc jaunâtre
            "G": "#FFF4EA",  # Jaune (Soleil)
            "K": "#FFD2A1",  # Orange
            "M": "#FFCC6F"   # Froide (rouge)
        }
        
        print(f"🚀 PROJET #4 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (4 minutes)")

    def phase_1_grande_ourse(self, duration=60):
        """Phase 1: Grande Ourse - Constellation emblématique."""
        print("🐻 Phase 1: Grande Ourse")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Créer la formation de la Grande Ourse
        target_ourse = self._create_grande_ourse()
        
        # Transition depuis positions aléatoires (20s)
        start_pos = self.base.random_positions()
        
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_ourse, 20)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Animation de la constellation (40s)
        maintain_steps = steps - int(20 * config.FPS)
        base_positions = target_ourse.copy()
        
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Rotation lente autour de l'étoile polaire
            angle = 2 * np.pi * 0.05 * time_val  # Rotation très lente
            
            # Centre de rotation (près de l'étoile polaire)
            center_x, center_y = 0.2, 0.9
            
            # Appliquer la rotation
            rotated_pos = base_positions.copy()
            for i in range(self.n):
                x = base_positions[0, i] - center_x
                y = base_positions[1, i] - center_y
                
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                
                rotated_pos[0, i] = new_x + center_x
                rotated_pos[1, i] = new_y + center_y
            
            # Effet de scintillement
            scintillement = 1.0 + 0.1 * np.sin(2*np.pi*2*time_val + np.arange(self.n)*0.1)
            center = np.mean(rotated_pos, axis=1, keepdims=True)
            animated_pos = center + (rotated_pos - center) * scintillement.reshape(1, -1)
            
            yield animated_pos, time_val

    def phase_2_orion(self, start_pos, duration=60):
        """Phase 2: Orion - Chasseur céleste avec nébuleuse."""
        print("🏹 Phase 2: Orion")
        
        start_time = self.phases['1_grande_ourse']
        steps = int(duration * config.FPS)
        
        # Créer la formation d'Orion
        target_orion = self._create_orion()
        
        # Transition depuis Grande Ourse (20s)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_orion, 20)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Animation d'Orion (40s)
        maintain_steps = steps - int(20 * config.FPS)
        base_positions = target_orion.copy()
        
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Animation de la nébuleuse (mouvement de nuage)
            nebula_movement = 0.05 * np.sin(2*np.pi*0.3*time_val + np.arange(self.n)*0.01)
            
            animated_pos = base_positions.copy()
            # Appliquer le mouvement seulement aux robots de la nébuleuse
            nebula_indices = range(30, min(45, self.n))  # Indices pour la nébuleuse
            for idx in nebula_indices:
                if idx < self.n:
                    animated_pos[0, idx] += nebula_movement[idx] * 0.1
                    animated_pos[1, idx] += nebula_movement[idx] * 0.05
            
            # Scintillement des étoiles
            scintillement = 1.0 + 0.15 * np.sin(2*np.pi*3*time_val + np.arange(self.n)*0.2)
            center = np.mean(animated_pos, axis=1, keepdims=True)
            animated_pos = center + (animated_pos - center) * scintillement.reshape(1, -1)
            
            yield animated_pos, time_val

    def phase_3_croix_sud(self, start_pos, duration=60):
        """Phase 3: Croix du Sud - Constellation de l'hémisphère sud."""
        print("✝️  Phase 3: Croix du Sud")
        
        start_time = self.phases['1_grande_ourse'] + self.phases['2_orion']
        steps = int(duration * config.FPS)
        
        # Créer la formation de la Croix du Sud
        target_croix = self._create_croix_sud()
        
        # Transition depuis Orion (20s)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_croix, 20)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Animation de la Croix du Sud (40s)
        maintain_steps = steps - int(20 * config.FPS)
        base_positions = target_croix.copy()
        
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Rotation complète de la croix
            angle = 2 * np.pi * 0.1 * time_val  # Rotation toutes les 10s
            
            center_x = np.mean(base_positions[0, :])
            center_y = np.mean(base_positions[1, :])
            
            rotated_pos = base_positions.copy()
            for i in range(self.n):
                x = base_positions[0, i] - center_x
                y = base_positions[1, i] - center_y
                
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                
                rotated_pos[0, i] = new_x + center_x
                rotated_pos[1, i] = new_y + center_y
            
            # Scintillement
            scintillement = 1.0 + 0.1 * np.sin(2*np.pi*2*time_val + np.arange(self.n)*0.15)
            center = np.mean(rotated_pos, axis=1, keepdims=True)
            animated_pos = center + (rotated_pos - center) * scintillement.reshape(1, -1)
            
            yield animated_pos, time_val

    def phase_4_spirale_galactique(self, start_pos, duration=60):
        """Phase 4: Spirale Galactique - Transformation en galaxie."""
        print("🌌 Phase 4: Spirale Galactique")
        
        start_time = self.phases['1_grande_ourse'] + self.phases['2_orion'] + self.phases['3_croix_sud']
        steps = int(duration * config.FPS)
        
        # Créer la formation spirale galactique
        target_galaxie = self._create_spirale_galactique()
        
        # Transition depuis Croix du Sud (20s)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_galaxie, 20)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Animation de la galaxie (40s)
        maintain_steps = steps - int(20 * config.FPS)
        base_positions = target_galaxie.copy()
        
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Rotation différentielle (centre plus rapide)
            animated_pos = base_positions.copy()
            
            for i in range(self.n):
                x = base_positions[0, i]
                y = base_positions[1, i]
                
                # Distance du centre
                r = np.sqrt(x**2 + y**2)
                
                # Vitesse angulaire décroissante avec la distance
                angular_speed = 0.5 / (1 + r*2)  # Plus rapide au centre
                angle = angular_speed * time_val
                
                # Rotation
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                
                animated_pos[0, i] = new_x
                animated_pos[1, i] = new_y
            
            # Légère expansion/contraction
            pulse = 1.0 + 0.05 * np.sin(2*np.pi*0.2*time_val)
            center = np.mean(animated_pos, axis=1, keepdims=True)
            animated_pos = center + (animated_pos - center) * pulse
            
            yield animated_pos, time_val

    def _create_grande_ourse(self):
        """Crée la formation de la Grande Ourse."""
        positions = np.zeros((2, self.n))
        
        # Étoiles principales (7 étoiles)
        etoiles_principales = self.constellations['grande_ourse']
        n_principales = min(len(etoiles_principales), self.n // 2)
        
        robot_count = 0
        
        # Placer les étoiles principales
        for i in range(n_principales):
            if robot_count < self.n:
                etoile = etoiles_principales[i]
                positions[0, robot_count] = etoile['pos'][0]
                positions[1, robot_count] = etoile['pos'][1]
                robot_count += 1
        
        # Environnement stellaire (étoiles secondaires)
        n_secondaires = self.n - robot_count
        if n_secondaires > 0:
            # Répartir autour des étoiles principales
            for i in range(n_secondaires):
                if robot_count < self.n:
                    # Choisir une étoile principale aléatoire comme centre
                    centre_idx = np.random.randint(0, n_principales)
                    centre_x = etoiles_principales[centre_idx]['pos'][0]
                    centre_y = etoiles_principales[centre_idx]['pos'][1]
                    
                    # Position aléatoire autour du centre
                    angle = np.random.uniform(0, 2*np.pi)
                    distance = np.random.uniform(0.1, 0.3)
                    
                    positions[0, robot_count] = centre_x + distance * np.cos(angle)
                    positions[1, robot_count] = centre_y + distance * np.sin(angle)
                    robot_count += 1
        
        return positions

    def _create_orion(self):
        """Crée la formation de la constellation d'Orion."""
        positions = np.zeros((2, self.n))
        
        etoiles_orion = self.constellations['orion']
        n_principales = min(len(etoiles_orion), self.n // 3)
        
        robot_count = 0
        
        # Étoiles principales
        for i in range(n_principales):
            if robot_count < self.n:
                etoile = etoiles_orion[i]
                positions[0, robot_count] = etoile['pos'][0]
                positions[1, robot_count] = etoile['pos'][1]
                robot_count += 1
        
        # Ceinture d'Orion (3 étoiles alignées)
        if robot_count < self.n:
            ceinture_robots = min(15, self.n - robot_count)
            for i in range(ceinture_robots):
                if robot_count < self.n:
                    x = -0.1 + i * (0.2 / (ceinture_robots - 1)) if ceinture_robots > 1 else 0
                    y = 0.0
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        # Nébuleuse d'Orion (nuage autour de la ceinture)
        if robot_count < self.n:
            nebula_robots = min(20, self.n - robot_count)
            for i in range(nebula_robots):
                if robot_count < self.n:
                    # Position aléatoire dans la zone de la nébuleuse
                    x = np.random.uniform(-0.3, 0.4)
                    y = np.random.uniform(-0.2, 0.3)
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        # Étoiles environnantes
        if robot_count < self.n:
            rest_robots = self.n - robot_count
            for i in range(rest_robots):
                if robot_count < self.n:
                    x = np.random.uniform(-1.0, 1.0)
                    y = np.random.uniform(-0.8, 0.8)
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        return positions

    def _create_croix_sud(self):
        """Crée la formation de la Croix du Sud."""
        positions = np.zeros((2, self.n))
        
        etoiles_croix = self.constellations['croix_sud']
        n_principales = min(len(etoiles_croix), self.n // 4)
        
        robot_count = 0
        
        # Étoiles principales de la croix
        for i in range(n_principales):
            if robot_count < self.n:
                etoile = etoiles_croix[i]
                positions[0, robot_count] = etoile['pos'][0]
                positions[1, robot_count] = etoile['pos'][1]
                robot_count += 1
        
        # Renforcer la forme de croix
        if robot_count < self.n:
            croix_robots = min(20, self.n - robot_count)
            
            # Bras vertical
            bras_v = min(8, croix_robots // 2)
            for i in range(bras_v):
                if robot_count < self.n:
                    y = -0.6 + i * (1.2 / (bras_v - 1)) if bras_v > 1 else 0
                    positions[0, robot_count] = 0.0
                    positions[1, robot_count] = y
                    robot_count += 1
            
            # Bras horizontal
            bras_h = croix_robots - bras_v
            for i in range(bras_h):
                if robot_count < self.n:
                    x = -0.3 + i * (0.6 / (bras_h - 1)) if bras_h > 1 else 0
                    positions[0, robot_count] = x
                    positions[1, robot_count] = 0.0
                    robot_count += 1
        
        # Étoiles environnantes
        if robot_count < self.n:
            rest_robots = self.n - robot_count
            for i in range(rest_robots):
                if robot_count < self.n:
                    angle = np.random.uniform(0, 2*np.pi)
                    distance = np.random.uniform(0.4, 0.8)
                    positions[0, robot_count] = distance * np.cos(angle)
                    positions[1, robot_count] = distance * np.sin(angle)
                    robot_count += 1
        
        return positions

    def _create_spirale_galactique(self):
        """Crée la formation d'une galaxie spirale."""
        positions = np.zeros((2, self.n))
        
        robot_count = 0
        
        # Noyau central (20% des robots)
        noyau_robots = min(int(self.n * 0.2), self.n - robot_count)
        if noyau_robots > 0:
            angles_noyau = np.linspace(0, 2*np.pi, noyau_robots, endpoint=False)
            rayon_noyau = 0.2
            positions[0, robot_count:robot_count+noyau_robots] = rayon_noyau * np.cos(angles_noyau)
            positions[1, robot_count:robot_count+noyau_robots] = rayon_noyau * np.sin(angles_noyau)
            robot_count += noyau_robots
        
        # Bras spiraux (80% des robots)
        n_bras = 4  # 4 bras spiraux
        robots_par_bras = (self.n - robot_count) // n_bras
        
        for bras in range(n_bras):
            if robot_count >= self.n:
                break
                
            bras_robots = min(robots_par_bras, self.n - robot_count)
            
            # Paramètres du bras spiral
            angle_depart = bras * (2*np.pi / n_bras)
            angle_fin = angle_depart + 2*np.pi  # Un tour complet
            
            for i in range(bras_robots):
                if robot_count < self.n:
                    # Progression le long du bras (0 à 1)
                    t = i / bras_robots
                    
                    # Angle le long du bras spiral
                    angle = angle_depart + t * (angle_fin - angle_depart)
                    
                    # Rayon croissant
                    rayon = 0.3 + t * 0.7
                    
                    # Spirale logarithmique
                    x = rayon * np.cos(angle + 2*t*np.pi)
                    y = rayon * np.sin(angle + 2*t*np.pi)
                    
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        return positions

    def get_star_color(self, robot_index, constellation_data):
        """Retourne la couleur d'une étoile selon son type spectral."""
        if robot_index < len(constellation_data):
            star_type = constellation_data[robot_index]['type']
            return self.couleurs_etoiles.get(star_type, self.couleurs_etoiles['G'])
        return self.couleurs_etoiles['G']

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #4: CONSTELLATION VIVANTE")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = phase_name.replace('_', ' ').replace('1 ', '').replace('2 ', '').replace('3 ', '').replace('4 ', '')
            
            print(f"\n▶️  Début {display_name} ({duration}s, {phase_frames} frames)")
            
            if current_pos is None:
                # Première phase
                for pos, time_val in phase_method(duration):
                    current_pos = pos
                    yield pos, display_name, time_val, frame_count
                    frame_count += 1
                    
                    if frame_count % 30 == 0:
                        print(f"   📊 Frame {frame_count:04d} | {time_val:05.1f}s")
            else:
                # Phases suivantes
                for pos, time_val in phase_method(current_pos, duration):
                    current_pos = pos
                    yield pos, display_name, time_val, frame_count
                    frame_count += 1
                    
                    if frame_count % 30 == 0:
                        print(f"   📊 Frame {frame_count:04d} | {time_val:05.1f}s")
            
            print(f"✅ {display_name} terminée")
        
        print("=" * 60)
        print(f"✅ PROJET #4 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")