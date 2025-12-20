# src/projects/project_08_calligraphie.py
"""
PROJET #8: CALLIGRAPHIE ARABE ANIMÉE
Robotarium Swarm - ANEM 2025
Animation de mots en calligraphie arabe avec effet de pinceau fluide
"""

import numpy as np
import matplotlib.pyplot as plt
from formations.base_formations import BaseFormations
from animations.transition_manager import TransitionManager
from animations.color_animations import ColorAnimator
from utils.config import config

class Project08Calligraphie:
    """Implémentation du projet Calligraphie Arabe Animée."""
    
    def __init__(self, n_robots=None):
        self.n = n_robots or config.N_ROBOTS
        self.base = BaseFormations(self.n)
        self.transitions = TransitionManager()
        self.colors = ColorAnimator()
        
        # Phases du projet (durées en secondes)
        self.phases = {
            '1_salam': 60,        # 0:00-1:00
            '2_ukhuwwa': 60,      # 1:00-2:00
            '3_tadamun': 60,      # 2:00-3:00
            '4_logo_anem': 60     # 3:00-4:00
        }
        
        # Styles calligraphiques
        self.styles = {
            'salam': 'thuluth',      # Style monumental
            'ukhuwwa': 'naskh',      # Style élégant
            'tadamun': 'diwani',     # Style ornemental
            'logo_anem': 'ruqaa'     # Style compact
        }
        
        print(f"📜 PROJET #8 INITIALISÉ: {self.n} robots")
        print(f"📊 Durée totale: {sum(self.phases.values())} secondes (4 minutes)")

    def phase_1_salam(self, duration=60):
        """Phase 1: Écriture de 'السلام' (La Paix) - Style Thuluth."""
        print("🕊️  Phase 1: السلام (As-Salam - La Paix)")
        
        start_time = 0
        steps = int(duration * config.FPS)
        
        # Formation finale du mot
        target_positions = self._create_word_salam()
        
        for step in range(steps):
            time_val = start_time + step / config.FPS
            positions = np.zeros((2, self.n))
            
            # Effet d'écriture progressive (droite à gauche)
            progression = step / steps
            n_visible = int(self.n * progression)
            
            if n_visible > 0:
                # Prendre les robots de droite vers la gauche
                positions[:, :n_visible] = target_positions[:, -n_visible:]
                
                # Effet d'encre qui coule pour les robots non visibles
                if n_visible < self.n:
                    remaining = self.n - n_visible
                    ink_positions = self._create_ink_effect(remaining, time_val)
                    positions[:, n_visible:] = ink_positions
            
            yield positions, time_val

    def phase_2_ukhuwwa(self, start_pos, duration=60):
        """Phase 2: Écriture de 'الأخوة' (La Fraternité) - Style Naskh."""
        print("🤝 Phase 2: الأخوة (Al-Ukhuwwa - La Fraternité)")
        
        start_time = self.phases['1_salam']
        steps = int(duration * config.FPS)
        
        # Formation du nouveau mot
        target_positions = self._create_word_ukhuwwa()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de danse des lettres
            if step % 20 < 10:
                # Légère oscillation des positions
                for i in range(positions.shape[1]):
                    offset_x = 0.02 * np.sin(2*np.pi*0.5*time_val + i*0.1)
                    offset_y = 0.01 * np.cos(2*np.pi*0.5*time_val + i*0.2)
                    positions[0, i] += offset_x
                    positions[1, i] += offset_y
            
            yield positions, time_val

    def phase_3_tadamun(self, start_pos, duration=60):
        """Phase 3: Écriture de 'التضامن' (La Solidarité) - Style Diwani."""
        print("🔄 Phase 3: التضامن (At-Tadamun - La Solidarité)")
        
        start_time = self.phases['1_salam'] + self.phases['2_ukhuwwa']
        steps = int(duration * config.FPS)
        
        # Formation en arc de cercle
        target_positions = self._create_word_tadamun()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de pulsation rythmique
            pulse_factor = 1.0 + 0.1 * np.sin(2*np.pi*0.3*time_val)
            center = np.array([[0.0], [0.0]])
            positions = center + (positions - center) * pulse_factor
            
            yield positions, time_val

    def phase_4_logo_anem(self, start_pos, duration=60):
        """Phase 4: Logo ANEM en calligraphie arabe - Style Ruqaa."""
        print("🎨 Phase 4: Logo ANEM en Arabe")
        
        start_time = self.phases['1_salam'] + self.phases['2_ukhuwwa'] + self.phases['3_tadamun']
        steps = int(duration * config.FPS)
        
        # Logo stylisé ANEM en arabe
        target_positions = self._create_logo_anem_arabe()
        
        for step, positions in enumerate(
            self.transitions.interpolate_positions(start_pos, target_positions, 5, 'ease_in_out')
        ):
            if step >= steps:
                break
            time_val = start_time + step / config.FPS
            
            # Animation de rotation 3D simulée
            angle = 0.1 * np.sin(2*np.pi*0.2*time_val)
            for i in range(positions.shape[1]):
                x, y = positions[0, i], positions[1, i]
                positions[0, i] = x * np.cos(angle) - y * np.sin(angle)
                positions[1, i] = x * np.sin(angle) + y * np.cos(angle)
            
            yield positions, time_val

    def _create_word_salam(self):
        """Crée la formation pour le mot 'السلام'."""
        positions = np.zeros((2, self.n))
        
        # Structure du mot السلام (de droite à gauche)
        # س - ل - ا - م
        
        robot_count = 0
        
        # Lettre م (Mim - à gauche)
        n_mim = self.n // 4
        if n_mim > 0:
            # Courbe caractéristique du Mim
            t_mim = np.linspace(0, 2*np.pi, n_mim)
            mim_x = -0.8 + 0.15 * np.cos(t_mim)
            mim_y = 0.0 + 0.1 * np.sin(t_mim)
            positions[0, robot_count:robot_count+n_mim] = mim_x
            positions[1, robot_count:robot_count+n_mim] = mim_y
            robot_count += n_mim
        
        # Lettre ا (Alif - verticale)
        n_alif = self.n // 4
        if n_alif > 0:
            alif_x = np.full(n_alif, -0.5)
            alif_y = np.linspace(-0.2, 0.2, n_alif)
            positions[0, robot_count:robot_count+n_alif] = alif_x
            positions[1, robot_count:robot_count+n_alif] = alif_y
            robot_count += n_alif
        
        # Lettre ل (Lam - courbe)
        n_lam = self.n // 4
        if n_lam > 0:
            t_lam = np.linspace(-np.pi/2, np.pi/2, n_lam)
            lam_x = -0.2 + 0.1 * np.cos(t_lam)
            lam_y = 0.1 * np.sin(t_lam)
            positions[0, robot_count:robot_count+n_lam] = lam_x
            positions[1, robot_count:robot_count+n_lam] = lam_y
            robot_count += n_lam
        
        # Lettre س (Sin - vagues)
        n_sin = self.n - robot_count
        if n_sin > 0:
            t_sin = np.linspace(0, 2*np.pi, n_sin)
            sin_x = 0.2 + 0.15 * np.cos(t_sin)
            sin_y = 0.0 + 0.08 * np.sin(2*t_sin)  # Double fréquence pour les vagues
            positions[0, robot_count:robot_count+n_sin] = sin_x
            positions[1, robot_count:robot_count+n_sin] = sin_y
        
        return positions

    def _create_word_ukhuwwa(self):
        """Crée la formation pour le mot 'الأخوة'."""
        positions = np.zeros((2, self.n))
        
        # Structure du mot الأخوة
        # أ - ل - خ - و - ة
        
        robot_count = 0
        
        # Lettre ة (Ta Marbuta - à gauche)
        n_ta = self.n // 5
        if n_ta > 0:
            t_ta = np.linspace(0, 2*np.pi, n_ta)
            ta_x = -0.9 + 0.1 * np.cos(t_ta)
            ta_y = -0.1 + 0.08 * np.sin(t_ta)
            positions[0, robot_count:robot_count+n_ta] = ta_x
            positions[1, robot_count:robot_count+n_ta] = ta_y
            robot_count += n_ta
        
        # Lettre و (Waw - cercle)
        n_waw = self.n // 5
        if n_waw > 0:
            t_waw = np.linspace(0, 2*np.pi, n_waw)
            waw_x = -0.6 + 0.12 * np.cos(t_waw)
            waw_y = 0.0 + 0.12 * np.sin(t_waw)
            positions[0, robot_count:robot_count+n_waw] = waw_x
            positions[1, robot_count:robot_count+n_waw] = waw_y
            robot_count += n_waw
        
        # Lettre خ (Kha - complexe)
        n_kha = self.n // 5
        if n_kha > 0:
            # Partie supérieure
            t_kha1 = np.linspace(0, np.pi, n_kha//2)
            kha1_x = -0.3 + 0.1 * np.cos(t_kha1)
            kha1_y = 0.1 + 0.05 * np.sin(t_kha1)
            
            # Partie inférieure
            t_kha2 = np.linspace(0, np.pi, n_kha//2)
            kha2_x = -0.3 + 0.1 * np.cos(t_kha2)
            kha2_y = -0.1 - 0.05 * np.sin(t_kha2)
            
            kha_x = np.concatenate([kha1_x, kha2_x])
            kha_y = np.concatenate([kha1_y, kha2_y])
            
            n_place = min(len(kha_x), self.n - robot_count)
            positions[0, robot_count:robot_count+n_place] = kha_x[:n_place]
            positions[1, robot_count:robot_count+n_place] = kha_y[:n_place]
            robot_count += n_place
        
        # Lettre ل (Lam)
        n_lam = self.n // 5
        if n_lam > 0:
            t_lam = np.linspace(-np.pi/2, np.pi/2, n_lam)
            lam_x = 0.0 + 0.1 * np.cos(t_lam)
            lam_y = 0.1 * np.sin(t_lam)
            positions[0, robot_count:robot_count+n_lam] = lam_x
            positions[1, robot_count:robot_count+n_lam] = lam_y
            robot_count += n_lam
        
        # Lettre أ (Alif avec Hamza)
        n_alif = self.n - robot_count
        if n_alif > 0:
            # Alif verticale
            alif_x = np.full(n_alif, 0.3)
            alif_y = np.linspace(-0.15, 0.15, n_alif)
            
            # Hamza (petit cercle en haut)
            if n_alif > 3:
                hamza_idx = robot_count + n_alif//2
                positions[0, hamza_idx] = 0.35
                positions[1, hamza_idx] = 0.15
            
            positions[0, robot_count:robot_count+n_alif] = alif_x
            positions[1, robot_count:robot_count+n_alif] = alif_y
        
        return positions

    def _create_word_tadamun(self):
        """Crée la formation pour le mot 'التضامن' en arc de cercle."""
        positions = np.zeros((2, self.n))
        
        # Mot التضامن disposé en arc
        letters = 6  # ا ل ت ض ا م ن
        robots_per_letter = self.n // letters
        remaining = self.n % letters
        
        radius = 0.7
        start_angle = np.pi/3
        end_angle = 2*np.pi/3
        
        robot_count = 0
        
        for i in range(letters):
            n_letter = robots_per_letter + (1 if i < remaining else 0)
            if robot_count >= self.n:
                break
                
            # Position angulaire pour cette lettre
            angle = start_angle + (end_angle - start_angle) * i / (letters - 1)
            
            # Petite formation pour chaque lettre
            t_letter = np.linspace(0, 2*np.pi, n_letter)
            letter_x = radius * np.cos(angle) + 0.1 * np.cos(t_letter)
            letter_y = radius * np.sin(angle) + 0.08 * np.sin(t_letter)
            
            n_place = min(n_letter, self.n - robot_count)
            positions[0, robot_count:robot_count+n_place] = letter_x[:n_place]
            positions[1, robot_count:robot_count+n_place] = letter_y[:n_place]
            robot_count += n_place
        
        return positions

    def _create_logo_anem_arabe(self):
        """Crée un logo stylisé ANEM en calligraphie arabe."""
        positions = np.zeros((2, self.n))
        
        # Logo circulaire avec les lettres entrelacées
        # أ ن م (ANEM stylisé)
        
        robot_count = 0
        
        # Cercle extérieur
        n_circle = self.n // 2
        if n_circle > 0:
            t_circle = np.linspace(0, 2*np.pi, n_circle)
            circle_x = 0.6 * np.cos(t_circle)
            circle_y = 0.6 * np.sin(t_circle)
            positions[0, robot_count:robot_count+n_circle] = circle_x
            positions[1, robot_count:robot_count+n_circle] = circle_y
            robot_count += n_circle
        
        # Lettre أ (Alif) au centre
        n_alif = self.n // 4
        if n_alif > 0:
            alif_x = np.full(n_alif, 0.0)
            alif_y = np.linspace(-0.3, 0.3, n_alif)
            positions[0, robot_count:robot_count+n_alif] = alif_x
            positions[1, robot_count:robot_count+n_alif] = alif_y
            robot_count += n_alif
        
        # Lettre ن (Nun) - courbe
        n_nun = self.n // 4
        if n_nun > 0:
            t_nun = np.linspace(-np.pi/4, np.pi/4, n_nun)
            nun_x = 0.2 + 0.15 * np.cos(t_nun)
            nun_y = 0.1 * np.sin(t_nun)
            positions[0, robot_count:robot_count+n_nun] = nun_x
            positions[1, robot_count:robot_count+n_nun] = nun_y
            robot_count += n_nun
        
        # Lettre م (Mim) - complément
        if robot_count < self.n:
            n_mim = self.n - robot_count
            t_mim = np.linspace(np.pi/4, 3*np.pi/4, n_mim)
            mim_x = -0.2 + 0.1 * np.cos(t_mim)
            mim_y = 0.1 * np.sin(t_mim)
            positions[0, robot_count:robot_count+n_mim] = mim_x
            positions[1, robot_count:robot_count+n_mim] = mim_y
        
        return positions

    def _create_ink_effect(self, n_robots, time_val):
        """Crée un effet d'encre qui coule pour l'animation d'écriture."""
        positions = np.zeros((2, n_robots))
        
        # Position de départ (encre)
        start_x = 1.0  # Droite de l'arène
        start_y = -0.8  # Bas de l'arène
        
        # Effet de gouttes qui tombent
        for i in range(n_robots):
            # Variation aléatoire mais contrôlée
            drop_speed = 0.5 + 0.3 * (i / n_robots)
            swing = 0.1 * np.sin(time_val * 2 + i * 0.5)
            
            x = start_x - drop_speed * time_val + swing
            y = start_y + 0.3 * np.sin(time_val * 3 + i)
            
            positions[0, i] = x
            positions[1, i] = y
        
        return positions

    def run_complete_animation(self):
        """Exécute l'animation complète du projet."""
        print("🎬 Démarrage du PROJET #8: CALLIGRAPHIE ARABE ANIMÉE")
        print("=" * 60)
        
        current_pos = None
        frame_count = 0
        
        # Exécuter chaque phase séquentiellement
        for phase_name, duration in self.phases.items():
            phase_method = getattr(self, f'phase_{phase_name}')
            phase_frames = int(duration * config.FPS)
            
            # Nom d'affichage
            display_name = self._get_phase_display_name(phase_name)
            
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
        print(f"✅ PROJET #8 TERMINÉ AVEC SUCCÈS!")
        print(f"📊 Total: {frame_count} frames, {frame_count/config.FPS:.1f} secondes")

    def _get_phase_display_name(self, phase_name):
        """Retourne le nom d'affichage pour chaque phase."""
        names = {
            '1_salam': 'السلام (La Paix)',
            '2_ukhuwwa': 'الأخوة (La Fraternité)', 
            '3_tadamun': 'التضامن (La Solidarité)',
            '4_logo_anem': 'Logo ANEM Arabe'
        }
        return names.get(phase_name, phase_name)