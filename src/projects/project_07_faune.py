# src/projects/project_07_faune_niger.py
"""
PROJET #7: FAUNE DU NIGER
Robotarium Swarm - ANEM 2025
Formation d'animaux emblématiques de la biodiversité nigérienne
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project07FauneNiger:
    """Implémentation du projet Faune du Niger."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_girafe': 75,      # 0:00-1:15
            '2_elephant': 75,    # 1:15-2:30
            '3_addax': 75,       # 2:30-3:45
            '4_dromadaire': 75   # 3:45-5:00
        }
        
        print(f"🦒 PROJET #7 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (5 minutes)")

    def phase_1_girafe(self, duration=75):
        """Phase 1: Girafe de l'Ouest - Marche et broutage."""
        print("🦒 Phase 1: Girafe de l'Ouest")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = self._create_girafe_silhouette(time_val)
            
            # Animation de marche
            if step % 20 < 10:  # Alternance pattes
                # Déplacer légèrement pour l'animation
                positions[0, :] += 0.01 * np.sin(2*np.pi*0.5*time_val)
            
            yield positions, time_val

    def phase_2_elephant(self, start_pos, duration=75):
        """Phase 2: Éléphant du désert - Marche majestueuse."""
        print("🐘 Phase 2: Éléphant du désert")
        
        start_time = self.phases['1_girafe']
        steps = int(duration * config.FPS)
        
        # Transition depuis la girafe
        elephant_base = self._create_elephant_silhouette()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, elephant_base, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de trompe
            if step % 30 < 15:
                # Mouvement de trompe
                trompe_indices = list(range(8, 18))  # Indices de la trompe
                for i in trompe_indices:
                    if i < positions.shape[1]:
                        positions[1, i] += 0.02 * np.sin(2*np.pi*0.3*time_val)
            
            yield positions, time_val

    def phase_3_addax(self, start_pos, duration=75):
        """Phase 3: Addax - Course et bonds."""
        print("🐐 Phase 3: Addax (antilope du Sahara)")
        
        start_time = self.phases['1_girafe'] + self.phases['2_elephant']
        steps = int(duration * config.FPS)
        
        # Formation de troupeau (3-4 addax)
        addax_positions = self._create_addax_troupeau()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, addax_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de course avec bonds
            bond_height = 0.1 * np.abs(np.sin(2*np.pi*1.5*time_val))
            positions[1, :] += bond_height
            
            # Déplacement latéral (course)
            positions[0, :] += 0.02
            
            yield positions, time_val

    def phase_4_dromadaire(self, start_pos, duration=75):
        """Phase 4: Dromadaire - Caravane du désert."""
        print("🐪 Phase 4: Dromadaire et caravane")
        
        start_time = self.phases['1_girafe'] + self.phases['2_elephant'] + self.phases['3_addax']
        steps = int(duration * config.FPS)
        
        # Formation de caravane (file indienne)
        caravane_positions = self._create_caravane_dromadaires()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, caravane_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de marche du désert (ondulation)
            for i in range(positions.shape[1]):
                # Ondulation progressive le long de la caravane
                wave_offset = 0.05 * np.sin(2*np.pi*0.2*time_val + i*0.3)
                positions[1, i] += wave_offset
            
            # Déplacement de la caravane
            positions[0, :] += 0.015
            
            yield positions, time_val

    def _create_girafe_silhouette(self, time_val=0):
        """Crée la silhouette d'une girafe."""
        positions = np.zeros((2, self.n))
        
        # Répartition anatomique
        n_pattes = 4 * 3  # 4 pattes × 3 robots
        n_cou = 15
        n_corps = 12
        n_tete = 5
        n_queue = 3
        n_rest = self.n - (n_pattes + n_cou + n_corps + n_tete + n_queue)
        
        if n_rest > 0:
            n_corps += n_rest  # Ajouter au corps
        
        robot_count = 0
        
        # Pattes arrière
        patte1_x = np.full(3, -0.3)
        patte1_y = np.linspace(-0.6, -0.3, 3)
        positions[0, robot_count:robot_count+3] = patte1_x
        positions[1, robot_count:robot_count+3] = patte1_y
        robot_count += 3
        
        patte2_x = np.full(3, -0.1)
        patte2_y = np.linspace(-0.6, -0.3, 3)
        positions[0, robot_count:robot_count+3] = patte2_x
        positions[1, robot_count:robot_count+3] = patte2_y
        robot_count += 3
        
        # Corps (ellipse allongée)
        t_corps = np.linspace(0, 2*np.pi, n_corps)
        corps_x = 0.1 + 0.3 * np.cos(t_corps)
        corps_y = -0.2 + 0.15 * np.sin(t_corps)
        positions[0, robot_count:robot_count+n_corps] = corps_x
        positions[1, robot_count:robot_count+n_corps] = corps_y
        robot_count += n_corps
        
        # Cou (courbe en S)
        t_cou = np.linspace(0, 1, n_cou)
        cou_x = 0.4 + 0.1 * np.sin(np.pi * t_cou)  # Courbure
        cou_y = -0.2 + 0.8 * t_cou  # Montée progressive
        positions[0, robot_count:robot_count+n_cou] = cou_x
        positions[1, robot_count:robot_count+n_cou] = cou_y
        robot_count += n_cou
        
        # Tête (ovale)
        t_tete = np.linspace(0, 2*np.pi, n_tete)
        tete_x = 0.5 + 0.08 * np.cos(t_tete)
        tete_y = 0.6 + 0.06 * np.sin(t_tete)
        positions[0, robot_count:robot_count+n_tete] = tete_x
        positions[1, robot_count:robot_count+n_tete] = tete_y
        robot_count += n_tete
        
        # Pattes avant
        patte3_x = np.full(3, 0.1)
        patte3_y = np.linspace(-0.6, -0.3, 3)
        positions[0, robot_count:robot_count+3] = patte3_x
        positions[1, robot_count:robot_count+3] = patte3_y
        robot_count += 3
        
        patte4_x = np.full(3, 0.3)
        patte4_y = np.linspace(-0.6, -0.3, 3)
        positions[0, robot_count:robot_count+3] = patte4_x
        positions[1, robot_count:robot_count+3] = patte4_y
        robot_count += 3
        
        # Queue
        if robot_count < self.n:
            queue_x = np.linspace(-0.3, -0.5, min(3, self.n-robot_count))
            queue_y = np.linspace(-0.2, -0.3, min(3, self.n-robot_count))
            n_queue = len(queue_x)
            positions[0, robot_count:robot_count+n_queue] = queue_x
            positions[1, robot_count:robot_count+n_queue] = queue_y
        
        return positions

    def _create_elephant_silhouette(self):
        """Crée la silhouette d'un éléphant."""
        positions = np.zeros((2, self.n))
        
        # Répartition anatomique
        n_tete = 8
        n_trompe = 10
        n_oreilles = 8
        n_corps = 15
        n_pattes = 8
        n_queue = 1
        
        robot_count = 0
        
        # Tête (cercle)
        t_tete = np.linspace(0, 2*np.pi, n_tete)
        tete_x = -0.2 + 0.15 * np.cos(t_tete)
        tete_y = 0.0 + 0.12 * np.sin(t_tete)
        positions[0, robot_count:robot_count+n_tete] = tete_x
        positions[1, robot_count:robot_count+n_tete] = tete_y
        robot_count += n_tete
        
        # Trompe (serpentin)
        t_trompe = np.linspace(0, 1, n_trompe)
        trompe_x = -0.35 + 0.1 * np.sin(2*np.pi*t_trompe)  # Ondulation
        trompe_y = 0.0 - 0.2 * t_trompe  # Descente
        positions[0, robot_count:robot_count+n_trompe] = trompe_x
        positions[1, robot_count:robot_count+n_trompe] = trompe_y
        robot_count += n_trompe
        
        # Oreilles (demi-cercles)
        # Oreille gauche
        t_oreille = np.linspace(np.pi/2, 3*np.pi/2, n_oreilles//2)
        oreille_g_x = -0.3 + 0.1 * np.cos(t_oreille)
        oreille_g_y = 0.1 + 0.08 * np.sin(t_oreille)
        positions[0, robot_count:robot_count+n_oreilles//2] = oreille_g_x
        positions[1, robot_count:robot_count+n_oreilles//2] = oreille_g_y
        robot_count += n_oreilles//2
        
        # Oreille droite
        t_oreille = np.linspace(-np.pi/2, np.pi/2, n_oreilles//2)
        oreille_d_x = -0.1 + 0.1 * np.cos(t_oreille)
        oreille_d_y = 0.1 + 0.08 * np.sin(t_oreille)
        positions[0, robot_count:robot_count+n_oreilles//2] = oreille_d_x
        positions[1, robot_count:robot_count+n_oreilles//2] = oreille_d_y
        robot_count += n_oreilles//2
        
        # Corps (ovale large)
        t_corps = np.linspace(0, 2*np.pi, n_corps)
        corps_x = 0.1 + 0.4 * np.cos(t_corps)
        corps_y = -0.1 + 0.25 * np.sin(t_corps)
        positions[0, robot_count:robot_count+n_corps] = corps_x
        positions[1, robot_count:robot_count+n_corps] = corps_y
        robot_count += n_corps
        
        # Pattes (cylindres)
        # Pattes avant
        positions[0, robot_count] = -0.1; positions[1, robot_count] = -0.35; robot_count += 1
        positions[0, robot_count] = 0.1; positions[1, robot_count] = -0.35; robot_count += 1
        
        # Pattes arrière
        positions[0, robot_count] = 0.3; positions[1, robot_count] = -0.35; robot_count += 1
        positions[0, robot_count] = 0.5; positions[1, robot_count] = -0.35; robot_count += 1
        
        # Queue
        if robot_count < self.n:
            positions[0, robot_count] = 0.6
            positions[1, robot_count] = -0.1
        
        return positions

    def _create_addax_troupeau(self):
        """Crée un troupeau de 3-4 addax."""
        positions = np.zeros((2, self.n))
        
        # 3 addax principaux
        addax_per_animal = self.n // 3
        remaining = self.n % 3
        
        # Addax 1
        addax1 = self._create_single_addax()
        n1 = min(addax_per_animal + (1 if remaining > 0 else 0), addax1.shape[1])
        positions[:, :n1] = addax1[:, :n1]
        current_count = n1
        
        # Décaler les addax suivants
        if current_count < self.n:
            addax2 = self._create_single_addax()
            addax2[0, :] += 0.6  # Décalage horizontal
            addax2[1, :] -= 0.1  # Légère variation verticale
            n2 = min(addax_per_animal + (1 if remaining > 1 else 0), self.n - current_count)
            positions[:, current_count:current_count+n2] = addax2[:, :n2]
            current_count += n2
        
        if current_count < self.n:
            addax3 = self._create_single_addax()
            addax3[0, :] += 1.2  # Décalage horizontal
            addax3[1, :] += 0.1  # Légère variation verticale
            n3 = min(addax_per_animal, self.n - current_count)
            positions[:, current_count:current_count+n3] = addax3[:, :n3]
        
        return positions

    def _create_single_addax(self):
        """Crée un seul addax."""
        n_robots = min(20, self.n)  # Limite pour un seul addax
        
        positions = np.zeros((2, n_robots))
        
        # Corps élancé
        n_corps = n_robots // 2
        t_corps = np.linspace(0, 2*np.pi, n_corps)
        corps_x = 0.0 + 0.2 * np.cos(t_corps)
        corps_y = 0.0 + 0.1 * np.sin(t_corps)
        positions[0, :n_corps] = corps_x
        positions[1, :n_corps] = corps_y
        
        # Tête et cornes
        if n_corps < n_robots:
            # Tête
            positions[0, n_corps] = -0.25
            positions[1, n_corps] = 0.0
            n_corps += 1
            
            # Cornes (spiralées)
            if n_corps < n_robots:
                # Corne gauche
                positions[0, n_corps] = -0.3
                positions[1, n_corps] = 0.05
                n_corps += 1
            
            if n_corps < n_robots:
                # Corne droite
                positions[0, n_corps] = -0.3
                positions[1, n_corps] = -0.05
        
        return positions

    def _create_caravane_dromadaires(self):
        """Crée une caravane de dromadaires en file indienne."""
        positions = np.zeros((2, self.n))
        
        # 4 dromadaires en file
        dromadaires_per_camel = self.n // 4
        remaining = self.n % 4
        
        for i in range(4):
            start_idx = i * dromadaires_per_camel + min(i, remaining)
            end_idx = start_idx + dromadaires_per_camel + (1 if i < remaining else 0)
            
            if start_idx < self.n:
                dromadaire = self._create_single_dromadaire()
                n_available = min(dromadaire.shape[1], end_idx - start_idx)
                
                # Positionner le dromadaire avec décalage
                dromadaire[0, :] += i * 0.5  # Espacement horizontal
                dromadaire[1, :] -= 0.1 * (i % 2)  # Légère variation
                
                positions[:, start_idx:start_idx+n_available] = dromadaire[:, :n_available]
        
        return positions

    def _create_single_dromadaire(self):
        """Crée un seul dromadaire."""
        n_robots = min(15, self.n)  # Limite pour un seul dromadaire
        
        positions = np.zeros((2, n_robots))
        
        # Bosse caractéristique
        n_bosse = n_robots // 3
        t_bosse = np.linspace(0, np.pi, n_bosse)
        bosse_x = 0.0 + 0.1 * np.cos(t_bosse)
        bosse_y = 0.1 + 0.08 * np.sin(t_bosse)
        positions[0, :n_bosse] = bosse_x
        positions[1, :n_bosse] = bosse_y
        
        # Cou long
        if n_bosse < n_robots:
            n_cou = min(5, n_robots - n_bosse)
            cou_x = np.full(n_cou, -0.15)
            cou_y = np.linspace(0.05, 0.2, n_cou)
            positions[0, n_bosse:n_bosse+n_cou] = cou_x
            positions[1, n_bosse:n_bosse+n_cou] = cou_y
            n_bosse += n_cou
        
        # Tête
        if n_bosse < n_robots:
            positions[0, n_bosse] = -0.2
            positions[1, n_bosse] = 0.25
        
        return positions

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #7: FAUNE DU NIGER")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = phase_name.replace('_', ' ').title()
            
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
        print(f"✅ PROJET #7 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")