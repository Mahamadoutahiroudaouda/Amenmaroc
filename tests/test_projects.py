# tests/test_projects.py
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from projects.project_01_anem_lumiere import Project01AnemLumiere
from projects.project_02_monuments import Project02Monuments
from projects.project_11_naissance_nation import Project11NaissanceNation

class TestProjects(unittest.TestCase):
    def test_project_01_init(self):
        p = Project01AnemLumiere(n_robots=10)
        self.assertEqual(p.n, 10)
        self.assertTrue(hasattr(p, 'phases'))
        
    def test_project_02_init(self):
        p = Project02Monuments(n_robots=10)
        self.assertEqual(p.n, 10)

    def test_project_11_init(self):
        p = Project11NaissanceNation(n_robots=100)
        self.assertEqual(p.n, 100)
        self.assertTrue('1_desert' in p.phases)

if __name__ == '__main__':
    unittest.main()
