# src/main/demo_all_projects.py
"""
POINT D'ENTRÉE PRINCIPAL - VERSION COMPLÈTE AMÉLIORÉE
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter

# Ajouter le chemin src au Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from projects.project_01_anem_lumiere import Project01AnemLumiere
from projects.project_02_monuments import Project02Monuments
from projects.project_03_vagues import Project03Vagues
from projects.project_04_constellations import Project04Constellations
from projects.project_05_feux_artifice import Project05FeuxArtifice
from projects.project_06_spirale_fibonacci import Project06SpiraleFibonacci
from projects.project_07_faune import Project07FauneNiger
from projects.project_08_calligraphie import Project08Calligraphie
from projects.project_09_parade import Project09GrandeParade
from projects.project_10_architecture import Project10PatrimoineArchitectural

from utils.config import config

def setup_visualization():
    """Configure la visualisation matplotlib."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Configuration de l'arène
    ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
    ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Cadre décoratif
    arena_border = plt.Rectangle(
        (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
        config.ARENA_WIDTH, config.ARENA_HEIGHT,
        fill=False, edgecolor='white', linewidth=2, alpha=0.5
    )
    ax.add_patch(arena_border)
    
    return fig, ax

def run_project_01_full():
    """Exécute le Projet 1: ANEM en Lumière avec visualisation complète."""
    print("🎬 LANCEMENT DU PROJET #1: ANEM EN LUMIÈRE")
    
    project = Project01AnemLumiere()
    fig, ax = setup_visualization()
    
    # Configuration vidéo (optionnel)
    video_writer = None
    try:
        video_writer = FFMpegWriter(fps=config.FPS, metadata=dict(artist='ANEM 2025'))
        video_path = os.path.join(config.VIDEO_DIR, "projet_01_anem_lumiere.mp4")
        os.makedirs(config.VIDEO_DIR, exist_ok=True)
        video_writer.setup(fig, video_path, dpi=100)
        print(f"📹 Enregistrement vidéo activé: {video_path}")
    except Exception as e:
        print(f"⚠️  Enregistrement vidéo désactivé: {e}")
        video_writer = None
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('black')
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='white', linewidth=2, alpha=0.3
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #1: ANEM EN LUMIÈRE",
                color='white', fontsize=16, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR CHAQUE ROBOT
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots AVEC LES BONNES COULEURS
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,  # Utiliser la liste des couleurs individuelles
                      s=100, alpha=0.9, 
                      edgecolors='white', linewidth=1.5,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Phase: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Légende des couleurs pour le drapeau
            if "drapeau" in phase_name.lower() or "pluie" in phase_name.lower():
                legend_text = "🟠 Orange ⚪ Blanc 🟢 Vert"
                ax.text(
                    0.5, 0.02, legend_text,
                    transform=ax.transAxes, color='white', fontsize=12,
                    verticalalignment='bottom', horizontalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
                )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor=config.COLORS['orange_niger'], alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Pourcentage de progression
            ax.text(
                0.98, 0.02, f"Progression: {progress*100:.0f}%",
                transform=ax.transAxes, color='white', fontsize=10,
                verticalalignment='bottom', horizontalalignment='right'
            )
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            # Capturer pour la vidéo
            if video_writer:
                video_writer.grab_frame()
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:20} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Fermer proprement
        if video_writer:
            video_writer.finish()
            print("✅ Vidéo sauvegardée")
        
        print("🎉 Animation terminée!")
        plt.show()

def run_project_01_fast():
    """Version rapide pour test (sans visualisation temps réel)."""
    print("⚡ LANCEMENT RAPIDE DU PROJET #1")
    
    project = Project01AnemLumiere(50)  # Test avec 50 robots
    
    frame_count = 0
    for positions, phase_name, time_val, frame in project.run_complete_animation():
        if frame_count % 30 == 0:  # Afficher toutes les secondes
            # Compter les couleurs pour vérification
            colors_count = {"orange": 0, "blanc": 0, "vert": 0, "autre": 0}
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                if color == config.COLORS['orange_niger']:
                    colors_count["orange"] += 1
                elif color == config.COLORS['blanc_pure']:
                    colors_count["blanc"] += 1
                elif color == config.COLORS['vert_espoir']:
                    colors_count["vert"] += 1
                else:
                    colors_count["autre"] += 1
            
            print(f"📊 Frame {frame:04d} | {phase_name:20} | {time_val:05.1f}s | "
                  f"Couleurs: 🟠{colors_count['orange']} ⚪{colors_count['blanc']} 🟢{colors_count['vert']}")
        
        frame_count += 1
    
    print("✅ Test rapide terminé!")

def run_project_01_colors_test():
    """Test spécifique des couleurs du drapeau."""
    print("🎨 TEST SPÉCIFIQUE DES COULEURS DRAPEAU")
    
    project = Project01AnemLumiere(30)  #Petit test
    
    # Tester chaque phase rapidement
    test_phases = ['pluie drapeau', 'drapeau pulsant']
    
    for phase_name in test_phases:
        print(f"\n🧪 Test phase: {phase_name}")
        
        # Positions de test
        positions = project.letters.random_positions()
        
        # Tester différentes frames
        for time_val in [0, 1, 2, 3]:
            colors_count = {"orange": 0, "blanc": 0, "vert": 0}
            
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                if color == config.COLORS['orange_niger']:
                    colors_count["orange"] += 1
                elif color == config.COLORS['blanc_pure']:
                    colors_count["blanc"] += 1
                elif color == config.COLORS['vert_espoir']:
                    colors_count["vert"] += 1
            
            print(f"   t={time_val}s: 🟠{colors_count['orange']} ⚪{colors_count['blanc']} 🟢{colors_count['vert']}")
    
    print("✅ Test couleurs terminé!")

def run_project_02_full():
    """Exécute le Projet 2: Monuments Iconiques du Niger."""
    print("🏛️  LANCEMENT DU PROJET #2: MONUMENTS ICONIQUES DU NIGER")
    
    project = Project02Monuments()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('black')
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='white', linewidth=2, alpha=0.3
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #2: MONUMENTS ICONIQUES DU NIGER",
                color='white', fontsize=16, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=100, alpha=0.9, 
                      edgecolors='white', linewidth=1.5,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Phase: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor=config.COLORS['terre_agadez'], alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 2 terminée!")
        plt.show()

def run_project_03_full():
    """Exécute le Projet 3: Vagues Océaniques."""
    print("🌊 LANCEMENT DU PROJET #3: VAGUES OCÉANIQUES")
    
    project = Project03Vagues()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('black')
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='white', linewidth=2, alpha=0.3
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #3: VAGUES OCÉANIQUES",
                color='white', fontsize=16, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LES VAGUES
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=100, alpha=0.9, 
                      edgecolors='white', linewidth=1.5,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Phase: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor=config.COLORS['bleu_profond'], alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Légende des couleurs pour les vagues
            if "vague" in phase_name.lower() or "ocean" in phase_name.lower():
                legend_text = "🌊 Profond → Turquoise → Écume 🌊"
                ax.text(
                    0.5, 0.02, legend_text,
                    transform=ax.transAxes, color='white', fontsize=12,
                    verticalalignment='bottom', horizontalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
                )
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 3 terminée!")
        plt.show()

def run_project_04_full():
    """Exécute le Projet 4: Constellation Vivante."""
    print("🌟 LANCEMENT DU PROJET #4: CONSTELLATION VIVANTE")
    
    project = Project04Constellations()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base avec fond étoilé
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#000033')  # Fond bleu nuit pour l'espace
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='white', linewidth=2, alpha=0.3
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #4: CONSTELLATION VIVANTE",
                color='white', fontsize=16, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LES ÉTOILES
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots (étoiles)
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=80, alpha=0.9, 
                      edgecolors='white', linewidth=1,
                      marker='*')  # Forme d'étoile
            
            # Informations en temps réel
            info_text = (
                f"Phase: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor=config.COLORS['or_soleil'], alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 4 terminée!")
        plt.show()

def run_project_05_full():
    """Exécute le Projet 5: Feu d'Artifice Nigérien."""
    print("🎆 LANCEMENT DU PROJET #5: FEU D'ARTIFICE NIGÉRIEN")
    
    project = Project05FeuxArtifice()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base avec fond nocturne
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#001122')  # Fond bleu nuit profond
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Sol (ligne horizontale)
            sol_line = plt.Line2D([-1.6, 1.6], [-0.9, -0.9], color='#333333', linewidth=3)
            ax.add_line(sol_line)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #5: FEU D'ARTIFICE NIGÉRIEN",
                color='white', fontsize=16, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LES FEUX D'ARTIFICE
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots (étincelles)
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=60, alpha=0.9, 
                      edgecolors='yellow', linewidth=0.5,
                      marker='.')  # Points pour les étincelles
            
            # Informations en temps réel
            info_text = (
                f"Phase: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor=config.COLORS['orange_niger'], alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 5 terminée!")
        plt.show()

def run_project_06_full():
    """Exécute le Projet 6: Spirale d'Or de Fibonacci."""
    print("🌀 LANCEMENT DU PROJET #6: SPIRALE D'OR DE FIBONACCI")
    
    project = Project06SpiraleFibonacci()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#1a1a2e')  # Fond bleu nuit profond
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='gold', linewidth=2, alpha=0.5
            )
            ax.add_patch(arena_border)
            
            # Titre principal avec info mathématique
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #6: SPIRALE D'OR DE FIBONACCI\n"
                f"φ = {project.phi:.6f}",
                color='gold', fontsize=14, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LA SPIRALE
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=80, alpha=0.9, 
                      edgecolors='white', linewidth=0.5,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Phase: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor='gold', alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Information mathématique
            math_text = f"Nombre d'or φ = {project.phi:.6f}"
            ax.text(
                0.5, 0.02, math_text,
                transform=ax.transAxes, color='gold', fontsize=12,
                verticalalignment='bottom', horizontalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 6 terminée!")
        plt.show()

def _get_conservation_info(animal_name):
    """Retourne les informations de conservation pour chaque animal."""
    conservation_data = {
        'Girafe': 'Giraffa camelopardalis peralta - Vulnérable',
        'Elephant': 'Loxodonta africana - En danger',
        'Addax': 'Addax nasomaculatus - En danger critique',
        'Dromadaire': 'Camelus dromedarius - Domestique'
    }
    return conservation_data.get(animal_name, 'Protégeons la biodiversité!')

def _add_savana_decor(ax, time_val):
    """Ajoute des éléments décoratifs de savane."""
    # Soleil
    sun = plt.Circle((1.2, 0.8), 0.1, color='yellow', alpha=0.7)
    ax.add_patch(sun)
    
    # Nuages animés
    cloud_x = 0.5 + 0.1 * np.sin(time_val * 0.3)
    cloud1 = plt.Circle((cloud_x - 1.5, 0.6), 0.08, color='white', alpha=0.6)
    cloud2 = plt.Circle((cloud_x - 1.4, 0.65), 0.1, color='white', alpha=0.6)
    cloud3 = plt.Circle((cloud_x - 1.3, 0.6), 0.07, color='white', alpha=0.6)
    ax.add_patch(cloud1)
    ax.add_patch(cloud2)
    ax.add_patch(cloud3)
    
    # Ligne d'horizon
    horizon = plt.Rectangle(
        (-1.6, -0.9), 3.2, 0.3,
        facecolor='#8B4513', alpha=0.3
    )
    ax.add_patch(horizon)

def run_project_07_full():
    """Exécute le Projet 7: Faune du Niger."""
    print("🦒 LANCEMENT DU PROJET #7: FAUNE DU NIGER")
    
    project = Project07FauneNiger()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#2d5016')  # Fond vert savane
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='#8B4513', linewidth=2, alpha=0.5
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            animal_emoji = {
                'Girafe': '🦒',
                'Elephant': '🐘',
                'Addax': '🐐',
                'Dromadaire': '🐪'
            }
            emoji = animal_emoji.get(phase_name.split()[0], '🐾')
            
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #7: FAUNE DU NIGER\n"
                f"{emoji} {phase_name}",
                color='#8B4513', fontsize=14, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LA FAUNE
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=80, alpha=0.9, 
                      edgecolors='white', linewidth=0.5,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Animal: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor='#8B4513', alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Information sur la biodiversité
            conservation_text = _get_conservation_info(phase_name)
            ax.text(
                0.5, 0.02, conservation_text,
                transform=ax.transAxes, color='#8B4513', fontsize=10,
                verticalalignment='bottom', horizontalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Ajouter un décor de savane
            _add_savana_decor(ax, time_val)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:20} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 7 terminée!")
        plt.show()

def test_formations_only():
    """Test simple des formations sans animation."""
    print("🧪 TEST DES FORMATIONS")
    
    from formations.letter_formations import LetterFormations
    from formations.base_formations import BaseFormations
    from formations.geo_formations import GeoFormations
    
    letters = LetterFormations(50)
    base = BaseFormations(50)
    geo = GeoFormations(50)
    
    # Tester quelques formations
    formations = {
        "Aléatoire": base.random_positions(),
        "Cercle": base.circle(),
        "ANEM": letters.get_ANEM_formation(),
        "Drapeau": base.grid(rows=3, cols=17),  # 3 bandes
        "Carte Niger": geo.get_niger_map_formation(),
        "Étoile": base.star_improved(n_points=8)
    }
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, positions) in enumerate(formations.items()):
        if idx >= len(axes):
            break
            
        ax = axes[idx]
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.0, 1.0)
        ax.set_facecolor('black')
        ax.set_aspect('equal')
        ax.set_title(f"Formation: {name}", color='white', fontsize=12)
        
        # Couleurs spécifiques pour certaines formations
        if name == "Drapeau":
            colors_list = []
            for i in range(positions.shape[1]):
                bande = i // (positions.shape[1] // 3)
                if bande == 0:
                    colors_list.append(config.COLORS['orange_niger'])
                elif bande == 1:
                    colors_list.append(config.COLORS['blanc_pure'])
                else:
                    colors_list.append(config.COLORS['vert_espoir'])
            ax.scatter(positions[0], positions[1], c=colors_list, s=50, alpha=0.8)
        else:
            ax.scatter(positions[0], positions[1], 
                      c=config.COLORS['orange_niger'], s=50, alpha=0.8)
        
        # Afficher le nombre de robots
        ax.text(0.02, 0.98, f"Robots: {positions.shape[1]}", 
               transform=ax.transAxes, color='white', fontsize=9,
               verticalalignment='top')
    
    # Cacher les axes non utilisés
    for idx in range(len(formations), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Test des formations terminé!")

# Mettre à jour le menu principal
def main():
    """Fonction principale avec menu interactif."""
    print("=" * 60)
    print("🤖 ROBOTARIUM SWARM - ANEM 2025")
    print("🎯 SYSTÈME DE LANCEMENT DES PROJETS")
    print("=" * 60)
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. 🎬 Projet #1: ANEM en Lumière")
        print("2. 🏛️  Projet #2: Monuments Iconiques du Niger")
        print("3. 🌊 Projet #3: Vagues Océaniques")
        print("4. 🌟 Projet #4: Constellation Vivante")
        print("5. 🎆 Projet #5: Feu d'Artifice Nigérien")
        print("6. 🌀 Projet #6: Spirale d'Or de Fibonacci")
        print("7. 🦒 Projet #7: Faune du Niger")
        print("8. 📜 Projet #8: Calligraphie Arabe Animée")
        print("9. 🎪 Projet #9: La Grande Parade")
        print("10. 🏛️  Projet #10: Patrimoine Architectural")  # NOUVEAU
        print("11. ⚡ Projet #1: Version rapide")
        print("12. 🎨 Test spécifique des couleurs drapeau")
        print("13. 🧪 Tester les formations seulement")
        print("14. 🚪 Quitter")  # Décalé à 14
        
        choix = input("\n🎮 Choisissez une option (1-14): ").strip()
        
        if choix == "1":
            run_project_01_full()
        elif choix == "2":
            run_project_02_full()
        elif choix == "3":
            run_project_03_full()
        elif choix == "4":
            run_project_04_full()
        elif choix == "5":
            run_project_05_full()
        elif choix == "6":
            run_project_06_full()
        elif choix == "7":
            run_project_07_full()
        elif choix == "8":
            run_project_08_full()
        elif choix == "9":
            run_project_09_full()
        elif choix == "10":
            run_project_10_full()  # NOUVEAU
        elif choix == "11":
            run_project_01_fast()
        elif choix == "12":
            run_project_01_colors_test()
        elif choix == "13":
            test_formations_only()
        elif choix == "14":
            print("👋 Au revoir ! À bientôt sur Robotarium ANEM 2025!")
            break
        else:
            print("❌ Choix invalide. Veuillez choisir 1-14.")

# Ajouter la fonction pour le projet 10
def run_project_10_full():
    """Exécute le Projet 10: Patrimoine Architectural."""
    print("🏛️  LANCEMENT DU PROJET #10: PATRIMOINE ARCHITECTURAL")
    
    project = Project10PatrimoineArchitectural()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base avec fond désertique
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#F5DEB3')  # Fond sable désert
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif style architectural
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='#8B4513', linewidth=2, alpha=0.7
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #10: PATRIMOINE ARCHITECTURAL\n"
                f"{phase_name}",
                color='#8B4513', fontsize=14, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR L'ARCHITECTURE
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=80, alpha=0.9, 
                      edgecolors='#8B4513', linewidth=0.5,
                      marker='s')  # Forme carrée pour l'architecture
            
            # Informations en temps réel
            info_text = (
                f"Édifice: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='#8B4513', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#F5DEB3', alpha=0.8)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor='#8B4513', alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Information sur les matériaux
            material_info = _get_material_info(phase_name)
            ax.text(
                0.5, 0.02, material_info,
                transform=ax.transAxes, color='#8B4513', fontsize=10,
                verticalalignment='bottom', horizontalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#F5DEB3', alpha=0.8)
            )
            
            # Ajouter des éléments de décor désertique
            _add_desert_decor(ax, time_val)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 10 terminée!")
        plt.show()

def _get_material_info(phase_name):
    """Retourne les informations sur les matériaux pour chaque phase."""
    materials_data = {
        'Case Traditionnel Haoussa': 'Matériaux: Terre crue (banco) + Paille',
        'Mosquée de Zinder': 'Matériaux: Pierre + Bois de palmier + Terre',
        'Sultanat de Zinder': 'Matériaux: Pierre taillée + Bois précieux',
        'Village Fortifié': 'Matériaux: Terre battue + Pierre défensive'
    }
    return materials_data.get(phase_name, 'Architecture traditionnelle nigérienne')

def _add_desert_decor(ax, time_val):
    """Ajoute des éléments décoratifs désertiques."""
    # Dunes de sable
    dune_y = -0.85
    dune_x = np.linspace(-1.6, 1.6, 50)
    dune_height = 0.05 * np.sin(2*np.pi*0.1*time_val + dune_x*3)
    ax.fill_between(dune_x, dune_y, dune_y + dune_height, color='#DEB887', alpha=0.6)
    
    # Palmiers
    palm_positions = [(-1.2, -0.7), (1.2, -0.7), (0.0, -0.8)]
    for palm_x, palm_y in palm_positions:
        # Tronc
        trunk = plt.Rectangle((palm_x-0.02, palm_y), 0.04, 0.2, color='#8B4513', alpha=0.8)
        ax.add_patch(trunk)
        
        # Feuilles
        for i in range(4):
            angle = i * np.pi/2 + time_val * 0.2
            leaf_x = palm_x + 0.1 * np.cos(angle)
            leaf_y = palm_y + 0.2 + 0.1 * np.sin(angle)
            leaf = plt.Circle((leaf_x, leaf_y), 0.08, color='#228B22', alpha=0.6)
            ax.add_patch(leaf)

# Ajouter la fonction pour le projet 9
def run_project_09_full():
    """Exécute le Projet 9: La Grande Parade."""
    print("🎪 LANCEMENT DU PROJET #9: LA GRANDE PARADE")
    
    project = Project09GrandeParade()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base avec fond de spectacle
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#1a1a2e')  # Fond bleu nuit de spectacle
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre de scène
            stage_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='gold', linewidth=3, alpha=0.7
            )
            ax.add_patch(stage_border)
            
            # Titre principal avec numéro de tableau
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #9: LA GRANDE PARADE\n"
                f"Tableau: {phase_name}",
                color='gold', fontsize=14, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LA PARADE
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=80, alpha=0.9, 
                      edgecolors='white', linewidth=0.5,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Tableau: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='white', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Barre de progression globale
            total_duration = sum(project.phases.values())
            progress = time_val / total_duration
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor='gold', alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Compte à rebours du spectacle
            remaining_time = total_duration - time_val
            time_text = f"Fin du spectacle dans: {remaining_time:05.1f}s"
            ax.text(
                0.5, 0.02, time_text,
                transform=ax.transAxes, color='gold', fontsize=12,
                verticalalignment='bottom', horizontalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7)
            )
            
            # Effets de lumière de scène
            _add_stage_effects(ax, time_val, phase_name)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Spectacle interrompu par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant le spectacle: {e}")
    finally:
        print("🎉 Spectacle Projet 9 terminé!")
        plt.show()

def _add_stage_effects(ax, time_val, phase_name):
    """Ajoute des effets de scène selon le tableau."""
    # Projecteurs colorés
    spotlights = [
        {'pos': (-1.2, 0.8), 'color': '#FF6B6B', 'size': 0.3},
        {'pos': (1.2, 0.8), 'color': '#4ECDC4', 'size': 0.3},
        {'pos': (0, -0.8), 'color': '#45B7D1', 'size': 0.4}
    ]
    
    for spotlight in spotlights:
        x, y = spotlight['pos']
        size = spotlight['size']
        color = spotlight['color']
        
        # Animation des projecteurs
        pulse = 0.7 + 0.3 * np.sin(2*np.pi*0.3*time_val)
        alpha = 0.2 * pulse
        
        circle = plt.Circle((x, y), size * pulse, color=color, alpha=alpha)
        ax.add_patch(circle)
    
    # Effets spéciaux selon le tableau
    if 'artifice' in phase_name.lower():
        # Étoiles filantes
        for i in range(3):
            star_x = -1.5 + 3 * ((time_val * 0.5 + i) % 1.0)
            star_y = 0.8 - 0.5 * ((time_val * 0.3 + i*0.7) % 1.0)
            star = plt.Circle((star_x, star_y), 0.02, color='white', alpha=0.8)
            ax.add_patch(star)
    
    elif 'coeur' in phase_name.lower():
        # Cœurs volants
        for i in range(2):
            heart_x = -1.0 + 2 * ((time_val * 0.2 + i*0.5) % 1.0)
            heart_y = 0.6 + 0.2 * np.sin(2*np.pi*0.4*time_val + i)
            heart = plt.Circle((heart_x, heart_y), 0.05, color='#E74C3C', alpha=0.6)
            ax.add_patch(heart)
        
# Ajouter la fonction pour le projet 8
def run_project_08_full():
    """Exécute le Projet 8: Calligraphie Arabe Animée."""
    print("📜 LANCEMENT DU PROJET #8: CALLIGRAPHIE ARABE ANIMÉE")
    
    project = Project08Calligraphie()
    fig, ax = setup_visualization()
    
    # Animation principale
    frame_count = 0
    start_time = None
    
    try:
        for positions, phase_name, time_val, frame in project.run_complete_animation():
            if start_time is None:
                start_time = time_val
            
            ax.clear()
            
            # Configuration de base avec fond parchemin
            ax.set_xlim(-config.ARENA_WIDTH/2, config.ARENA_WIDTH/2)
            ax.set_ylim(-config.ARENA_HEIGHT/2, config.ARENA_HEIGHT/2)
            ax.set_facecolor('#FDF6E3')  # Fond parchemin
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Cadre décoratif style oriental
            arena_border = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2),
                config.ARENA_WIDTH, config.ARENA_HEIGHT,
                fill=False, edgecolor='#8B4513', linewidth=3, alpha=0.7
            )
            ax.add_patch(arena_border)
            
            # Titre principal
            ax.set_title(
                f"ANEM 2025 - Robotarium Swarm\n"
                f"PROJET #8: CALLIGRAPHIE ARABE ANIMÉE\n"
                f"{phase_name}",
                color='#8B4513', fontsize=14, pad=20, weight='bold'
            )
            
            # GÉNÉRER LES COULEURS POUR LA CALLIGRAPHIE
            colors_list = []
            for i in range(positions.shape[1]):
                color = project.colors.get_phase_color(positions, phase_name, time_val, i)
                colors_list.append(color)
            
            # Afficher les robots (points d'encre)
            ax.scatter(positions[0], positions[1], 
                      c=colors_list,
                      s=100, alpha=0.9, 
                      edgecolors='gold', linewidth=1,
                      marker='o')
            
            # Informations en temps réel
            info_text = (
                f"Mot: {phase_name}\n"
                f"Temps: {time_val:05.1f}s\n"
                f"Robots: {config.N_ROBOTS}\n"
                f"Frame: {frame:04d}"
            )
            
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes, color='#8B4513', fontsize=11,
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#FDF6E3', alpha=0.8)
            )
            
            # Barre de progression
            progress = time_val / sum(project.phases.values())
            progress_bar = plt.Rectangle(
                (-config.ARENA_WIDTH/2, -config.ARENA_HEIGHT/2 - 0.1),
                config.ARENA_WIDTH * progress, 0.03,
                facecolor='#8B4513', alpha=0.8
            )
            ax.add_patch(progress_bar)
            
            # Information sur le style calligraphique
            style_info = project.styles.get(phase_name.split('_')[0], 'Thuluth')
            style_text = f"Style: {style_info.title()}"
            ax.text(
                0.5, 0.02, style_text,
                transform=ax.transAxes, color='#8B4513', fontsize=12,
                verticalalignment='bottom', horizontalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#FDF6E3', alpha=0.8)
            )
            
            # Ajouter des éléments décoratifs orientaux
            _add_oriental_decor(ax, time_val)
            
            # Mettre à jour l'affichage
            plt.draw()
            plt.pause(1/config.FPS)
            
            frame_count += 1
            
            # Log de progression
            if frame_count % 30 == 0:
                print(f"📊 Frame {frame:04d} | {phase_name:25} | {time_val:05.1f}s")
    
    except KeyboardInterrupt:
        print("\n⏹️  Animation interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur pendant l'animation: {e}")
    finally:
        print("🎉 Animation Projet 8 terminée!")
        plt.show()

def _add_oriental_decor(ax, time_val):
    """Ajoute des éléments décoratifs orientaux."""
    # Motifs géométriques dans les coins
    corners = [(-1.5, 0.8), (1.5, 0.8), (-1.5, -0.8), (1.5, -0.8)]
    
    for corner_x, corner_y in corners:
        # Rosace orientale
        t_rosace = np.linspace(0, 2*np.pi, 8)
        rosace_x = corner_x + 0.1 * np.cos(t_rosace)
        rosace_y = corner_y + 0.1 * np.sin(t_rosace)
        ax.plot(rosace_x, rosace_y, color='#8B4513', alpha=0.5, linewidth=1)

if __name__ == "__main__":
    main()