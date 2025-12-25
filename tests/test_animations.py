# tests/test_animations.py
import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from animations.color_animations import ColorAnimator

class TestColorAnimator(unittest.TestCase):
    def setUp(self):
        self.colors = ColorAnimator()
        self.positions = np.zeros((2, 50))
        
    def test_get_color(self):
        # Test basic retrieval
        c = self.colors.get_phase_color(self.positions, "default", 0, 0)
        self.assertIsInstance(c, str)
        self.assertTrue(c.startswith('#') or c in ['red', 'blue', 'white'])

    def test_gradient(self):
        # Implement specific test if gradient logic exists
        pass

if __name__ == '__main__':
    unittest.main()
