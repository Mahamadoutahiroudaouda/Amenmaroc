# src/projects/project_05_feux_artifice.py
"""
PROJET #5: FEU D'ARTIFICE NIGÉRIEN
Robotarium Swarm - ANEM 2025
Simulation réaliste de feux d'artifice avec trajectoires balistiques
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project05FeuxArtifice:
    """Implémentation du projet Feu d'Artifice Nigérien."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_lancement': 20,          # 0:00-0:20
            '2_explosion_principale': 30, # 0:20-0:50
            '3_pluie_etoiles': 40,      # 0:50-1:30
            '4_feux_multiples': 40,     # 1:30-2:10
            '5_grand_finale': 20        # 2:10-2:30
        }
        
        # Paramètres physiques
        self.g = 1.5           # Gravité simulée
        self.v0_fusee = 2.0    # Vitesse initiale montée
        self.v0_explosion = 1.5 # Vitesse dispersion
        
        print(f"🚀 PROJET #5 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (2.5 minutes)")

    def phase_1_lancement(self, duration=20):
        """Phase 1: Lancement des fusées depuis le sol."""
        print("🚀 Phase 1: Lancement des fusées")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # 5 fusées successives
        n_fusees = 5
        robots_par_fusee = self.n // n_fusees
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            robot_count = 0
            
            for fusee in range(n_fusees):
                if robot_count >= self.n:
                    break
                    
                # Décalage temporel entre les fusées
                fusee_time = max(0, time_val - fusee * 3)  # 3s entre chaque fusée
                
                fusee_robots = min(robots_par_fusee, self.n - robot_count)
                
                for i in range(fusee_robots):
                    if robot_count < self.n:
                        # Position horizontale de la fusée
                        x_base = -0.8 + fusee * (1.6 / (n_fusees - 1)) if n_fusees > 1 else 0
                        
                        # Trajectoire parabolique
                        if fusee_time > 0:
                            # Montée de la fusée
                            y_pos = -0.9 + self.v0_fusee * fusee_time - 0.5 * self.g * fusee_time**2
                            
                            # Léger écartement horizontal pendant la montée
                            x_spread = 0.05 * np.sin(2*np.pi*2*fusee_time + i*0.5)
                            x_pos = x_base + x_spread
                        else:
                            # Au sol avant le lancement
                            x_pos = x_base
                            y_pos = -0.9
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_pos
                        robot_count += 1
            
            yield positions, time_val

    def phase_2_explosion_principale(self, start_pos, duration=30):
        """Phase 2: Explosion principale au sommet des trajectoires."""
        print("💥 Phase 2: Explosion principale")
        
        start_time = self.phases['1_lancement']
        steps = int(duration * config.FPS)
        
        # Calculer les positions d'explosion (au sommet des trajectoires)
        explosion_positions = self._calculate_explosion_positions()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Temps depuis l'explosion
            t_explosion = time_val
            
            robot_count = 0
            n_fusees = 5
            robots_par_fusee = self.n // n_fusees
            
            for fusee in range(n_fusees):
                if robot_count >= self.n:
                    break
                    
                fusee_robots = min(robots_par_fusee, self.n - robot_count)
                
                # Centre de l'explosion pour cette fusée
                center_x = -0.8 + fusee * (1.6 / (n_fusees - 1)) if n_fusees > 1 else 0
                center_y = 0.3  # Hauteur d'explosion
                
                for i in range(fusee_robots):
                    if robot_count < self.n:
                        # Direction radiale pour l'explosion
                        angle = (i / fusee_robots) * 2 * np.pi
                        
                        # Distance depuis le centre (expansion)
                        distance = self.v0_explosion * t_explosion
                        
                        # Position après explosion
                        x_pos = center_x + distance * np.cos(angle)
                        y_pos = center_y + distance * np.sin(angle) - 0.5 * self.g * t_explosion**2
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_pos
                        robot_count += 1
            
            yield positions, time_val

    def phase_3_pluie_etoiles(self, start_pos, duration=40):
        """Phase 3: Pluie d'étoiles - Retombées paraboliques."""
        print("🌠 Phase 3: Pluie d'étoiles")
        
        start_time = self.phases['1_lancement'] + self.phases['2_explosion_principale']
        steps = int(duration * config.FPS)
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Temps depuis le début de la phase
            t_pluie = time_val
            
            robot_count = 0
            n_fusees = 5
            robots_par_fusee = self.n // n_fusees
            
            for fusee in range(n_fusees):
                if robot_count >= self.n:
                    break
                    
                fusee_robots = min(robots_par_fusee, self.n - robot_count)
                center_x = -0.8 + fusee * (1.6 / (n_fusees - 1)) if n_fusees > 1 else 0
                
                for i in range(fusee_robots):
                    if robot_count < self.n:
                        # Angle initial de l'explosion
                        angle = (i / fusee_robots) * 2 * np.pi
                        
                        # Vitesses initiales
                        vx0 = self.v0_explosion * np.cos(angle)
                        vy0 = self.v0_explosion * np.sin(angle)
                        
                        # Position avec trajectoire balistique
                        x_pos = center_x + vx0 * t_pluie
                        y_pos = 0.3 + vy0 * t_pluie - 0.5 * self.g * t_pluie**2
                        
                        # Effet de traînée (ralentissement horizontal)
                        drag = np.exp(-0.1 * t_pluie)
                        x_pos = center_x + vx0 * t_pluie * drag
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_pos
                        robot_count += 1
            
            yield positions, time_val

    def phase_4_feux_multiples(self, start_pos, duration=40):
        """Phase 4: Feux multiples - 3 explosions simultanées."""
        print("🎇 Phase 4: Feux multiples")
        
        start_time = self.phases['1_lancement'] + self.phases['2_explosion_principale'] + self.phases['3_pluie_etoiles']
        steps = int(duration * config.FPS)
        
        # Positions des 3 explosions
        explosion_centers = [(-0.6, 0.4), (0.0, 0.6), (0.6, 0.3)]
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Temps depuis le début des explosions multiples
            t_multiple = time_val
            
            robot_count = 0
            n_explosions = 3
            robots_par_explosion = self.n // n_explosions
            
            for explosion in range(n_explosions):
                if robot_count >= self.n:
                    break
                    
                explosion_robots = min(robots_par_explosion, self.n - robot_count)
                center_x, center_y = explosion_centers[explosion]
                
                for i in range(explosion_robots):
                    if robot_count < self.n:
                        # Pattern d'explosion spécifique
                        if explosion == 0:
                            # Chrysanthème (sphérique)
                            angle = (i / explosion_robots) * 2 * np.pi
                            distance = self.v0_explosion * t_multiple
                        elif explosion == 1:
                            # Palmier (vertical)
                            angle = np.pi/2 + (i / explosion_robots - 0.5) * np.pi/3
                            distance = self.v0_explosion * t_multiple * (1 + 0.5 * (i / explosion_robots))
                        else:
                            # Tourbillon (spiral)
                            angle = (i / explosion_robots) * 4 * np.pi + t_multiple * 2
                            distance = self.v0_explosion * t_multiple * (0.5 + 0.5 * (i / explosion_robots))
                        
                        x_pos = center_x + distance * np.cos(angle)
                        y_pos = center_y + distance * np.sin(angle) - 0.5 * self.g * t_multiple**2
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_pos
                        robot_count += 1
            
            yield positions, time_val

    def phase_5_grand_finale(self, start_pos, duration=20):
        """Phase 5: Grand finale - Explosion sphérique totale."""
        print("🎆 Phase 5: Grand finale")
        
        start_time = (self.phases['1_lancement'] + 
                     self.phases['2_explosion_principale'] + 
                     self.phases['3_pluie_etoiles'] + 
                     self.phases['4_feux_multiples'])
        steps = int(duration * config.FPS)
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Temps depuis le début de la finale
            t_finale = time_val
            
            # Centre de l'explosion finale
            center_x, center_y = 0.0, 0.0
            
            for i in range(self.n):
                # Pattern final complexe
                if t_finale < 10:
                    # Expansion sphérique
                    angle = (i / self.n) * 4 * np.pi  # Double spirale
                    distance = self.v0_explosion * t_finale * (0.8 + 0.4 * np.sin(angle))
                    
                    x_pos = center_x + distance * np.cos(angle)
                    y_pos = center_y + distance * np.sin(angle)
                else:
                    # Contraction puis disparition
                    contraction_time = t_finale - 10
                    contraction = 1.0 / (1 + contraction_time)
                    
                    angle = (i / self.n) * 4 * np.pi
                    distance = self.v0_explosion * 10 * contraction
                    
                    x_pos = center_x + distance * np.cos(angle)
                    y_pos = center_y + distance * np.sin(angle)
                
                # Légère chute due à la gravité
                y_pos -= 0.2 * self.g * t_finale**2
                
                positions[0, i] = x_pos
                positions[1, i] = y_pos
            
            yield positions, time_val

    def _calculate_explosion_positions(self):
        """Calcule les positions optimales pour les explosions."""
        # Pour l'instant, retourne des positions par défaut
        # Cette méthode pourrait être étendue pour des calculs plus complexes
        return [(-0.8, 0.3), (-0.4, 0.3), (0.0, 0.3), (0.4, 0.3), (0.8, 0.3)]

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #5: FEU D'ARTIFICE NIGÉRIEN")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = phase_name.replace('_', ' ').replace('1 ', '').replace('2 ', '').replace('3 ', '').replace('4 ', '').replace('5 ', '')
            
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
        print(f"✅ PROJET #5 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")