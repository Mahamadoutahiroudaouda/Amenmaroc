# src/utils/performance.py
"""
ANALYSE DE PERFORMANCE
"""

import time
import psutil
import os

class PerformanceMonitor:
    """Moniteur de performance système et application."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.fps_start = time.time()
        self.frame_count = 0
        self.current_fps = 0
        
    def update(self):
        """Met à jour les métriques à chaque frame."""
        self.frame_count += 1
        elapsed = time.time() - self.fps_start
        if elapsed >= 1.0:
            self.current_fps = self.frame_count / elapsed
            self.frame_count = 0
            self.fps_start = time.time()
            return True # Une seconde s'est écoulée
        return False
        
    def get_metrics(self):
        """Retourne les métriques actuelles."""
        return {
            'fps': self.current_fps,
            'memory_mb': self.process.memory_info().rss / 1024 / 1024,
            'cpu_percent': self.process.cpu_percent()
        }
    
    def log_status(self):
        """Affiche les métriques."""
        m = self.get_metrics()
        print(f"PERF: {m['fps']:.1f} FPS | Mem: {m['memory_mb']:.1f} MB | CPU: {m['cpu_percent']}%")
