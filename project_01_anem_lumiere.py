# src/projects/project_01_anem_lumiere.py
"""
PROJET #1: ANEM EN LUMIÈRE - VERSION COMPLÈTE
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.letter_formations import LetterFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project01AnemLumiere:
    """Implémentation complète du projet ANEM en Lumière avec phases améliorées."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.letters = LetterFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_pluie_drapeau': 15,      # Pluie drapeau
            '2_formation_anem': 20,     # ANEM  
            '3_formation_niger': 20,    # NIGER
            '4_drapeau_pulsant': 25,    # Drapeau
            '5_carte_niger': 45,        # Carte Niger
            '6_finale_etoile': 30       # Finale étoile
        }
        
        print(f"🚀 PROJET #1 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes")

    def phase_1_pluie_drapeau(self, duration=15):
        """Phase 1: Pluie de lignes colorées comme le drapeau du Niger."""
        print("🌧️  Phase 1: Pluie du drapeau nigérien")
        
        # Créer des lignes horizontales SÉPARÉES qui tombent
        n_lignes = 9
        robots_par_ligne = max(1, self.n // n_lignes)
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Positionner chaque ligne SÉPARÉMENT
            robot_count = 0
            for i in range(n_lignes):
                ligne_robots = robots_par_ligne if i < n_lignes - 1 else self.n - robot_count
                
                if robot_count < self.n and ligne_robots > 0:
                    # Position horizontale avec espacement
                    x_pos = np.linspace(-1.0, 1.0, ligne_robots)
                    
                    # Position verticale avec effet de "chute" DÉCALÉE
                    y_start = 1.2 - (i * 0.15)
                    y_pos = y_start - (time_val * 1.2 + i * 0.3) % 3.0
                    
                    positions[0, robot_count:robot_count + ligne_robots] = x_pos
                    positions[1, robot_count:robot_count + ligne_robots] = y_pos
                    robot_count += ligne_robots
        
            yield positions, time_val

    def phase_2_formation_anem(self, start_pos, duration=20):
        """Phase 2: Formation des lettres A-N-E-M."""
        print("🔤 Phase 2: Formation ANEM")
        
        # Régénérer la formation ANEM
        self.letters = LetterFormations(self.n)
        target_anem = self.letters.get_ANEM_formation()
        
        # S'assurer que les shapes correspondent
        if target_anem.shape[1] != start_pos.shape[1]:
            n_robots = start_pos.shape[1]
            if n_robots < target_anem.shape[1]:
                target_anem = target_anem[:, :n_robots]
            else:
                repeat_factor = int(np.ceil(n_robots / target_anem.shape[1]))
                repeated_formation = np.tile(target_anem, (1, repeat_factor))
                target_anem = repeated_formation[:, :n_robots]
        
        start_time = self.phases['1_pluie_drapeau']
        
        steps = int(duration * config.FPS)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_anem, duration)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val

    def phase_3_formation_niger(self, start_pos, duration=20):
        """Phase 3: Formation du mot NIGER."""
        print("🔤 Phase 3: Formation NIGER")
        
        if self.n < 25:
            print("   ℹ️  Nombre de robots insuffisant pour NIGER, utilisation d'un cercle")
            target_niger = self.letters.circle(radius=0.7)
        else:
            self.letters = LetterFormations(self.n)
            target_niger = self.letters.get_NIGER_formation()
        
        # S'assurer que les shapes correspondent
        if target_niger.shape[1] != start_pos.shape[1]:
            n_robots = start_pos.shape[1]
            if n_robots < target_niger.shape[1]:
                target_niger = target_niger[:, :n_robots]
            else:
                repeat_factor = int(np.ceil(n_robots / target_niger.shape[1]))
                repeated_formation = np.tile(target_niger, (1, repeat_factor))
                target_niger = repeated_formation[:, :n_robots]
        
        start_time = self.phases['1_pluie_drapeau'] + self.phases['2_formation_anem']
        
        steps = int(duration * config.FPS)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_niger, duration)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val

    def phase_4_drapeau_pulsant(self, start_pos, duration=25):
        """Phase 4: Drapeau du Niger pulsant."""
        print("🇳🇪 Phase 4: Drapeau du Niger pulsant")
        
        n_bandes = min(3, self.n // 2)
        robots_par_bande = max(1, self.n // n_bandes)
        
        target_drapeau = np.zeros((2, self.n))
        
        robot_count = 0
        for i in range(n_bandes):
            bande_robots = robots_par_bande if i < n_bandes - 1 else self.n - robot_count
            
            if robot_count < self.n and bande_robots > 0:
                x_pos = np.linspace(-1.2, 1.2, bande_robots)
                
                if i == 0:
                    y_pos = np.full(bande_robots, 0.4)
                elif i == 1:
                    y_pos = np.full(bande_robots, 0.0)
                else:
                    y_pos = np.full(bande_robots, -0.4)
                
                target_drapeau[0, robot_count:robot_count + bande_robots] = x_pos
                target_drapeau[1, robot_count:robot_count + bande_robots] = y_pos
                robot_count += bande_robots
        
        start_time = (self.phases['1_pluie_drapeau'] + 
                     self.phases['2_formation_anem'] + 
                     self.phases['3_formation_niger'])
        
        steps = int(duration * config.FPS)
        base_positions = target_drapeau.copy()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            
            pulse_factor = 1.0 + 0.15 * np.sin(2 * np.pi * 0.8 * time_val)
            center = np.mean(base_positions, axis=1, keepdims=True)
            current_pos = center + (base_positions - center) * pulse_factor
            
            yield current_pos, time_val

    def phase_5_carte_niger(self, start_pos, duration=45):
        """Phase 5: Carte du Niger avec GeoJSON et soleil."""
        print("🗺️  Phase 5: Carte du Niger avec soleil")
        
        from formations.geo_formations import GeoFormations
        geo = GeoFormations(self.n)
        target_carte = geo.get_niger_map_formation()
        
        if target_carte.shape[1] != start_pos.shape[1]:
            n_robots = start_pos.shape[1]
            if n_robots < target_carte.shape[1]:
                target_carte = target_carte[:, :n_robots]
            else:
                repeat_factor = int(np.ceil(n_robots / target_carte.shape[1]))
                repeated_formation = np.tile(target_carte, (1, repeat_factor))
                target_carte = repeated_formation[:, :n_robots]
        
        start_time = (self.phases['1_pluie_drapeau'] + 
                     self.phases['2_formation_anem'] + 
                     self.phases['3_formation_niger'] + 
                     self.phases['4_drapeau_pulsant'])
        
        steps = int(duration * config.FPS)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_carte, duration)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val

    def phase_6_finale_etoile(self, start_pos, duration=30):
        """Phase 6: Finale explosive avec étoile."""
        print("💫 Phase 6: Finale étoile")
        
        # Utiliser l'étoile de base_formations
        target_star = self.letters.star(n_points=8, outer_radius=0.9, inner_radius=0.3)
        
        if target_star.shape[1] != start_pos.shape[1]:
            n_robots = start_pos.shape[1]
            if n_robots < target_star.shape[1]:
                target_star = target_star[:, :n_robots]
            else:
                repeat_factor = int(np.ceil(n_robots / target_star.shape[1]))
                repeated_star = np.tile(target_star, (1, repeat_factor))
                target_star = repeated_star[:, :n_robots]
        
        start_time = (self.phases['1_pluie_drapeau'] + 
                     self.phases['2_formation_anem'] + 
                     self.phases['3_formation_niger'] + 
                     self.phases['4_drapeau_pulsant'] + 
                     self.phases['5_carte_niger'])
        
        steps = int(duration * config.FPS)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_star, duration, 'elastic')
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage de l'animation complète ANEM EN LUMIÈRE")
        print("=" * 50)
        
        current_pos = None
        total_frames = sum(int(duration * config.FPS) for duration in self.phases.values())
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage plus joli
            display_name = phase_name.replace('_', ' ').replace('1 ', '').replace('2 ', '').replace('3 ', '').replace('4 ', '').replace('5 ', '').replace('6 ', '')
            
            print(f"\n▶️  Début {display_name} ({duration}s, {phase_frames} frames)")
            
            if current_pos is None:
                # Première phase
                for pos, time_val in phase_method(duration):
                    current_pos = pos
                    yield pos, display_name, time_val, frame_count
                    frame_count += 1
                    
                    # Log de progression
                    if frame_count % 30 == 0:
                        print(f"   📊 Frame {frame_count:04d} | {time_val:05.1f}s | Robots: {pos.shape[1]}")
            else:
                # Phases suivantes
                for pos, time_val in phase_method(current_pos, duration):
                    current_pos = pos
                    yield pos, display_name, time_val, frame_count
                    frame_count += 1
                    
                    # Log de progression
                    if frame_count % 30 == 0:
                        print(f"   📊 Frame {frame_count:04d} | {time_val:05.1f}s | Robots: {pos.shape[1]}")
            
            print(f"✅ {display_name} terminée")
        
        print("=" * 50)
        print(f"✅ PROJET #1 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")