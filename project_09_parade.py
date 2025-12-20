# src/projects/project_09_grande_parade.py
"""
PROJET #9: LA GRANDE PARADE
Robotarium Swarm - ANEM 2025
Spectacle chorégraphié en 7 tableaux - Expérience visuelle complète
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project09GrandeParade:
    """Implémentation du projet La Grande Parade."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_entree_militaire': 60,      # 0:00-1:00
            '2_tempete_sable': 60,         # 1:00-2:00
            '3_vagues_ocean': 60,          # 2:00-3:00
            '4_spirale_hypnotique': 60,    # 3:00-4:00
            '5_feu_artifice': 60,          # 4:00-5:00
            '6_formations_geo': 60,        # 5:00-6:00
            '7_coeur_final': 60            # 6:00-7:00
        }
        
        print(f"🎪 PROJET #9 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (7 minutes)")

    def phase_1_entree_militaire(self, duration=60):
        """Tableau 1: Entrée Militaire - Défilé synchronisé."""
        print("🎖️  Tableau 1: Entrée Militaire")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Formation militaire (5 rangées de 10 robots)
        base_positions = self._create_military_formation()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = base_positions.copy()
            
            # Animation de marche synchronisée
            # Effet de vague entre les rangées
            for row in range(5):
                row_offset = 0.02 * np.sin(2*np.pi*1.0*time_val + row*0.5)
                row_indices = list(range(row*10, (row+1)*10))
                positions[1, row_indices] += row_offset
            
            # Avancée progressive depuis la gauche
            entrance_progress = min(1.0, time_val / 10.0)  # 10s pour entrer complètement
            positions[0, :] -= (1.0 - entrance_progress) * 1.5
            
            yield positions, time_val

    def phase_2_tempete_sable(self, start_pos, duration=60):
        """Tableau 2: Tempête de Sable - Chaos contrôlé."""
        print("🌪️  Tableau 2: Tempête de Sable")
        
        start_time = self.phases['1_entree_militaire']
        steps = int(duration * config.FPS)
        
        # Transition vers le chaos
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = start_pos.copy()
            
            # Progression du chaos (0 à 1)
            chaos_factor = min(1.0, (time_val - start_time) / 20.0)
            
            # Application du chaos contrôlé
            for i in range(self.n):
                # Mouvement brownien avec amplitude croissante
                brownian_x = 0.3 * chaos_factor * np.sin(2*np.pi*0.8*time_val + i*0.7)
                brownian_y = 0.2 * chaos_factor * np.cos(2*np.pi*0.6*time_val + i*0.9)
                
                positions[0, i] += brownian_x
                positions[1, i] += brownian_y
            
            # Tourbillons contrôlés
            if chaos_factor > 0.5:
                vortex_centers = [(-0.8, 0.4), (0.8, -0.4)]
                for vx, vy in vortex_centers:
                    for i in range(self.n):
                        dx = positions[0, i] - vx
                        dy = positions[1, i] - vy
                        distance = np.sqrt(dx**2 + dy**2)
                        
                        if distance < 0.6:
                            # Force vortex
                            vortex_strength = 0.1 * (0.6 - distance) / 0.6
                            angle = np.arctan2(dy, dx)
                            vortex_x = -vortex_strength * np.sin(angle)
                            vortex_y = vortex_strength * np.cos(angle)
                            
                            positions[0, i] += vortex_x
                            positions[1, i] += vortex_y
            
            yield positions, time_val

    def phase_3_vagues_ocean(self, start_pos, duration=60):
        """Tableau 3: Vagues Océaniques - Onde propagée."""
        print("🌊 Tableau 3: Vagues Océaniques")
        
        start_time = self.phases['1_entree_militaire'] + self.phases['2_tempete_sable']
        steps = int(duration * config.FPS)
        
        # Formation de vagues
        wave_positions = self._create_wave_formation()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, wave_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation des vagues
            wave_speed = 0.5
            wave_frequency = 2.0
            wave_amplitude = 0.2
            
            for i in range(positions.shape[1]):
                x = positions[0, i]
                # Vague sinusoïdale se propageant de droite à gauche
                wave_offset = wave_amplitude * np.sin(wave_frequency * x - wave_speed * time_val)
                positions[1, i] += wave_offset
            
            yield positions, time_val

    def phase_4_spirale_hypnotique(self, start_pos, duration=60):
        """Tableau 4: Spirale Hypnotique - Rotation galactique."""
        print("🌀 Tableau 4: Spirale Hypnotique")
        
        start_time = self.phases['1_entree_militaire'] + self.phases['2_tempete_sable'] + self.phases['3_vagues_ocean']
        steps = int(duration * config.FPS)
        
        # Formation spirale
        spiral_positions = self._create_spiral_formation()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, spiral_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Rotation différentielle (comme une galaxie)
            center_x, center_y = 0.0, 0.0
            
            for i in range(positions.shape[1]):
                x = positions[0, i] - center_x
                y = positions[1, i] - center_y
                distance = np.sqrt(x**2 + y**2)
                
                # Vitesse angulaire décroissante avec la distance
                angular_speed = 0.8 / (1 + distance * 2)
                angle = angular_speed * time_val
                
                # Rotation
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                
                positions[0, i] = center_x + new_x
                positions[1, i] = center_y + new_y
            
            yield positions, time_val

    def phase_5_feu_artifice(self, start_pos, duration=60):
        """Tableau 5: Feu d'Artifice - Explosions multiples."""
        print("🎆 Tableau 5: Feu d'Artifice")
        
        start_time = self.phases['1_entree_militaire'] + self.phases['2_tempete_sable'] + self.phases['3_vagues_ocean'] + self.phases['4_spirale_hypnotique']
        steps = int(duration * config.FPS)
        
        # Simulation de feux d'artifice
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Gestion des explosions
            explosion_times = [5, 15, 25, 35, 45]  # Temps des explosions
            explosion_centers = [(-0.8, 0.6), (0.0, 0.8), (0.8, 0.6), (-0.4, 0.4), (0.4, 0.4)]
            
            robot_count = 0
            
            for exp_time, (center_x, center_y) in zip(explosion_times, explosion_centers):
                if time_val >= exp_time and time_val < exp_time + 10:  # 10s d'affichage par explosion
                    # État de l'explosion (0 à 1)
                    explosion_progress = (time_val - exp_time) / 10.0
                    
                    if explosion_progress <= 0.3:
                        # Phase d'expansion
                        n_sparks = min(15, self.n - robot_count)
                        if n_sparks > 0:
                            radius = 0.8 * explosion_progress / 0.3
                            angles = np.linspace(0, 2*np.pi, n_sparks)
                            
                            spark_x = center_x + radius * np.cos(angles)
                            spark_y = center_y + radius * np.sin(angles)
                            
                            positions[0, robot_count:robot_count+n_sparks] = spark_x
                            positions[1, robot_count:robot_count+n_sparks] = spark_y
                            robot_count += n_sparks
                    else:
                        # Phase de retombée
                        n_sparks = min(10, self.n - robot_count)
                        if n_sparks > 0:
                            fall_progress = (explosion_progress - 0.3) / 0.7
                            radius = 0.8 * (1 - fall_progress)
                            angles = np.linspace(0, 2*np.pi, n_sparks)
                            
                            spark_x = center_x + radius * np.cos(angles)
                            spark_y = center_y + radius * np.sin(angles) - fall_progress * 0.5
                            
                            positions[0, robot_count:robot_count+n_sparks] = spark_x
                            positions[1, robot_count:robot_count+n_sparks] = spark_y
                            robot_count += n_sparks
            
            # Robots restants en position aléatoire basse
            if robot_count < self.n:
                remaining = self.n - robot_count
                ground_x = np.random.uniform(-1.2, 1.2, remaining)
                ground_y = np.full(remaining, -0.8)
                positions[0, robot_count:] = ground_x
                positions[1, robot_count:] = ground_y
            
            yield positions, time_val

    def phase_6_formations_geo(self, start_pos, duration=60):
        """Tableau 6: Formation Géométrique - Transitions fluides."""
        print("🔷 Tableau 6: Formations Géométriques")
        
        start_time = self.phases['1_entree_militaire'] + self.phases['2_tempete_sable'] + self.phases['3_vagues_ocean'] + self.phases['4_spirale_hypnotique'] + self.phases['5_feu_artifice']
        steps = int(duration * config.FPS)
        
        # Séquence de formes géométriques
        shapes = [
            self._create_circle_formation(),
            self._create_square_formation(),
            self._create_triangle_formation(),
            self._create_hexagon_formation(),
            self._create_star_formation()
        ]
        
        shape_duration = duration / len(shapes)
        
        current_shape_idx = 0
        shape_start_time = start_time
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            
            # Changement de forme
            if time_val - shape_start_time >= shape_duration and current_shape_idx < len(shapes) - 1:
                current_shape_idx += 1
                shape_start_time = time_val
            
            # Transition entre formes
            shape_progress = (time_val - shape_start_time) / shape_duration
            current_shape = shapes[current_shape_idx]
            next_shape = shapes[min(current_shape_idx + 1, len(shapes) - 1)]
            
            # Interpolation entre formes
            positions = current_shape + (next_shape - current_shape) * min(shape_progress, 1.0)
            
            # Rotation lente
            angle = 0.1 * np.sin(2*np.pi*0.2*time_val)
            for i in range(positions.shape[1]):
                x, y = positions[0, i], positions[1, i]
                positions[0, i] = x * np.cos(angle) - y * np.sin(angle)
                positions[1, i] = x * np.sin(angle) + y * np.cos(angle)
            
            yield positions, time_val

    def phase_7_coeur_final(self, start_pos, duration=60):
        """Tableau 7: Cœur Final - Pulsation émotionnelle."""
        print("❤️  Tableau 7: Cœur Final")
        
        start_time = self.phases['1_entree_militaire'] + self.phases['2_tempete_sable'] + self.phases['3_vagues_ocean'] + self.phases['4_spirale_hypnotique'] + self.phases['5_feu_artifice'] + self.phases['6_formations_geo']
        steps = int(duration * config.FPS)
        
        # Formation en cœur
        heart_positions = self._create_heart_formation()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, heart_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de pulsation (battements de cœur)
            pulse_rate = 0.8  # Hz
            pulse_strength = 0.15
            
            pulse_factor = 1.0 + pulse_strength * np.sin(2*np.pi*pulse_rate*time_val)
            
            # Appliquer la pulsation depuis le centre
            center_x, center_y = 0.0, 0.0
            for i in range(positions.shape[1]):
                dx = positions[0, i] - center_x
                dy = positions[1, i] - center_y
                
                positions[0, i] = center_x + dx * pulse_factor
                positions[1, i] = center_y + dy * pulse_factor
            
            yield positions, time_val

    def _create_military_formation(self):
        """Crée une formation militaire (5x10)."""
        positions = np.zeros((2, self.n))
        
        rows = 5
        cols = self.n // rows
        remaining = self.n % rows
        
        robot_count = 0
        
        for row in range(rows):
            n_cols = cols + (1 if row < remaining else 0)
            if robot_count >= self.n:
                break
                
            for col in range(n_cols):
                if robot_count < self.n:
                    x = -1.2 + col * (2.4 / max(1, n_cols-1))
                    y = -0.6 + row * (1.2 / max(1, rows-1))
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        return positions

    def _create_wave_formation(self):
        """Crée une formation pour les vagues océaniques."""
        positions = np.zeros((2, self.n))
        
        # 10 colonnes de robots
        cols = 10
        rows = self.n // cols
        remaining = self.n % cols
        
        robot_count = 0
        
        for col in range(cols):
            n_rows = rows + (1 if col < remaining else 0)
            if robot_count >= self.n:
                break
                
            for row in range(n_rows):
                if robot_count < self.n:
                    x = -1.5 + col * (3.0 / max(1, cols-1))
                    y = -0.6 + row * (1.2 / max(1, n_rows-1))
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        return positions

    def _create_spiral_formation(self):
        """Crée une formation spirale."""
        positions = np.zeros((2, self.n))
        
        # Spirale de Vogel
        phi = (1 + np.sqrt(5)) / 2  # Nombre d'or
        angle_step = 2 * np.pi / phi**2
        
        for i in range(self.n):
            angle = i * angle_step
            radius = 0.1 * np.sqrt(i + 1)
            
            positions[0, i] = radius * np.cos(angle)
            positions[1, i] = radius * np.sin(angle)
        
        return positions

    def _create_circle_formation(self):
        """Crée une formation circulaire."""
        return self.base.circle(radius=0.7)

    def _create_square_formation(self):
        """Crée une formation carrée."""
        positions = np.zeros((2, self.n))
        
        side_length = 1.2
        robots_per_side = self.n // 4
        remaining = self.n % 4
        
        robot_count = 0
        
        # Côtés du carré
        sides = [
            np.linspace(-side_length/2, side_length/2, robots_per_side),  # Bas
            np.linspace(-side_length/2, side_length/2, robots_per_side),  # Droite
            np.linspace(side_length/2, -side_length/2, robots_per_side),  # Haut
            np.linspace(side_length/2, -side_length/2, robots_per_side)   # Gauche
        ]
        
        for i, side in enumerate(sides):
            n_side = robots_per_side + (1 if i < remaining else 0)
            if robot_count >= self.n:
                break
                
            for j in range(n_side):
                if robot_count < self.n:
                    if i == 0:  # Bas
                        positions[0, robot_count] = side[j]
                        positions[1, robot_count] = -side_length/2
                    elif i == 1:  # Droite
                        positions[0, robot_count] = side_length/2
                        positions[1, robot_count] = side[j]
                    elif i == 2:  # Haut
                        positions[0, robot_count] = side[j]
                        positions[1, robot_count] = side_length/2
                    else:  # Gauche
                        positions[0, robot_count] = -side_length/2
                        positions[1, robot_count] = side[j]
                    
                    robot_count += 1
        
        return positions

    def _create_triangle_formation(self):
        """Crée une formation triangulaire."""
        positions = np.zeros((2, self.n))
        
        # Triangle équilatéral
        height = 1.4
        side = height * 2 / np.sqrt(3)
        
        robots_per_side = self.n // 3
        remaining = self.n % 3
        
        robot_count = 0
        
        # Sommets du triangle
        vertices = [
            (0, height/2),                    # Haut
            (-side/2, -height/2),             # Bas gauche
            (side/2, -height/2)               # Bas droit
        ]
        
        for i in range(3):
            n_side = robots_per_side + (1 if i < remaining else 0)
            if robot_count >= self.n:
                break
                
            start_vertex = vertices[i]
            end_vertex = vertices[(i + 1) % 3]
            
            for j in range(n_side):
                if robot_count < self.n:
                    t = j / max(1, n_side - 1)
                    x = start_vertex[0] + t * (end_vertex[0] - start_vertex[0])
                    y = start_vertex[1] + t * (end_vertex[1] - start_vertex[1])
                    
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        return positions

    def _create_hexagon_formation(self):
        """Crée une formation hexagonale."""
        positions = np.zeros((2, self.n))
        
        radius = 0.8
        vertices = 6
        
        robots_per_side = self.n // vertices
        remaining = self.n % vertices
        
        robot_count = 0
        
        for i in range(vertices):
            n_side = robots_per_side + (1 if i < remaining else 0)
            if robot_count >= self.n:
                break
                
            angle1 = 2 * np.pi * i / vertices
            angle2 = 2 * np.pi * (i + 1) / vertices
            
            for j in range(n_side):
                if robot_count < self.n:
                    t = j / max(1, n_side - 1)
                    angle = angle1 + t * (angle2 - angle1)
                    
                    # Légère réduction pour les côtés
                    side_radius = radius * 0.95
                    
                    x = side_radius * np.cos(angle)
                    y = side_radius * np.sin(angle)
                    
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        return positions

    def _create_star_formation(self):
        """Crée une formation en étoile."""
        return self.base.star_improved(n_points=8, outer_radius=0.8, inner_radius=0.4)

    def _create_heart_formation(self):
        """Crée une formation en cœur."""
        positions = np.zeros((2, self.n))
        
        scale = 0.6
        
        for i in range(self.n):
            t = 2 * np.pi * i / self.n
            x = scale * 16 * np.sin(t)**3 / 16
            y = scale * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)) / 16
            
            positions[0, i] = x
            positions[1, i] = y
        
        return positions

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #9: LA GRANDE PARADE")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = self._get_phase_display_name(phase_name)
            
            print(f"\n🎪 Début {display_name} ({duration}s, {phase_frames} frames)")
            
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
            
            print(f"✅ {display_name} terminé")
        
        print("=" * 60)
        print(f"✅ PROJET #9 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")

    def _get_phase_display_name(self, phase_name):
        """Retourne le nom d'affichage pour chaque phase."""
        names = {
            '1_entree_militaire': 'Entrée Militaire',
            '2_tempete_sable': 'Tempête de Sable',
            '3_vagues_ocean': 'Vagues Océaniques',
            '4_spirale_hypnotique': 'Spirale Hypnotique',
            '5_feu_artifice': 'Feu d\'Artifice',
            '6_formations_geo': 'Formations Géométriques',
            '7_coeur_final': 'Cœur Final'
        }
        return names.get(phase_name, phase_name)