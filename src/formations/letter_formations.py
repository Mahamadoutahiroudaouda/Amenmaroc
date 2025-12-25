# src/formations/letter_formations.py
"""
FORMATIONS DES LETTRES A-N-E-M - TAILLES OPTIMISÉES POUR L'ARÈNE
"""

import numpy as np
from .base_formations import BaseFormations
from utils.config import config

class LetterFormations(BaseFormations):
    """Générateur de formations pour les lettres A, N, E, M - TAILLES RÉDUITES."""
    
    def __init__(self, n_robots=None):
        super().__init__(n_robots)
        # TAILLES FORTEMENT RÉDUITES pour bien tenir dans l'arène
        self.letter_height = 0.4   # Réduit de 1.2 à 0.6 (50% plus petit)
        self.letter_width = 0.4   # Réduit de 0.8 à 0.4 (50% plus petit)
        self.spacing = 0.3        # Réduit de 0.8 à 0.3 (espacement réduit)
    
    def letter_A(self, robots_count):
        """Formation de la lettre A - TAILLE RÉDUITE."""
        n_diag = max(2, robots_count // 4)
        n_barre = max(2, robots_count - 2 * n_diag)
        
        # Diagonale gauche
        x1 = np.linspace(-self.letter_width/2, 0, n_diag)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_diag)
        
        # Diagonale droite  
        x2 = np.linspace(0, self.letter_width/2, n_diag)
        y2 = np.linspace(self.letter_height/2, -self.letter_height/2, n_diag)
        
        # Barre horizontale
        x3 = np.linspace(-self.letter_width/3, self.letter_width/3, n_barre)
        y3 = np.zeros(n_barre)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        
        return np.array([x, y])
    
    def letter_N(self, robots_count):
        """Formation de la lettre N - TAILLE RÉDUITE."""
        n_vertical = max(2, robots_count // 3)
        n_diag = max(2, robots_count // 3)
        n_rest = robots_count - n_vertical - n_diag
        
        # Barre gauche
        x1 = np.full(n_vertical, -self.letter_width/2)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_vertical)
        
        # Diagonale
        x2 = np.linspace(-self.letter_width/2, self.letter_width/2, n_diag)
        y2 = np.linspace(-self.letter_height/2, self.letter_height/2, n_diag)
        
        # Barre droite
        x3 = np.full(n_rest, self.letter_width/2)
        y3 = np.linspace(self.letter_height/2, -self.letter_height/2, n_rest)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        
        return np.array([x, y])
    
    def letter_E(self, robots_count):
        """Formation de la lettre E - TAILLE RÉDUITE."""
        n_vertical = max(2, robots_count // 4)
        n_horizontal = max(2, (robots_count - n_vertical) // 3)
        
        # Barre verticale
        x1 = np.full(n_vertical, -self.letter_width/2)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_vertical)
        
        # Barre haute
        x2 = np.linspace(-self.letter_width/2, self.letter_width/2, n_horizontal)
        y2 = np.full(n_horizontal, self.letter_height/2)
        
        # Barre milieu
        x3 = np.linspace(-self.letter_width/2, self.letter_width/2, n_horizontal)
        y3 = np.zeros(n_horizontal)
        
        # Barre basse
        n_rest = robots_count - n_vertical - 2 * n_horizontal
        x4 = np.linspace(-self.letter_width/2, self.letter_width/2, n_rest)
        y4 = np.full(n_rest, -self.letter_height/2)
        
        x = np.concatenate([x1, x2, x3, x4])
        y = np.concatenate([y1, y2, y3, y4])
        
        return np.array([x, y])
    
    def letter_M(self, robots_count):
        """Formation de la lettre M - AMÉLI ORÉE."""
        n_per_segment = max(2, robots_count // 4)
        
        # Barre gauche (verticale)
        x1 = np.full(n_per_segment, -self.letter_width/2)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_per_segment)
        
        # Diagonale gauche (descend vers le centre)
        x2 = np.linspace(-self.letter_width/2, 0, n_per_segment)
        y2 = np.linspace(self.letter_height/2, -self.letter_height/4, n_per_segment)
        
        # Diagonale droite (remonte vers la droite)
        x3 = np.linspace(0, self.letter_width/2, n_per_segment)
        y3 = np.linspace(-self.letter_height/4, self.letter_height/2, n_per_segment)
        
        # Barre droite (verticale)
        remaining = robots_count - 3 * n_per_segment
        x4 = np.full(remaining, self.letter_width/2)
        y4 = np.linspace(self.letter_height/2, -self.letter_height/2, remaining)
        
        x = np.concatenate([x1, x2, x3, x4])
        y = np.concatenate([y1, y2, y3, y4])
        
        return np.array([x, y])
    
    def letter_I(self, robots_count):
        """Formation de la lettre I - TAILLE RÉDUITE."""
        n_vertical = max(2, robots_count // 3)
        n_horizontal = max(2, (robots_count - n_vertical) // 2)
        
        # Barre verticale
        x1 = np.zeros(n_vertical)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_vertical)
        
        # Barre haute
        x2 = np.linspace(-self.letter_width/3, self.letter_width/3, n_horizontal)
        y2 = np.full(n_horizontal, self.letter_height/2)
        
        # Barre basse
        n_rest = robots_count - n_vertical - n_horizontal
        x3 = np.linspace(-self.letter_width/3, self.letter_width/3, n_rest)
        y3 = np.full(n_rest, -self.letter_height/2)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        
        return np.array([x, y])
    
    def letter_G(self, robots_count):
        """Formation de la lettre G - TAILLE RÉDUITE."""
        # Cercle avec ouverture
        angles = np.linspace(-np.pi/4, 2*np.pi - np.pi/4, robots_count, endpoint=False)
        x = 0.3 * np.cos(angles)  # Réduit
        y = 0.4 * np.sin(angles)  # Réduit
        
        # Barre horizontale
        n_barre = max(2, robots_count // 5)
        x_barre = np.linspace(0, 0.2, n_barre)  # Réduit
        y_barre = np.zeros(n_barre)
        
        x = np.concatenate([x[:-n_barre], x_barre])
        y = np.concatenate([y[:-n_barre], y_barre])
        
        return np.array([x[:robots_count], y[:robots_count]])
    
    def letter_R(self, robots_count):
        """Formation de la lettre R - TAILLE RÉDUITE."""
        n_vertical = max(2, robots_count // 3)
        n_diag = max(2, robots_count // 3)
        n_curve = robots_count - n_vertical - n_diag
        
        # Barre verticale
        x1 = np.full(n_vertical, -self.letter_width/2)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_vertical)
        
        # Demi-cercle haut
        angles = np.linspace(-np.pi/2, np.pi/2, n_curve)
        x2 = -self.letter_width/2 + 0.2 + 0.2 * np.cos(angles)  # Réduit
        y2 = 0.2 * np.sin(angles)  # Réduit
        
        # Diagonale
        x3 = np.linspace(0, self.letter_width/2, n_diag)
        y3 = np.linspace(0, -self.letter_height/2, n_diag)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        
        return np.array([x, y])
    
    def get_ANEM_formation(self):
        """Formation complète ANEM avec espacement réduit."""
        robots_per_letter = self.n // 4
        remainder = self.n % 4
        
        A_pos = self.letter_A(robots_per_letter + (1 if remainder >= 1 else 0))
        N_pos = self.letter_N(robots_per_letter + (1 if remainder >= 2 else 0))
        E_pos = self.letter_E(robots_per_letter + (1 if remainder >= 3 else 0))
        M_pos = self.letter_M(robots_per_letter)
        
        # Largeur totale RÉDUITE
        total_width = 4 * self.letter_width + 3 * self.spacing
        start_x = -total_width / 2 + self.letter_width / 2
        
        # Positionner chaque lettre
        A_pos[0, :] += start_x
        N_pos[0, :] += start_x + self.letter_width + self.spacing
        E_pos[0, :] += start_x + 2 * (self.letter_width + self.spacing)
        M_pos[0, :] += start_x + 3 * (self.letter_width + self.spacing)
        
        # Centrer verticalement
        for letter_pos in [A_pos, N_pos, E_pos, M_pos]:
            letter_pos[1, :] -= letter_pos[1, :].mean()
        
        # Combiner
        all_x = np.concatenate([A_pos[0], N_pos[0], E_pos[0], M_pos[0]])
        all_y = np.concatenate([A_pos[1], N_pos[1], E_pos[1], M_pos[1]])
        
        return np.array([all_x, all_y])
    
    def get_NIGER_formation(self):
        """Formation du mot NIGER - TAILLES RÉDUITES."""
        # Pour 50 robots, on fait NIGER avec 10 robots par lettre
        robots_per_letter = min(10, self.n // 5)
        
        N_pos = self.letter_N(robots_per_letter)
        I_pos = self.letter_I(robots_per_letter)
        G_pos = self.letter_G(robots_per_letter)
        E_pos = self.letter_E(robots_per_letter)
        R_pos = self.letter_R(robots_per_letter)
        
        # Positionner chaque lettre avec espacement réduit
        total_width = 5 * self.letter_width + 4 * self.spacing
        start_x = -total_width / 2 + self.letter_width / 2
        
        N_pos[0, :] += start_x
        I_pos[0, :] += start_x + self.letter_width + self.spacing
        G_pos[0, :] += start_x + 2 * (self.letter_width + self.spacing)
        E_pos[0, :] += start_x + 3 * (self.letter_width + self.spacing)
        R_pos[0, :] += start_x + 4 * (self.letter_width + self.spacing)
        
        # Centrer verticalement
        for letter_pos in [N_pos, I_pos, G_pos, E_pos, R_pos]:
            letter_pos[1, :] -= letter_pos[1, :].mean()
        
        all_x = np.concatenate([N_pos[0], I_pos[0], G_pos[0], E_pos[0], R_pos[0]])
        all_y = np.concatenate([N_pos[1], I_pos[1], G_pos[1], E_pos[1], R_pos[1]])
        
        return np.array([all_x, all_y])
    
    def letter_J(self, robots_count):
        """Formation de la lettre J."""
        n_vertical = max(2, robots_count // 2)
        n_curve = robots_count - n_vertical
        
        # Barre verticale
        x1 = np.full(n_vertical, self.letter_width/4)
        y1 = np.linspace(-self.letter_height/2 + 0.1, self.letter_height/2, n_vertical)
        
        # Crochet bas (quart de cercle)
        angles = np.linspace(np.pi, 3*np.pi/2, n_curve)
        radius = self.letter_width/4
        x2 = radius * np.cos(angles)
        y2 = -self.letter_height/2 + 0.1 + radius * np.sin(angles)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        
        return np.array([x, y])
    
    def letter_C(self, robots_count):
        """Formation de la lettre C."""
        # Arc de cercle avec ouverture à droite
        angles = np.linspace(np.pi/3, 5*np.pi/3, robots_count)
        x = 0.3 * np.cos(angles)
        y = 0.4 * np.sin(angles)
        
        return np.array([x, y])
    
    def letter_S(self, robots_count):
        """Formation de la lettre S."""
        # Deux demi-cercles opposés
        n_half = robots_count // 2
        
        # Demi-cercle haut
        angles1 = np.linspace(0, np.pi, n_half)
        x1 = 0.15 * np.cos(angles1)
        y1 = 0.2 + 0.15 * np.sin(angles1)
        
        # Demi-cercle bas
        angles2 = np.linspace(np.pi, 2*np.pi, robots_count - n_half)
        x2 = 0.15 * np.cos(angles2)
        y2 = -0.2 + 0.15 * np.sin(angles2)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        
        return np.array([x, y])
    
    def letter_F(self, robots_count):
        """Formation de la lettre F."""
        n_vertical = max(2, robots_count // 3)
        n_horizontal = max(2, (robots_count - n_vertical) // 2)
        
        # Barre verticale
        x1 = np.full(n_vertical, -self.letter_width/2)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_vertical)
        
        # Barre haute
        x2 = np.linspace(-self.letter_width/2, self.letter_width/2, n_horizontal)
        y2 = np.full(n_horizontal, self.letter_height/2)
        
        # Barre milieu
        n_rest = robots_count - n_vertical - n_horizontal
        x3 = np.linspace(-self.letter_width/2, self.letter_width/3, n_rest)
        y3 = np.zeros(n_rest)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        
        return np.array([x, y])
    
    # ========== DIGITS ==========
    
    def digit_0(self, robots_count):
        """Formation du chiffre 0."""
        angles = np.linspace(0, 2*np.pi, robots_count, endpoint=False)
        x = 0.25 * np.cos(angles)
        y = 0.35 * np.sin(angles)
        return np.array([x, y])
    
    def digit_1(self, robots_count):
        """Formation du chiffre 1."""
        # Ligne verticale simple
        x = np.zeros(robots_count)
        y = np.linspace(-self.letter_height/2, self.letter_height/2, robots_count)
        return np.array([x, y])
    
    def digit_2(self, robots_count):
        """Formation du chiffre 2."""
        n_top = robots_count // 3
        n_diag = robots_count // 3
        n_bottom = robots_count - n_top - n_diag
        
        # Arc supérieur
        angles = np.linspace(np.pi, 2*np.pi, n_top)
        x1 = 0.15 * np.cos(angles)
        y1 = 0.15 + 0.15 * np.sin(angles)
        
        # Diagonale
        x2 = np.linspace(0.15, -0.2, n_diag)
        y2 = np.linspace(0, -0.3, n_diag)
        
        # Barre basse
        x3 = np.linspace(-0.2, 0.2, n_bottom)
        y3 = np.full(n_bottom, -0.3)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        return np.array([x, y])
    
    def digit_3(self, robots_count):
        """Formation du chiffre 3."""
        n_per_arc = robots_count // 2
        
        # Arc supérieur
        angles1 = np.linspace(np.pi/2, 5*np.pi/2, n_per_arc)
        x1 = 0.15 * np.cos(angles1)
        y1 = 0.15 + 0.15 * np.sin(angles1)
        
        # Arc inférieur
        angles2 = np.linspace(np.pi/2, 5*np.pi/2, robots_count - n_per_arc)
        x2 = 0.15 * np.cos(angles2)
        y2 = -0.15 + 0.15 * np.sin(angles2)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        return np.array([x, y])
    
    def digit_4(self, robots_count):
        """Formation du chiffre 4."""
        n_vertical = robots_count // 3
        n_diag = robots_count // 3
        n_horizontal = robots_count - n_vertical - n_diag
        
        # Diagonale
        x1 = np.linspace(-0.15, 0, n_diag)
        y1 = np.linspace(0.3, 0, n_diag)
        
        # Horizontale
        x2 = np.linspace(-0.15, 0.15, n_horizontal)
        y2 = np.zeros(n_horizontal)
        
        # Verticale
        x3 = np.full(n_vertical, 0.1)
        y3 = np.linspace(-0.3, 0.3, n_vertical)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        return np.array([x, y])
    
    def digit_5(self, robots_count):
        """Formation du chiffre 5."""
        n_top = robots_count // 4
        n_vertical = robots_count // 4
        n_arc = robots_count - n_top - n_vertical
        
        # Barre haute
        x1 = np.linspace(-0.15, 0.15, n_top)
        y1 = np.full(n_top, 0.3)
        
        # Verticale gauche
        x2 = np.full(n_vertical, -0.15)
        y2 = np.linspace(0.3, 0, n_vertical)
        
        # Arc inférieur
        angles = np.linspace(np.pi/2, 5*np.pi/2, n_arc)
        x3 = 0.15 * np.cos(angles)
        y3 = -0.15 + 0.15 * np.sin(angles)
        
        x = np.concatenate([x1, x2, x3])
        y = np.concatenate([y1, y2, y3])
        return np.array([x, y])
    
    def digit_6(self, robots_count):
        """Formation du chiffre 6."""
        n_arc = robots_count // 2
        n_circle = robots_count - n_arc
        
        # Arc supérieur
        angles1 = np.linspace(0, np.pi, n_arc)
        x1 = -0.1 + 0.1 * np.cos(angles1)
        y1 = 0.15 + 0.1 * np.sin(angles1)
        
        # Cercle inférieur
        angles2 = np.linspace(0, 2*np.pi, n_circle, endpoint=False)
        x2 = 0.15 * np.cos(angles2)
        y2 = -0.15 + 0.15 * np.sin(angles2)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        return np.array([x, y])
    
    def digit_7(self, robots_count):
        """Formation du chiffre 7."""
        n_top = robots_count // 2
        n_diag = robots_count - n_top
        
        # Barre haute
        x1 = np.linspace(-0.15, 0.15, n_top)
        y1 = np.full(n_top, 0.3)
        
        # Diagonale
        x2 = np.linspace(0.15, -0.05, n_diag)
        y2 = np.linspace(0.3, -0.3, n_diag)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        return np.array([x, y])
    
    def digit_8(self, robots_count):
        """Formation du chiffre 8."""
        n_per_circle = robots_count // 2
        
        # Cercle supérieur
        angles1 = np.linspace(0, 2*np.pi, n_per_circle, endpoint=False)
        x1 = 0.12 * np.cos(angles1)
        y1 = 0.15 + 0.12 * np.sin(angles1)
        
        # Cercle inférieur
        angles2 = np.linspace(0, 2*np.pi, robots_count - n_per_circle, endpoint=False)
        x2 = 0.15 * np.cos(angles2)
        y2 = -0.15 + 0.15 * np.sin(angles2)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        return np.array([x, y])
    
    def digit_9(self, robots_count):
        """Formation du chiffre 9."""
        n_circle = robots_count // 2
        n_arc = robots_count - n_circle
        
        # Cercle supérieur
        angles1 = np.linspace(0, 2*np.pi, n_circle, endpoint=False)
        x1 = 0.15 * np.cos(angles1)
        y1 = 0.15 + 0.15 * np.sin(angles1)
        
        # Arc inférieur
        angles2 = np.linspace(-np.pi/2, np.pi/2, n_arc)
        x2 = 0.1 + 0.1 * np.cos(angles2)
        y2 = -0.15 + 0.1 * np.sin(angles2)
        
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])
        return np.array([x, y])
    
    # ========== COMPOSITE TEXT FORMATIONS ==========
    
    def get_JCN2026_formation(self):
        """Formation du texte JCN2026."""
        robots_per_char = self.n // 7
        remainder = self.n % 7
        
        J_pos = self.letter_J(robots_per_char + (1 if remainder >= 1 else 0))
        C_pos = self.letter_C(robots_per_char + (1 if remainder >= 2 else 0))
        N_pos = self.letter_N(robots_per_char + (1 if remainder >= 3 else 0))
        d2_pos = self.digit_2(robots_per_char + (1 if remainder >= 4 else 0))
        d0_pos = self.digit_0(robots_per_char + (1 if remainder >= 5 else 0))
        d2b_pos = self.digit_2(robots_per_char + (1 if remainder >= 6 else 0))
        d6_pos = self.digit_6(robots_per_char)
        
        # Positionner chaque caractère
        total_width = 7 * self.letter_width + 6 * self.spacing
        start_x = -total_width / 2 + self.letter_width / 2
        
        J_pos[0, :] += start_x
        C_pos[0, :] += start_x + self.letter_width + self.spacing
        N_pos[0, :] += start_x + 2 * (self.letter_width + self.spacing)
        d2_pos[0, :] += start_x + 3 * (self.letter_width + self.spacing)
        d0_pos[0, :] += start_x + 4 * (self.letter_width + self.spacing)
        d2b_pos[0, :] += start_x + 5 * (self.letter_width + self.spacing)
        d6_pos[0, :] += start_x + 6 * (self.letter_width + self.spacing)
        
        all_x = np.concatenate([J_pos[0], C_pos[0], N_pos[0], d2_pos[0], d0_pos[0], d2b_pos[0], d6_pos[0]])
        all_y = np.concatenate([J_pos[1], C_pos[1], N_pos[1], d2_pos[1], d0_pos[1], d2b_pos[1], d6_pos[1]])
        
        return np.array([all_x, all_y])
    
    def get_22EME_EDITION_formation(self):
        """Formation du texte 22EME EDITION (en deux lignes)."""
        # Ligne 1: 22EME
        robots_line1 = self.n // 2
        robots_per_char1 = robots_line1 // 5
        
        d2a_pos = self.digit_2(robots_per_char1)
        d2b_pos = self.digit_2(robots_per_char1)
        E1_pos = self.letter_E(robots_per_char1)
        M_pos = self.letter_M(robots_per_char1)
        E2_pos = self.letter_E(robots_per_char1)
        
        # Positionner ligne 1
        width1 = 5 * self.letter_width + 4 * self.spacing
        start_x1 = -width1 / 2 + self.letter_width / 2
        
        d2a_pos[0, :] += start_x1
        d2b_pos[0, :] += start_x1 + self.letter_width + self.spacing
        E1_pos[0, :] += start_x1 + 2 * (self.letter_width + self.spacing)
        M_pos[0, :] += start_x1 + 3 * (self.letter_width + self.spacing)
        E2_pos[0, :] += start_x1 + 4 * (self.letter_width + self.spacing)
        
        # Décaler vers le haut
        for pos in [d2a_pos, d2b_pos, E1_pos, M_pos, E2_pos]:
            pos[1, :] += 0.3
        
        # Ligne 2: EDITION
        robots_line2 = self.n - robots_line1
        robots_per_char2 = robots_line2 // 7
        
        E3_pos = self.letter_E(robots_per_char2)
        D_pos = self.letter_N(robots_per_char2)  # Using N shape rotated as D approximation
        I_pos = self.letter_I(robots_per_char2)
        T_pos = self.letter_I(robots_per_char2)  # T approximated as I with top bar
        I2_pos = self.letter_I(robots_per_char2)
        O_pos = self.digit_0(robots_per_char2)
        N2_pos = self.letter_N(robots_per_char2)
        
        # Positionner ligne 2
        width2 = 7 * self.letter_width + 6 * self.spacing
        start_x2 = -width2 / 2 + self.letter_width / 2
        
        E3_pos[0, :] += start_x2
        D_pos[0, :] += start_x2 + self.letter_width + self.spacing
        I_pos[0, :] += start_x2 + 2 * (self.letter_width + self.spacing)
        T_pos[0, :] += start_x2 + 3 * (self.letter_width + self.spacing)
        I2_pos[0, :] += start_x2 + 4 * (self.letter_width + self.spacing)
        O_pos[0, :] += start_x2 + 5 * (self.letter_width + self.spacing)
        N2_pos[0, :] += start_x2 + 6 * (self.letter_width + self.spacing)
        
        # Décaler vers le bas
        for pos in [E3_pos, D_pos, I_pos, T_pos, I2_pos, O_pos, N2_pos]:
            pos[1, :] -= 0.3
        
        all_x = np.concatenate([d2a_pos[0], d2b_pos[0], E1_pos[0], M_pos[0], E2_pos[0],
                                E3_pos[0], D_pos[0], I_pos[0], T_pos[0], I2_pos[0], O_pos[0], N2_pos[0]])
        all_y = np.concatenate([d2a_pos[1], d2b_pos[1], E1_pos[1], M_pos[1], E2_pos[1],
                                E3_pos[1], D_pos[1], I_pos[1], T_pos[1], I2_pos[1], O_pos[1], N2_pos[1]])
        
        return np.array([all_x, all_y])
    
    def get_FES_MEKNES_formation(self):
        """Formation du texte FES-MEKNES."""
        # 10 caractères: F E S - M E K N E S
        robots_per_char = self.n // 10
        remainder = self.n % 10
        
        F_pos = self.letter_F(robots_per_char + (1 if remainder >= 1 else 0))
        E1_pos = self.letter_E(robots_per_char + (1 if remainder >= 2 else 0))
        S1_pos = self.letter_S(robots_per_char + (1 if remainder >= 3 else 0))
        # Tiret représenté par une ligne horizontale courte
        dash_robots = robots_per_char + (1 if remainder >= 4 else 0)
        dash_x = np.linspace(-0.1, 0.1, dash_robots)
        dash_y = np.zeros(dash_robots)
        dash_pos = np.array([dash_x, dash_y])
        
        M_pos = self.letter_M(robots_per_char + (1 if remainder >= 5 else 0))
        E2_pos = self.letter_E(robots_per_char + (1 if remainder >= 6 else 0))
        K_pos = self.letter_N(robots_per_char + (1 if remainder >= 7 else 0))  # K approximated
        N_pos = self.letter_N(robots_per_char + (1 if remainder >= 8 else 0))
        E3_pos = self.letter_E(robots_per_char + (1 if remainder >= 9 else 0))
        S2_pos = self.letter_S(robots_per_char)
        
        # Positionner
        total_width = 10 * self.letter_width + 9 * self.spacing
        start_x = -total_width / 2 + self.letter_width / 2
        
        positions = [F_pos, E1_pos, S1_pos, dash_pos, M_pos, E2_pos, K_pos, N_pos, E3_pos, S2_pos]
        for i, pos in enumerate(positions):
            pos[0, :] += start_x + i * (self.letter_width + self.spacing)
        
        all_x = np.concatenate([pos[0] for pos in positions])
        all_y = np.concatenate([pos[1] for pos in positions])
        
        return np.array([all_x, all_y])