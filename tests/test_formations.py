# tests/test_formations.py
import unittest
import numpy as np
import sys
import os

# Ajouter src au path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from formations.base_formations import BaseFormations
from utils.config import config

class TestBaseFormations(unittest.TestCase):
    def setUp(self):
        self.n = 50
        self.base = BaseFormations(self.n)
        
    def test_circle_shape(self):
        pos = self.base.circle(radius=1.0)
        self.assertEqual(pos.shape, (2, self.n))
        # Vérifier que le rayon est constant
        radii = np.sqrt(pos[0]**2 + pos[1]**2)
        self.assertTrue(np.allclose(radii, 1.0))
        
    def test_grid_shape(self):
        pos = self.base.grid(rows=5, cols=10)
        self.assertEqual(pos.shape, (2, self.n))
        
    def test_random_positions(self):
        pos = self.base.random_positions()
        self.assertEqual(pos.shape, (2, self.n))
        # Vérifier les bornes
        self.assertTrue(np.all(pos[0] >= config.safe_zone['x_min']))
        self.assertTrue(np.all(pos[0] <= config.safe_zone['x_max']))

if __name__ == '__main__':
    unittest.main()
