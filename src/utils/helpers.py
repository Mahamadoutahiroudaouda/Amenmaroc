# src/utils/helpers.py
"""
FONCTIONS UTILITAIRES ET AIDE
"""

import numpy as np
import time
import logging

def setup_logger(name="AmenMaroc"):
    """Configure le logger pour le projet."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

class Timer:
    """Classe utilitaire pour mesurer le temps d'exécution."""
    def __init__(self):
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

def normalize_positions(positions, bounds):
    """Normalise les positions pour rester dans les bornes."""
    x_min, x_max, y_min, y_max = bounds
    positions[0] = np.clip(positions[0], x_min, x_max)
    positions[1] = np.clip(positions[1], y_min, y_max)
    return positions

def distance_matrix(positions):
    """Calcule la matrice de distance entre tous les robots."""
    n = positions.shape[1]
    x = positions[0]
    y = positions[1]
    
    dists = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            d = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)
            dists[i, j] = dists[j, i] = d
    return dists

def check_collisions(positions, min_dist=0.1):
    """Vérifie s'il y a des collisions entre robots."""
    dists = distance_matrix(positions)
    # Remplir la diagonale avec l'infini pour éviter l'auto-collision
    np.fill_diagonal(dists, np.inf)
    
    collisions = np.argwhere(dists < min_dist)
    return len(collisions) // 2  # Diviser par 2 car symétrique

def smooth_path(points, smoothing_factor=0.5):
    """Lisse un chemin donné par une série de points (simple moyenne mobile)."""
    # Simple exemple pour lisser des trajectoires si nécessaire
    return points # Placeholder implementation
