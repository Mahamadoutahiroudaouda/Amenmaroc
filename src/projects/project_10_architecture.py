# src/projects/project_10_patrimoine_architectural.py
"""
PROJET #10: PATRIMOINE ARCHITECTURAL
Robotarium Swarm - ANEM 2025
Reconstruction virtuelle de l'architecture traditionnelle nigérienne
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project10PatrimoineArchitectural:
    """Implémentation du projet Patrimoine Architectural."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_case_haoussa': 75,        # 0:00-1:15
            '2_mosquee_zinder': 75,      # 1:15-2:30
            '3_sultanat_zinder': 75,     # 2:30-3:45
            '4_village_fortifie': 75     # 3:45-5:00
        }
        
        # Matériaux traditionnels
        self.materials = {
            'banco': '#A0522D',      # Terre crue
            'pierre': '#8B7355',     # Grès local
            'bois': '#8B4513',       # Palmier doum
            'paille': '#D2B48C'      # Typha
        }
        
        print(f"🏛️  PROJET #10 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (5 minutes)")

    def phase_1_case_haoussa(self, duration=75):
        """Phase 1: Case Traditionnel Haoussa - Construction progressive."""
        print("🏠 Phase 1: Case Traditionnel Haoussa")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Formation finale de la case
        target_case = self._create_case_haoussa()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Construction progressive
            build_progress = step / steps
            
            # Étape 1: Fondations (0-25%)
            if build_progress < 0.25:
                foundation_progress = build_progress / 0.25
                n_foundation = int(self.n * 0.3 * foundation_progress)
                positions[:, :n_foundation] = target_case[:, :n_foundation]
            
            # Étape 2: Murs (25-60%)
            elif build_progress < 0.6:
                wall_progress = (build_progress - 0.25) / 0.35
                n_walls = int(self.n * 0.5 * wall_progress)
                positions[:, :int(self.n*0.3)+n_walls] = target_case[:, :int(self.n*0.3)+n_walls]
            
            # Étape 3: Toit (60-90%)
            elif build_progress < 0.9:
                roof_progress = (build_progress - 0.6) / 0.3
                n_roof = int(self.n * 0.2 * roof_progress)
                start_idx = int(self.n * 0.8)
                positions[:, start_idx:start_idx+n_roof] = target_case[:, start_idx:start_idx+n_roof]
                positions[:, :int(self.n*0.8)] = target_case[:, :int(self.n*0.8)]
            
            # Étape 4: Finitions (90-100%)
            else:
                positions = target_case
            
            yield positions, time_val

    def phase_2_mosquee_zinder(self, start_pos, duration=75):
        """Phase 2: Mosquée de Zinder - Architecture soudano-sahélienne."""
        print("🕌 Phase 2: Mosquée de Zinder")
        
        start_time = self.phases['1_case_haoussa']
        steps = int(duration * config.FPS)
        
        # Formation de la mosquée
        mosque_positions = self._create_mosquee_zinder()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, mosque_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation d'appel à la prière (ondulation)
            if step % 40 < 20:
                # Légère ondulation des torons
                for i in range(positions.shape[1]):
                    if i < positions.shape[1] * 0.3:  # Torons
                        wave_offset = 0.02 * np.sin(2*np.pi*0.3*time_val + i*0.2)
                        positions[1, i] += wave_offset
            
            yield positions, time_val

    def phase_3_sultanat_zinder(self, start_pos, duration=75):
        """Phase 3: Sultanat de Zinder (Palais) - Architecture palatiale."""
        print("🏰 Phase 3: Sultanat de Zinder (Palais)")
        
        start_time = self.phases['1_case_haoussa'] + self.phases['2_mosquee_zinder']
        steps = int(duration * config.FPS)
        
        # Formation du palais
        palace_positions = self._create_sultanat_zinder()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, palace_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de zoom progressif sur les détails
            zoom_factor = 1.0 + 0.1 * np.sin(2*np.pi*0.2*time_val)
            center = np.array([[0.0], [0.0]])
            positions = center + (positions - center) * zoom_factor
            
            yield positions, time_val

    def phase_4_village_fortifie(self, start_pos, duration=75):
        """Phase 4: Village fortifié (Kasbah) - Vue aérienne rotative."""
        print("🏘️  Phase 4: Village Fortifié (Kasbah)")
        
        start_time = self.phases['1_case_haoussa'] + self.phases['2_mosquee_zinder'] + self.phases['3_sultanat_zinder']
        steps = int(duration * config.FPS)
        
        # Formation du village
        village_positions = self._create_village_fortifie()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, village_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de rotation (vue aérienne)
            rotation_angle = 0.05 * time_val
            center_x, center_y = 0.0, 0.0
            
            for i in range(positions.shape[1]):
                x = positions[0, i] - center_x
                y = positions[1, i] - center_y
                
                new_x = x * np.cos(rotation_angle) - y * np.sin(rotation_angle)
                new_y = x * np.sin(rotation_angle) + y * np.cos(rotation_angle)
                
                positions[0, i] = center_x + new_x
                positions[1, i] = center_y + new_y
            
            yield positions, time_val

    def _create_case_haoussa(self):
        """Crée la formation d'une case traditionnelle haoussa."""
        positions = np.zeros((2, self.n))
        
        robot_count = 0
        
        # Base circulaire (fondations)
        n_base = int(self.n * 0.3)
        if n_base > 0:
            t_base = np.linspace(0, 2*np.pi, n_base)
            base_x = 0.0 + 0.4 * np.cos(t_base)
            base_y = -0.5 + 0.4 * np.sin(t_base)
            positions[0, robot_count:robot_count+n_base] = base_x
            positions[1, robot_count:robot_count+n_base] = base_y
            robot_count += n_base
        
        # Murs circulaires
        n_walls = int(self.n * 0.5)
        if n_walls > 0:
            # Mur extérieur
            t_wall = np.linspace(0, 2*np.pi, n_walls)
            wall_x = 0.0 + 0.35 * np.cos(t_wall)
            wall_y = -0.2 + 0.35 * np.sin(t_wall)
            positions[0, robot_count:robot_count+n_walls] = wall_x
            positions[1, robot_count:robot_count+n_walls] = wall_y
            robot_count += n_walls
        
        # Toit conique
        n_roof = self.n - robot_count
        if n_roof > 0:
            # Base du toit
            t_roof_base = np.linspace(0, 2*np.pi, n_roof//2)
            roof_base_x = 0.0 + 0.3 * np.cos(t_roof_base)
            roof_base_y = 0.1 + 0.3 * np.sin(t_roof_base)
            
            # Sommet du toit
            t_roof_top = np.linspace(0, 2*np.pi, n_roof - n_roof//2)
            roof_top_x = 0.0 + 0.1 * np.cos(t_roof_top)
            roof_top_y = 0.4 + 0.1 * np.sin(t_roof_top)
            
            roof_x = np.concatenate([roof_base_x, roof_top_x])
            roof_y = np.concatenate([roof_base_y, roof_top_y])
            
            n_place = min(len(roof_x), self.n - robot_count)
            positions[0, robot_count:robot_count+n_place] = roof_x[:n_place]
            positions[1, robot_count:robot_count+n_place] = roof_y[:n_place]
        
        return positions

    def _create_mosquee_zinder(self):
        """Crée la formation de la Mosquée de Zinder."""
        positions = np.zeros((2, self.n))
        
        robot_count = 0
        
        # Base rectangulaire
        n_base = int(self.n * 0.2)
        if n_base > 0:
            # Périmètre de la base
            base_points = []
            # Bas
            base_points.extend(zip(np.linspace(-0.6, 0.6, n_base//4), np.full(n_base//4, -0.4)))
            # Droite
            base_points.extend(zip(np.full(n_base//4, 0.6), np.linspace(-0.4, 0.2, n_base//4)))
            # Haut
            base_points.extend(zip(np.linspace(0.6, -0.6, n_base//4), np.full(n_base//4, 0.2)))
            # Gauche
            base_points.extend(zip(np.full(n_base//4, -0.6), np.linspace(0.2, -0.4, n_base//4)))
            
            for i, (x, y) in enumerate(base_points[:n_base]):
                if robot_count < self.n:
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        # Minaret pyramidal
        n_minaret = int(self.n * 0.4)
        if n_minaret > 0:
            # Base du minaret
            minaret_width = 0.3
            minaret_height = 0.8
            
            # Faces du minaret
            for face in range(4):
                n_face = n_minaret // 4
                for i in range(n_face):
                    if robot_count < self.n:
                        if face == 0:  # Face avant
                            x = -minaret_width/2 + (minaret_width/(n_face-1)) * i
                            y = -0.4 + (minaret_height/(n_face-1)) * i
                        elif face == 1:  # Face droite
                            x = minaret_width/2 - (minaret_width/(n_face-1)) * i
                            y = -0.4 + (minaret_height/(n_face-1)) * i
                        elif face == 2:  # Face arrière
                            x = -minaret_width/2 + (minaret_width/(n_face-1)) * i
                            y = 0.4 - (minaret_height/(n_face-1)) * i
                        else:  # Face gauche
                            x = minaret_width/2 - (minaret_width/(n_face-1)) * i
                            y = 0.4 - (minaret_height/(n_face-1)) * i
                        
                        positions[0, robot_count] = x
                        positions[1, robot_count] = y
                        robot_count += 1
        
        # Torons (poutres en bois)
        n_torons = int(self.n * 0.3)
        if n_torons > 0:
            # Torons horizontaux sur la façade
            for i in range(n_torons):
                if robot_count < self.n:
                    x = -0.5 + (1.0/(n_torons-1)) * i
                    y = -0.2 + 0.1 * np.sin(i * 0.5)  # Légère courbure
                    positions[0, robot_count] = x
                    positions[1, robot_count] = y
                    robot_count += 1
        
        # Détails décoratifs
        n_details = self.n - robot_count
        if n_details > 0:
            # Motifs géométriques
            t_details = np.linspace(0, 2*np.pi, n_details)
            details_x = 0.0 + 0.2 * np.cos(t_details)
            details_y = 0.0 + 0.1 * np.sin(t_details)
            positions[0, robot_count:] = details_x[:n_details]
            positions[1, robot_count:] = details_y[:n_details]
        
        return positions

    def _create_sultanat_zinder(self):
        """Crée la formation du Sultanat de Zinder (Palais)."""
        positions = np.zeros((2, self.n))
        
        robot_count = 0
        
        # Cours intérieures multiples
        n_courtyards = 3
        courtyard_centers = [(-0.4, 0.0), (0.4, 0.0), (0.0, 0.3)]
        courtyard_sizes = [0.3, 0.25, 0.2]
        
        for i, (center_x, center_y) in enumerate(courtyard_centers):
            if i >= n_courtyards:
                break
                
            n_courtyard = int(self.n * 0.2)
            if n_courtyard > 0 and robot_count < self.n:
                size = courtyard_sizes[i]
                t_court = np.linspace(0, 2*np.pi, n_courtyard)
                court_x = center_x + size * np.cos(t_court)
                court_y = center_y + size * np.sin(t_court)
                
                n_place = min(n_courtyard, self.n - robot_count)
                positions[0, robot_count:robot_count+n_place] = court_x[:n_place]
                positions[1, robot_count:robot_count+n_place] = court_y[:n_place]
                robot_count += n_place
        
        # Bâtiments principaux
        n_buildings = int(self.n * 0.4)
        if n_buildings > 0:
            # Formes rectangulaires pour les bâtiments
            building_shapes = [
                (-0.7, -0.3, 0.2, 0.4),   # x, y, width, height
                (0.5, -0.2, 0.25, 0.3),
                (-0.2, 0.5, 0.3, 0.2)
            ]
            
            for building in building_shapes:
                x, y, w, h = building
                n_building = n_buildings // len(building_shapes)
                
                # Périmètre du bâtiment
                perimeter_points = []
                # Bas
                perimeter_points.extend(zip(np.linspace(x-w/2, x+w/2, n_building//4), np.full(n_building//4, y-h/2)))
                # Droite
                perimeter_points.extend(zip(np.full(n_building//4, x+w/2), np.linspace(y-h/2, y+h/2, n_building//4)))
                # Haut
                perimeter_points.extend(zip(np.linspace(x+w/2, x-w/2, n_building//4), np.full(n_building//4, y+h/2)))
                # Gauche
                perimeter_points.extend(zip(np.full(n_building//4, x-w/2), np.linspace(y+h/2, y-h/2, n_building//4)))
                
                for px, py in perimeter_points[:n_building]:
                    if robot_count < self.n:
                        positions[0, robot_count] = px
                        positions[1, robot_count] = py
                        robot_count += 1
        
        # Détails architecturaux
        n_details = int(self.n * 0.3)
        if n_details > 0:
            # Colonnes, arcs, décorations
            t_details = np.linspace(0, 2*np.pi, n_details)
            details_x = 0.0 + 0.5 * np.cos(t_details)
            details_y = 0.0 + 0.3 * np.sin(t_details)
            
            n_place = min(n_details, self.n - robot_count)
            positions[0, robot_count:robot_count+n_place] = details_x[:n_place]
            positions[1, robot_count:robot_count+n_place] = details_y[:n_place]
            robot_count += n_place
        
        # Éléments restants
        if robot_count < self.n:
            remaining = self.n - robot_count
            # Points aléatoires pour compléter
            random_x = np.random.uniform(-0.8, 0.8, remaining)
            random_y = np.random.uniform(-0.6, 0.6, remaining)
            positions[0, robot_count:] = random_x
            positions[1, robot_count:] = random_y
        
        return positions

    def _create_village_fortifie(self):
        """Crée la formation d'un village fortifié (Kasbah)."""
        positions = np.zeros((2, self.n))
        
        robot_count = 0
        
        # Enceinte défensive circulaire
        n_enceinte = int(self.n * 0.3)
        if n_enceinte > 0:
            t_enceinte = np.linspace(0, 2*np.pi, n_enceinte)
            enceinte_x = 0.0 + 0.7 * np.cos(t_enceinte)
            enceinte_y = 0.0 + 0.7 * np.sin(t_enceinte)
            positions[0, robot_count:robot_count+n_enceinte] = enceinte_x
            positions[1, robot_count:robot_count+n_enceinte] = enceinte_y
            robot_count += n_enceinte
        
        # Tours de guet
        n_towers = 4
        tower_angles = [0, np.pi/2, np.pi, 3*np.pi/2]
        
        for angle in tower_angles:
            n_tower = int(self.n * 0.1)
            if n_tower > 0 and robot_count < self.n:
                # Position de la tour
                tower_x = 0.7 * np.cos(angle)
                tower_y = 0.7 * np.sin(angle)
                
                # Formation carrée pour la tour
                tower_size = 0.15
                t_tower = np.linspace(0, 2*np.pi, n_tower)
                tower_points_x = tower_x + tower_size * np.cos(t_tower)
                tower_points_y = tower_y + tower_size * np.sin(t_tower)
                
                n_place = min(n_tower, self.n - robot_count)
                positions[0, robot_count:robot_count+n_place] = tower_points_x[:n_place]
                positions[1, robot_count:robot_count+n_place] = tower_points_y[:n_place]
                robot_count += n_place
        
        # Habitations à l'intérieur
        n_houses = int(self.n * 0.4)
        if n_houses > 0:
            # Cases circulaires réparties aléatoirement à l'intérieur
            for i in range(n_houses):
                if robot_count < self.n:
                    # Position aléatoire à l'intérieur de l'enceinte
                    angle = np.random.uniform(0, 2*np.pi)
                    radius = np.random.uniform(0.1, 0.5)
                    
                    house_x = radius * np.cos(angle)
                    house_y = radius * np.sin(angle)
                    
                    # Petite formation circulaire pour chaque case
                    n_house_points = min(3, self.n - robot_count)
                    if n_house_points > 0:
                        t_house = np.linspace(0, 2*np.pi, n_house_points)
                        house_circle_x = house_x + 0.08 * np.cos(t_house)
                        house_circle_y = house_y + 0.08 * np.sin(t_house)
                        
                        positions[0, robot_count:robot_count+n_house_points] = house_circle_x
                        positions[1, robot_count:robot_count+n_house_points] = house_circle_y
                        robot_count += n_house_points
        
        # Portes monumentales
        n_gates = int(self.n * 0.1)
        if n_gates > 0 and robot_count < self.n:
            # Portes aux points cardinaux
            gate_positions = [(0.7, 0.0), (0.0, 0.7), (-0.7, 0.0), (0.0, -0.7)]
            
            for gate_x, gate_y in gate_positions:
                n_gate = n_gates // 4
                if n_gate > 0 and robot_count < self.n:
                    # Formation linéaire pour la porte
                    gate_line_x = np.linspace(gate_x - 0.1, gate_x + 0.1, n_gate)
                    gate_line_y = np.full(n_gate, gate_y)
                    
                    n_place = min(n_gate, self.n - robot_count)
                    positions[0, robot_count:robot_count+n_place] = gate_line_x[:n_place]
                    positions[1, robot_count:robot_count+n_place] = gate_line_y[:n_place]
                    robot_count += n_place
        
        # Éléments restants
        if robot_count < self.n:
            remaining = self.n - robot_count
            # Rues et chemins
            street_angles = np.linspace(0, 2*np.pi, remaining)
            street_radius = np.linspace(0.2, 0.6, remaining)
            
            street_x = street_radius * np.cos(street_angles)
            street_y = street_radius * np.sin(street_angles)
            
            positions[0, robot_count:] = street_x
            positions[1, robot_count:] = street_y
        
        return positions

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #10: PATRIMOINE ARCHITECTURAL")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = self._get_phase_display_name(phase_name)
            
            print(f"\n🏛️  Début {display_name} ({duration}s, {phase_frames} frames)")
            
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
        print(f"✅ PROJET #10 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")

    def _get_phase_display_name(self, phase_name):
        """Retourne le nom d'affichage pour chaque phase."""
        names = {
            '1_case_haoussa': 'Case Traditionnel Haoussa',
            '2_mosquee_zinder': 'Mosquée de Zinder',
            '3_sultanat_zinder': 'Sultanat de Zinder',
            '4_village_fortifie': 'Village Fortifié (Kasbah)'
        }
        return names.get(phase_name, phase_name)