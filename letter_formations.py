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
        """Formation de la lettre M - TAILLE RÉDUITE."""
        n_vertical = max(2, robots_count // 4)
        n_diag = max(2, robots_count // 4)
        n_rest = robots_count - 2 * n_vertical - 2 * n_diag
        
        # Barre gauche
        x1 = np.full(n_vertical, -self.letter_width/2)
        y1 = np.linspace(-self.letter_height/2, self.letter_height/2, n_vertical)
        
        # Diagonale gauche
        x2 = np.linspace(-self.letter_width/2, 0, n_diag)
        y2 = np.linspace(self.letter_height/2, 0, n_diag)
        
        # Diagonale droite
        x3 = np.linspace(0, self.letter_width/2, n_diag)
        y3 = np.linspace(0, self.letter_height/2, n_diag)
        
        # Barre droite
        x4 = np.full(n_rest, self.letter_width/2)
        y4 = np.linspace(self.letter_height/2, -self.letter_height/2, n_rest)
        
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