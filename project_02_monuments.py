# src/projects/project_02_monuments.py
"""
PROJET #2: MONUMENTS ICONIQUES DU NIGER
Robotarium Swarm - ANEM 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project02Monuments:
    """Implémentation du projet Monuments Iconiques du Niger."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_mosquee_agadez': 80,      # 1:20
            '2_girafe_niger': 80,        # 1:20  
            '3_croix_agadez': 80         # 1:20
        }
        
        print(f"🚀 PROJET #2 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (4 minutes)")

    def phase_1_mosquee_agadez(self, duration=80):
        """Phase 1: Mosquée d'Agadez - Monument historique."""
        print("🕌 Phase 1: Mosquée d'Agadez")
        
        # Formation de la mosquée d'Agadez
        target_mosquee = self._create_mosquee_agadez()
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Transition depuis positions aléatoires
        start_pos = self.base.random_positions()
        
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_mosquee, 20)  # 20s de transition
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Maintenir la formation (60s)
        maintain_steps = steps - int(20 * config.FPS)
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Légère animation de pulsation
            pulse = 1.0 + 0.05 * np.sin(2 * np.pi * 0.2 * time_val)
            center = np.mean(current_pos, axis=1, keepdims=True)
            animated_pos = center + (current_pos - center) * pulse
            
            yield animated_pos, time_val

    def phase_2_girafe_niger(self, start_pos, duration=80):
        """Phase 2: Girafe du Niger - Symbole de la faune."""
        print("🦒 Phase 2: Girafe du Niger")
        
        # Formation de la girafe
        target_girafe = self._create_girafe_silhouette()
        
        start_time = self.phases['1_mosquee_agadez']
        
        # Transition depuis mosquée (20s)
        steps_transition = int(20 * config.FPS)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_girafe, 20)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Animation de la girafe qui marche (60s)
        maintain_steps = int(duration * config.FPS) - steps_transition
        base_positions = target_girafe.copy()
        
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Animation de marche (déplacement latéral doux)
            walk_offset = 0.1 * np.sin(2 * np.pi * 0.3 * time_val)
            animated_pos = base_positions.copy()
            animated_pos[0, :] += walk_offset
            
            # Légère pulsation du corps
            pulse = 1.0 + 0.03 * np.sin(2 * np.pi * 0.5 * time_val)
            center = np.mean(animated_pos, axis=1, keepdims=True)
            animated_pos = center + (animated_pos - center) * pulse
            
            yield animated_pos, time_val

    def phase_3_croix_agadez(self, start_pos, duration=80):
        """Phase 3: Croix d'Agadez - Symbole touareg."""
        print("✝️  Phase 3: Croix d'Agadez")
        
        # Formation de la croix d'Agadez
        target_croix = self._create_croix_agadez()
        
        start_time = self.phases['1_mosquee_agadez'] + self.phases['2_girafe_niger']
        
        # Transition depuis girafe (20s)
        steps_transition = int(20 * config.FPS)
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_croix, 20)
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val
            current_pos = intermediate_pos
        
        # Animation de rotation (60s)
        maintain_steps = int(duration * config.FPS) - steps_transition
        base_positions = target_croix.copy()
        
        for step in range(maintain_steps):
            time_val = start_time + 20 + step / config.FPS
            
            # Rotation lente de la croix
            angle = 2 * np.pi * 0.1 * time_val  # Rotation complète toutes les 10s
            
            # Centre de rotation
            center_x = np.mean(base_positions[0, :])
            center_y = np.mean(base_positions[1, :])
            
            # Appliquer la rotation
            rotated_pos = base_positions.copy()
            for i in range(self.n):
                x = base_positions[0, i] - center_x
                y = base_positions[1, i] - center_y
                
                # Rotation
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                
                rotated_pos[0, i] = new_x + center_x
                rotated_pos[1, i] = new_y + center_y
            
            yield rotated_pos, time_val

    def _create_mosquee_agadez(self):
        """Crée la formation de la Mosquée d'Agadez."""
        positions = np.zeros((2, self.n))
        
        # Répartition des robots
        n_base = self.n // 3      # Base rectangulaire
        n_minaret = self.n // 3   # Minaret
        n_details = self.n - 2 * (self.n // 3)  # Détails
        
        robot_count = 0
        
        # BASE RECTANGULAIRE
        if robot_count < self.n:
            base_robots = min(n_base, self.n - robot_count)
            # Rectangle pour la base
            x_base = np.linspace(-0.6, 0.6, int(np.sqrt(base_robots)))
            y_base = np.linspace(-0.3, -0.1, int(np.sqrt(base_robots)))
            xx, yy = np.meshgrid(x_base, y_base)
            
            for i in range(min(base_robots, xx.size)):
                if robot_count < self.n:
                    positions[0, robot_count] = xx.flatten()[i]
                    positions[1, robot_count] = yy.flatten()[i]
                    robot_count += 1
        
        # MINARET PYRAMIDAL
        if robot_count < self.n:
            minaret_robots = min(n_minaret, self.n - robot_count)
            # Pyramide pour le minaret
            levels = 4
            robots_per_level = minaret_robots // levels
            
            for level in range(levels):
                level_robots = robots_per_level if level < levels - 1 else minaret_robots - level * robots_per_level
                width = 0.4 * (1 - level/levels)  # Rétrécissement
                height = 0.1 + level * 0.15
                
                x_minaret = np.linspace(-width/2, width/2, level_robots)
                y_minaret = np.full(level_robots, height)
                
                for i in range(level_robots):
                    if robot_count < self.n:
                        positions[0, robot_count] = x_minaret[i]
                        positions[1, robot_count] = y_minaret[i]
                        robot_count += 1
        
        # DÉTAILS ARCHITECTURAUX
        if robot_count < self.n:
            detail_robots = min(n_details, self.n - robot_count)
            # Ajouter des détails (torons, etc.)
            x_details = np.random.uniform(-0.7, 0.7, detail_robots)
            y_details = np.random.uniform(-0.2, 0.5, detail_robots)
            
            for i in range(detail_robots):
                if robot_count < self.n:
                    positions[0, robot_count] = x_details[i]
                    positions[1, robot_count] = y_details[i]
                    robot_count += 1
        
        return positions

    def _create_girafe_silhouette(self):
        """Crée la formation de la girafe du Niger."""
        positions = np.zeros((2, self.n))
        
        # Répartition anatomique
        n_tete = max(3, self.n // 15)        # Tête
        n_cou = max(8, self.n // 6)          # Cou
        n_corps = max(10, self.n // 5)       # Corps
        n_pattes = 4 * max(2, self.n // 20)  # 4 pattes
        n_queue = max(2, self.n // 25)       # Queue
        n_rest = self.n - (n_tete + n_cou + n_corps + n_pattes + n_queue)
        
        robot_count = 0
        
        # TÊTE
        if robot_count < self.n:
            # Cercle pour la tête
            angles = np.linspace(0, 2*np.pi, n_tete, endpoint=False)
            positions[0, robot_count:robot_count+n_tete] = 0.3 + 0.08 * np.cos(angles)
            positions[1, robot_count:robot_count+n_tete] = 0.6 + 0.08 * np.sin(angles)
            robot_count += n_tete
        
        # COU (courbe en S)
        if robot_count < self.n:
            t_cou = np.linspace(0, 1, n_cou)
            # Courbe en S pour le cou
            x_cou = 0.15 * np.sin(2*np.pi*t_cou)  # Légère courbure
            y_cou = 0.6 - t_cou * 0.8  # Du haut vers le bas
            
            positions[0, robot_count:robot_count+n_cou] = x_cou
            positions[1, robot_count:robot_count+n_cou] = y_cou
            robot_count += n_cou
        
        # CORPS (ellipse)
        if robot_count < self.n:
            angles_corps = np.linspace(0, 2*np.pi, n_corps, endpoint=False)
            positions[0, robot_count:robot_count+n_corps] = -0.1 + 0.3 * np.cos(angles_corps)
            positions[1, robot_count:robot_count+n_corps] = -0.2 + 0.2 * np.sin(angles_corps)
            robot_count += n_corps
        
        # PATTES
        if robot_count < self.n:
            patte_positions = [
                (-0.3, -0.2, -0.3, -0.6),   # Patte avant gauche
                (-0.1, -0.2, -0.1, -0.6),   # Patte avant droite
                (-0.4, -0.2, -0.4, -0.6),   # Patte arrière gauche  
                (-0.0, -0.2, -0.0, -0.6)    # Patte arrière droite
            ]
            
            robots_par_patte = n_pattes // 4
            for patte in patte_positions:
                if robot_count < self.n:
                    patte_robots = min(robots_par_patte, self.n - robot_count)
                    x_patte = np.linspace(patte[0], patte[2], patte_robots)
                    y_patte = np.linspace(patte[1], patte[3], patte_robots)
                    
                    positions[0, robot_count:robot_count+patte_robots] = x_patte
                    positions[1, robot_count:robot_count+patte_robots] = y_patte
                    robot_count += patte_robots
        
        # QUEUE
        if robot_count < self.n:
            queue_robots = min(n_queue, self.n - robot_count)
            x_queue = np.linspace(-0.5, -0.6, queue_robots)
            y_queue = np.linspace(-0.1, -0.3, queue_robots)
            
            positions[0, robot_count:robot_count+queue_robots] = x_queue
            positions[1, robot_count:robot_count+queue_robots] = y_queue
            robot_count += queue_robots
        
        # RESTE (taches, etc.)
        if robot_count < self.n:
            rest_robots = self.n - robot_count
            # Ajouter des points aléatoires pour les taches
            x_rest = np.random.uniform(-0.4, 0.1, rest_robots)
            y_rest = np.random.uniform(-0.3, 0.3, rest_robots)
            
            positions[0, robot_count:] = x_rest
            positions[1, robot_count:] = y_rest
        
        return positions

    def _create_croix_agadez(self):
        """Crée la formation de la Croix d'Agadez (12 branches)."""
        positions = np.zeros((2, self.n))
        
        n_branches = 12
        robots_par_branche = self.n // (n_branches + 1)  # +1 pour le centre
        
        robot_count = 0
        
        # CENTRE DE LA CROIX
        if robot_count < self.n:
            centre_robots = min(8, self.n - robot_count)
            # Cercle central
            angles_centre = np.linspace(0, 2*np.pi, centre_robots, endpoint=False)
            positions[0, robot_count:robot_count+centre_robots] = 0.1 * np.cos(angles_centre)
            positions[1, robot_count:robot_count+centre_robots] = 0.1 * np.sin(angles_centre)
            robot_count += centre_robots
        
        # 12 BRANCHES
        for branche in range(n_branches):
            if robot_count >= self.n:
                break
                
            branche_robots = min(robots_par_branche, self.n - robot_count)
            angle = branche * (2 * np.pi / n_branches)
            
            # Longueur de la branche
            longueur = 0.7
            
            # Points le long de la branche
            t = np.linspace(0.1, longueur, branche_robots)
            x_branche = t * np.cos(angle)
            y_branche = t * np.sin(angle)
            
            positions[0, robot_count:robot_count+branche_robots] = x_branche
            positions[1, robot_count:robot_count+branche_robots] = y_branche
            robot_count += branche_robots
        
        return positions

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #2: MONUMENTS ICONIQUES DU NIGER")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = phase_name.replace('_', ' ').replace('1 ', '').replace('2 ', '').replace('3 ', '')
            
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
        print(f"✅ PROJET #2 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")