# src/utils/video_recorder.py
"""
ENREGISTREMENT VIDÉO
"""

import os
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from utils.config import config

class VideoRecorder:
    """Gère l'enregistrement vidéo des animations."""
    
    def __init__(self, filename="animation.mp4", fps=None):
        self.fps = fps or config.FPS
        self.filename = filename
        self.writer = None
        self.output_dir = config.VIDEO_DIR
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()

    def setup(self, fig):
        """Configure l'enregistreur avec la figure matplotlib."""
        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, self.filename)
        
        try:
            self.writer = FFMpegWriter(
                fps=self.fps, 
                metadata=dict(title='AmenMaroc Animation', artist='ANEM 2025'),
                bitrate=1800
            )
            self.writer.setup(fig, file_path, dpi=100)
            print(f"📹 Enregistrement vidéo initialisé: {file_path}")
            return True
        except Exception as e:
            print(f"⚠️ Erreur d'initialisation vidéo: {e}")
            self.writer = None
            return False

    def grab_frame(self):
        """Capture la frame actuelle."""
        if self.writer:
            try:
                self.writer.grab_frame()
            except Exception as e:
                print(f"⚠️ Erreur capture frame: {e}")

    def finish(self):
        """Finalise l'enregistrement."""
        if self.writer:
            try:
                self.writer.finish()
                print(f"✅ Vidéo sauvegardée: {self.filename}")
            except Exception as e:
                print(f"⚠️ Erreur finalisation vidéo: {e}")
            self.writer = None
