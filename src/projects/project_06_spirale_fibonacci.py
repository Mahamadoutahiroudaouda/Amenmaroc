# src/projects/project_06_spirale_fibonacci.py
"""
PROJET #6: SPIRALE D'OR DE FIBONACCI
Robotarium Swarm - ANEM 2025
Formation d'une spirale logarithmique basée sur le nombre d'or φ = 1.618
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project06SpiraleFibonacci:
    """Implémentation du projet Spirale d'Or de Fibonacci."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_construction': 50,      # 0:00-0:50
            '2_rotation': 50,          # 0:50-1:40
            '3_pulsation': 40,         # 1:40-2:20
            '4_transformation': 40     # 2:20-3:00
        }
        
        # Constantes mathématiques
        self.phi = (1 + np.sqrt(5)) / 2  # Nombre d'or
        self.angle_or = 2 * np.pi / self.phi**2  # Angle d'or en radians
        
        print(f"🚀 PROJET #6 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (3 minutes)")
        print(f"🧮 Nombre d'or φ = {self.phi:.6f}")

    def phase_1_construction(self, duration=50):
        """Phase 1: Construction progressive de la spirale."""
        print("🌀 Phase 1: Construction de la spirale Fibonacci")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Position finale de la spirale complète
        target_spiral = self._create_fibonacci_spiral()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Progression de la construction (0 à 1)
            progression = step / steps
            
            # Nombre de robots à afficher progressivement
            n_visible = int(self.n * progression)
            
            if n_visible > 0:
                # Prendre les premiers n_visible robots de la spirale complète
                positions[:, :n_visible] = target_spiral[:, :n_visible]
                
                # Positionner les robots restants au centre
                if n_visible < self.n:
                    positions[0, n_visible:] = 0.0
                    positions[1, n_visible:] = 0.0
            
            yield positions, time_val

    def phase_2_rotation(self, start_pos, duration=50):
        """Phase 2: Rotation galactique avec vitesse différentielle."""
        print("🌌 Phase 2: Rotation galactique")
        
        start_time = self.phases['1_construction']
        steps = int(duration * config.FPS)
        
        base_positions = self._create_fibonacci_spiral()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = base_positions.copy()
            
            # Appliquer la rotation différentielle
            for i in range(self.n):
                x = base_positions[0, i]
                y = base_positions[1, i]
                
                # Distance du centre
                r = np.sqrt(x**2 + y**2)
                
                # Vitesse angulaire décroissante avec la distance
                # (comme dans les galaxies spirales)
                angular_speed = 0.5 / (1 + r*3)
                angle = angular_speed * time_val
                
                # Rotation
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                
                positions[0, i] = new_x
                positions[1, i] = new_y
            
            yield positions, time_val

    def phase_3_pulsation(self, start_pos, duration=40):
        """Phase 3: Pulsation de la spirale."""
        print("💓 Phase 3: Pulsation")
        
        start_time = self.phases['1_construction'] + self.phases['2_rotation']
        steps = int(duration * config.FPS)
        
        base_positions = self._create_fibonacci_spiral()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = base_positions.copy()
            
            # Effet de pulsation (respiration)
            pulse_factor = 1.0 + 0.2 * np.sin(2 * np.pi * 0.5 * time_val)
            
            # Appliquer la pulsation
            center = np.array([[0.0], [0.0]])  # Centre à l'origine
            positions = center + (positions - center) * pulse_factor
            
            yield positions, time_val

    def phase_4_transformation(self, start_pos, duration=40):
        """Phase 4: Transformation en rectangles et carrés dorés."""
        print("🔷 Phase 4: Transformation géométrique")
        
        start_time = self.phases['1_construction'] + self.phases['2_rotation'] + self.phases['3_pulsation']
        steps = int(duration * config.FPS)
        
        # Cible : rectangles dorés imbriqués
        target_rectangles = self._create_rectangles_dores()
        
        # Transition depuis la spirale
        for step, intermediate_pos in enumerate(
            self.transitions.interpolate_positions(start_pos, target_rectangles, duration, 'ease_in_out')
        ):
            time_val = start_time + step / config.FPS
            yield intermediate_pos, time_val

    def _create_fibonacci_spiral(self):
        """Crée une spirale de Fibonacci (spirale d'or)."""
        positions = np.zeros((2, self.n))
        
        # Méthode de Vogel pour une distribution optimale
        for i in range(self.n):
            # Angle selon l'angle d'or
            theta = i * self.angle_or
            
            # Rayon selon une spirale logarithmique
            r = 0.1 * np.sqrt(i + 1)  # Spirale de Vogel
            
            # Coordonnées
            positions[0, i] = r * np.cos(theta)
            positions[1, i] = r * np.sin(theta)
        
        return positions

    def _create_rectangles_dores(self):
        """Crée une formation de rectangles dorés imbriqués."""
        positions = np.zeros((2, self.n))
        
        # Suite de Fibonacci
        fibonacci = self._generate_fibonacci(10)  # Générer les 10 premiers termes
        
        robot_count = 0
        current_x, current_y = 0.0, 0.0
        direction = 0  # 0: droite, 1: haut, 2: gauche, 3: bas
        
        for i in range(len(fibonacci) - 1):
            if robot_count >= self.n:
                break
                
            a = fibonacci[i] * 0.1   # Petit côté
            b = fibonacci[i+1] * 0.1 # Grand côté (suivant Fibonacci)
            
            # Nombre de robots pour ce rectangle
            n_rect = min(int(self.n * 0.7 / len(fibonacci)), self.n - robot_count)
            
            if n_rect > 0:
                # Créer les points du rectangle
                if direction == 0:  # Vers la droite
                    x_rect = np.linspace(current_x, current_x + b, int(np.sqrt(n_rect)))
                    y_rect = np.linspace(current_y, current_y + a, int(np.sqrt(n_rect)))
                    current_x += b
                elif direction == 1:  # Vers le haut
                    x_rect = np.linspace(current_x - a, current_x, int(np.sqrt(n_rect)))
                    y_rect = np.linspace(current_y, current_y + b, int(np.sqrt(n_rect)))
                    current_y += b
                elif direction == 2:  # Vers la gauche
                    x_rect = np.linspace(current_x - b, current_x, int(np.sqrt(n_rect)))
                    y_rect = np.linspace(current_y - a, current_y, int(np.sqrt(n_rect)))
                    current_x -= b
                else:  # Vers le bas
                    x_rect = np.linspace(current_x, current_x + a, int(np.sqrt(n_rect)))
                    y_rect = np.linspace(current_y - b, current_y, int(np.sqrt(n_rect)))
                    current_y -= b
                
                # Grille pour le rectangle
                xx, yy = np.meshgrid(x_rect, y_rect)
                
                # Placer les robots
                rect_positions = np.array([xx.flatten(), yy.flatten()])
                n_place = min(n_rect, rect_positions.shape[1])
                
                positions[0, robot_count:robot_count+n_place] = rect_positions[0, :n_place]
                positions[1, robot_count:robot_count+n_place] = rect_positions[1, :n_place]
                robot_count += n_place
                
                # Changer de direction
                direction = (direction + 1) % 4
        
        # Si des robots restent, les placer en spirale au centre
        if robot_count < self.n:
            remaining = self.n - robot_count
            spiral_remaining = self._create_fibonacci_spiral()[:, :remaining]
            positions[0, robot_count:] = spiral_remaining[0, :]
            positions[1, robot_count:] = spiral_remaining[1, :]
        
        return positions

    def _generate_fibonacci(self, n):
        """Génère les n premiers termes de la suite de Fibonacci."""
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib

    def _create_suite_carres(self):
        """Crée une formation basée sur la suite de carrés de Fibonacci."""
        positions = np.zeros((2, self.n))
        
        # Suite de Fibonacci pour les tailles des carrés
        fib = self._generate_fibonacci(8)  # 8 termes
        fib = [f for f in fib if f > 0]  # Enlever le 0
        
        robot_count = 0
        current_x, current_y = 0.0, 0.0
        
        for i, size in enumerate(fib):
            if robot_count >= self.n:
                break
                
            taille_carre = size * 0.08
            n_carre = min(int(self.n / len(fib)), self.n - robot_count)
            
            if n_carre > 0:
                # Créer un carré
                cote = int(np.sqrt(n_carre))
                if cote < 2: cote = 2
                
                x_carre = np.linspace(current_x, current_x + taille_carre, cote)
                y_carre = np.linspace(current_y, current_y + taille_carre, cote)
                
                xx, yy = np.meshgrid(x_carre, y_carre)
                carre_positions = np.array([xx.flatten(), yy.flatten()])
                
                n_place = min(n_carre, carre_positions.shape[1])
                positions[0, robot_count:robot_count+n_place] = carre_positions[0, :n_place]
                positions[1, robot_count:robot_count+n_place] = carre_positions[1, :n_place]
                robot_count += n_place
                
                # Déplacer la position pour le prochain carré
                if i % 2 == 0:
                    current_x += taille_carre + 0.05
                else:
                    current_y += taille_carre + 0.05
        
        return positions

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #6: SPIRALE D'OR DE FIBONACCI")
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
        print(f"✅ PROJET #6 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")