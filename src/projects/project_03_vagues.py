# src/projects/project_03_vagues.py
"""
PROJET #3: VAGUES OCÉANIQUES
Robotarium Swarm - ANEM 2025
Simulation hypnotique de vagues océaniques avec interférences
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project03Vagues:
    """Implémentation du projet Vagues Océaniques."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_ocean_calme': 40,           # 0:00-0:40
            '2_tempete_progressive': 50,   # 0:40-1:30
            '3_interferences': 50,         # 1:30-2:20
            '4_tsunami': 30,               # 2:20-2:50
            '5_retour_calme': 10           # 2:50-3:00
        }
        
        # Paramètres des vagues
        self.vague_params = {
            'calme': {'A': 0.3, 'λ': 2.0, 'f': 0.5},
            'tempete': {'A': 0.8, 'λ': 1.5, 'f': 0.7},
            'interference1': {'A': 0.5, 'λ': 2.0, 'f': 0.5},
            'interference2': {'A': 0.3, 'λ': 1.5, 'f': 0.7},
            'interference3': {'A': 0.2, 'λ': 1.0, 'f': 1.0},
            'tsunami': {'A': 1.2, 'λ': 3.0, 'f': 0.3}
        }
        
        print(f"🚀 PROJET #3 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (3 minutes)")

    def phase_1_ocean_calme(self, duration=40):
        """Phase 1: Océan calme - Une vague sinusoïdale douce."""
        print("🌊 Phase 1: Océan calme")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Configuration des robots en grille pour les vagues
        n_colonnes = 10
        n_lignes = self.n // n_colonnes
        robots_par_colonne = n_lignes
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Paramètres de la vague calme
            A = self.vague_params['calme']['A']
            λ = self.vague_params['calme']['λ']
            f = self.vague_params['calme']['f']
            
            robot_count = 0
            for col in range(n_colonnes):
                if robot_count >= self.n:
                    break
                    
                x_pos = -1.2 + col * (2.4 / (n_colonnes - 1)) if n_colonnes > 1 else 0
                robots_dans_colonne = min(robots_par_colonne, self.n - robot_count)
                
                for ligne in range(robots_dans_colonne):
                    if robot_count < self.n:
                        # Position verticale basée sur l'équation d'onde
                        y_base = -0.5 + ligne * (1.0 / (robots_par_colonne - 1)) if robots_par_colonne > 1 else 0
                        
                        # Équation de vague simple
                        y_wave = A * np.sin(2*np.pi*(x_pos/λ - f*time_val))
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_base + y_wave
                        robot_count += 1
            
            yield positions, time_val

    def phase_2_tempete_progressive(self, start_pos, duration=50):
        """Phase 2: Tempête progressive - Amplitude croissante + vagues secondaires."""
        print("🌪️  Phase 2: Tempête progressive")
        
        start_time = self.phases['1_ocean_calme']
        steps = int(duration * config.FPS)
        
        n_colonnes = 10
        n_lignes = self.n // n_colonnes
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Progression de la tempête (0 à 1)
            progression = step / steps
            
            # Amplitude croissante
            A_base = self.vague_params['calme']['A']
            A_tempete = self.vague_params['tempete']['A']
            A = A_base + (A_tempete - A_base) * progression
            
            # Fréquence augmentant progressivement
            f_base = self.vague_params['calme']['f']
            f_tempete = self.vague_params['tempete']['f']
            f = f_base + (f_tempete - f_base) * progression
            
            λ = self.vague_params['tempete']['λ']
            
            robot_count = 0
            for col in range(n_colonnes):
                if robot_count >= self.n:
                    break
                    
                x_pos = -1.2 + col * (2.4 / (n_colonnes - 1)) if n_colonnes > 1 else 0
                robots_dans_colonne = min(n_lignes, self.n - robot_count)
                
                for ligne in range(robots_dans_colonne):
                    if robot_count < self.n:
                        y_base = -0.5 + ligne * (1.0 / (n_lignes - 1)) if n_lignes > 1 else 0
                        
                        # Vague principale + vague secondaire
                        y_main = A * np.sin(2*np.pi*(x_pos/λ - f*time_val))
                        y_secondary = 0.2 * A * np.sin(2*np.pi*(x_pos/(λ*0.7) - 1.5*f*time_val + 0.5))
                        
                        # Effet de vent (déplacement horizontal)
                        wind_effect = 0.1 * progression * np.sin(2*np.pi*0.3*time_val)
                        
                        positions[0, robot_count] = x_pos + wind_effect
                        positions[1, robot_count] = y_base + y_main + y_secondary
                        robot_count += 1
            
            yield positions, time_val

    def phase_3_interferences(self, start_pos, duration=50):
        """Phase 3: Interférences complexes - 3 vagues simultanées."""
        print("🌀 Phase 3: Interférences complexes")
        
        start_time = self.phases['1_ocean_calme'] + self.phases['2_tempete_progressive']
        steps = int(duration * config.FPS)
        
        n_colonnes = 10
        n_lignes = self.n // n_colonnes
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Paramètres des 3 vagues interférentes
            v1 = self.vague_params['interference1']
            v2 = self.vague_params['interference2'] 
            v3 = self.vague_params['interference3']
            
            robot_count = 0
            for col in range(n_colonnes):
                if robot_count >= self.n:
                    break
                    
                x_pos = -1.2 + col * (2.4 / (n_colonnes - 1)) if n_colonnes > 1 else 0
                robots_dans_colonne = min(n_lignes, self.n - robot_count)
                
                for ligne in range(robots_dans_colonne):
                    if robot_count < self.n:
                        y_base = -0.5 + ligne * (1.0 / (n_lignes - 1)) if n_lignes > 1 else 0
                        
                        # Trois vagues interférentes
                        y1 = v1['A'] * np.sin(2*np.pi*(x_pos/v1['λ'] - v1['f']*time_val))
                        y2 = v2['A'] * np.sin(2*np.pi*(x_pos/v2['λ'] - v2['f']*time_val + 0.3))
                        y3 = v3['A'] * np.sin(2*np.pi*(x_pos/v3['λ'] - v3['f']*time_val + 0.7))
                        
                        # Somme des vagues (interférence)
                        y_total = y1 + y2 + y3
                        
                        # Effet de Moiré (modulation d'amplitude)
                        moire = 0.5 + 0.5 * np.sin(2*np.pi*0.2*time_val + x_pos*2)
                        y_total *= moire
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_base + y_total
                        robot_count += 1
            
            yield positions, time_val

    def phase_4_tsunami(self, start_pos, duration=30):
        """Phase 4: Tsunami - Convergence en une vague géante."""
        print("🌅 Phase 4: Tsunami")
        
        start_time = (self.phases['1_ocean_calme'] + 
                     self.phases['2_tempete_progressive'] + 
                     self.phases['3_interferences'])
        steps = int(duration * config.FPS)
        
        n_colonnes = 10
        n_lignes = self.n // n_colonnes
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Progression du tsunami (0 à 1)
            progression = step / steps
            
            # Paramètres du tsunami
            A_tsunami = self.vague_params['tsunami']['A']
            λ_tsunami = self.vague_params['tsunami']['λ']
            f_tsunami = self.vague_params['tsunami']['f']
            
            robot_count = 0
            for col in range(n_colonnes):
                if robot_count >= self.n:
                    break
                    
                x_pos = -1.2 + col * (2.4 / (n_colonnes - 1)) if n_colonnes > 1 else 0
                robots_dans_colonne = min(n_lignes, self.n - robot_count)
                
                for ligne in range(robots_dans_colonne):
                    if robot_count < self.n:
                        y_base = -0.5 + ligne * (1.0 / (n_lignes - 1)) if n_lignes > 1 else 0
                        
                        # Formation progressive du tsunami
                        if progression < 0.7:
                            # Phase de montée
                            tsunami_factor = progression / 0.7
                            A = A_tsunami * tsunami_factor
                            
                            # Vague qui se concentre au centre
                            center_attraction = np.exp(-4 * (x_pos)**2)  # Gaussienne centrée
                            y_tsunami = A * center_attraction * np.sin(2*np.pi*(x_pos/λ_tsunami - f_tsunami*time_val))
                        else:
                            # Phase de déferlante
                            tsunami_factor = 1.0
                            A = A_tsunami * tsunami_factor
                            
                            # Vague qui déferle vers la droite
                            wave_front = np.clip((x_pos + 1.0 - 2*(progression-0.7)) * 5, 0, 1)
                            y_tsunami = A * wave_front * np.sin(2*np.pi*(x_pos/λ_tsunami - 2*f_tsunami*time_val))
                        
                        positions[0, robot_count] = x_pos
                        positions[1, robot_count] = y_base + y_tsunami
                        robot_count += 1
            
            yield positions, time_val

    def phase_5_retour_calme(self, start_pos, duration=10):
        """Phase 5: Retour au calme - Décroissance exponentielle."""
        print("😌 Phase 5: Retour au calme")
        
        start_time = (self.phases['1_ocean_calme'] + 
                     self.phases['2_tempete_progressive'] + 
                     self.phases['3_interferences'] + 
                     self.phases['4_tsunami'])
        steps = int(duration * config.FPS)
        
        # Position cible (ligne horizontale calme)
        target_calme = np.zeros((2, self.n))
        n_colonnes = 10
        n_lignes = self.n // n_colonnes
        
        robot_count = 0
        for col in range(n_colonnes):
            if robot_count >= self.n:
                break
                
            x_pos = -1.2 + col * (2.4 / (n_colonnes - 1)) if n_colonnes > 1 else 0
            robots_dans_colonne = min(n_lignes, self.n - robot_count)
            
            for ligne in range(robots_dans_colonne):
                if robot_count < self.n:
                    y_pos = -0.5 + ligne * (1.0 / (n_lignes - 1)) if n_lignes > 1 else -0.5
                    
                    target_calme[0, robot_count] = x_pos
                    target_calme[1, robot_count] = y_pos
                    robot_count += 1
        
        # Transition vers le calme
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_calme, duration, 'ease_in_out')
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #3: VAGUES OCÉANIQUES")
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
        print(f"✅ PROJET #3 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")