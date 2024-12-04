#----------------------------------------------------------------------------------------------------------------------#
# imports

import pygame
from etincelle import Etincelle
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from utiles import draw_arrow
import numpy as np


#----------------------------------------------------------------------------------------------------------------------#
# initialisation

# on initialise
pygame.init()

# couleurs
WHITE = (255, 255, 255)
METALLIC_GRAY = (169, 169, 169)
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# dimensions et titre de la fenêtre
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation de collisions élastiques")


#----------------------------------------------------------------------------------------------------------------------#
# paramètres du système

# Variables pour les masses
m1_mass = 100
m2_mass = 1
m1_size = 50 + len(str(m1_mass)) if len(str(m1_mass)) > 1 and len(str(m1_mass)) > len(str(m2_mass)) else 50
m2_size = 50
horizontal_line_y = 2 * height // 3
m1_pos = [width // 4 + 250, horizontal_line_y - m1_size - 2]
m2_pos = [width // 4 + 100, horizontal_line_y - m2_size - 2]

# vitesses initiales
m1_velocity = [-2, 0]
m2_velocity = [0, 0]

# mur
L_vertical_x = width // 10

# liste des vitesses avec les vitesses initiales
liste_v1 = [-2]
liste_v2 = [0]

# liste des coordonnées d'énergie pour le diagramme de phase avec les vitesses initiales
coords = [(liste_v1[0] * np.sqrt(m1_mass), liste_v2[0] * np.sqrt(m2_mass))]

# liste des étincelles
etincelles = []

# police compteur
font = pygame.font.SysFont('Arial', 36, italic=True)
collision_count = 0


#----------------------------------------------------------------------------------------------------------------------#
# graphique

radius = np.sqrt(m1_mass * m1_velocity[0]**2) # le rayon du cercle d'énergie
theta = np.linspace(0, 2 * np.pi, 500)
circle_x = radius * np.cos(theta)
circle_y = radius * np.sin(theta)

# on initialise la figure Matplotlib
fig, ax = plt.subplots(figsize=(6, 6), dpi=70)
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.plot(circle_x, circle_y, 'y-', label="Cercle d'énergie")  # on trace le cercle d'énergie
ax.axhline(0, color='white', linewidth=0.5, linestyle='--') # on place un axe x dans le cercle
ax.axvline(0, color='white', linewidth=0.5, linestyle='--') # de même y
# labels et titre
ax.set_xlabel(r"$v_1 \sqrt{m_1}$", fontsize=12, color='white')
ax.set_ylabel(r"$v_2 \sqrt{m_2}$", fontsize=12, color='white')
ax.set_title("Diagramme de phase", fontsize=12, color='white')

# on définit un canvas
points, = ax.plot([], [], 'ro', color='orange', label="Énergies atteintes")
lines, = ax.plot([], [], 'r-', alpha=0.5, color='orange', label="Chemin d'énergie")
canvas = FigureCanvas(fig)

# placer la legende en haut à droite
legend = fig.legend(loc='upper right', fontsize=10, frameon=False)

# police de la légende
for text in legend.get_texts():
    text.set_color('white')

def update_phase_diagram():
    """
    Met à jour le diagramme de phase avec de nouvelles coordonnées.

    Cette fonction ajoute les dernières coordonnées calculées à la liste `coords`,
    et met à jour les données des objets `points` et `lines` dans le diagramme de phase.
    Enfin, elle redessine le canevas pour refléter les changements.

    Arguments:
        Aucun

    Retour:
        Aucun
    """
    global coords
    coords.append((liste_v1[-1] * np.sqrt(m1_mass), liste_v2[-1] * np.sqrt(m2_mass)))
    x, y = zip(*coords)
    points.set_data(x, y)
    lines.set_data(x, y)
    canvas.draw()

def render_matplotlib(fig):
    """
    Transforme une figure matplotlib en surface pygame pour l'affichage.

    Arguments:
        fig(matplotlib.figure.Figure): la figure à afficher.

    Retour:
        Aucun
    """
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return pygame.image.fromstring(raw_data, size, "RGB")


#----------------------------------------------------------------------------------------------------------------------#
# boucle principale

clock = pygame.time.Clock()
running = True
while running:

    screen.fill(BLACK)
    # mur et sol
    pygame.draw.line(screen, WHITE, (width / 10 - 2, 2 * height / 3), (width, 2 * height / 3), 5)  # Ligne horizontale
    pygame.draw.line(screen, WHITE, (width / 10, height / 3), (width / 10, 2 * height / 3), 5)  # Ligne verticale

    # masses
    m1_rect = pygame.Rect(m1_pos[0], m1_pos[1], m1_size, m1_size)
    m2_rect = pygame.Rect(m2_pos[0], m2_pos[1], m2_size, m2_size)
    pygame.draw.rect(screen, LIGHT_BLUE, m1_rect)
    pygame.draw.rect(screen, METALLIC_GRAY, m2_rect)

    # Dessiner les flèches pour m1 et m2
    draw_arrow(screen, m1_pos, m1_velocity, m1_size, RED)
    draw_arrow(screen, m2_pos, m2_velocity, m2_size, RED)

    # collisions entre m1 et m2
    if m1_rect.colliderect(m2_rect):

        v1 = m1_velocity[0]
        v2 = m2_velocity[0]
        v1_prime = ((m1_mass - m2_mass) * v1 + 2 * m2_mass * v2) / (m1_mass + m2_mass)
        v2_prime = ((m2_mass - m1_mass) * v2 + 2 * m1_mass * v1) / (m1_mass + m2_mass)
        m1_velocity[0] = v1_prime
        m2_velocity[0] = v2_prime
        
        collision_count += 1

        liste_v1.append(v1_prime)
        liste_v2.append(v2_prime)
        

        # création étincelles
        for _ in range(7):

            velocity = [random.uniform(-3, 3), random.uniform(-3, 3)]
            etincelles.append(Etincelle(m2_pos[0] + m2_size // 2, m2_pos[1] + m2_size // 2, YELLOW, 30, velocity))

        update_phase_diagram()

    # bouger les masses
    m2_pos[0] += m2_velocity[0]
    m1_pos[0] += m1_velocity[0]

    # collision de m2 avec le mur
    if m2_pos[0] <= L_vertical_x:
        m2_velocity[0] = -m2_velocity[0]
        m2_pos[0] = L_vertical_x
        collision_count += 1
        
        liste_v1.append(m1_velocity[0])
        liste_v2.append(m2_velocity[0])

        # création étincelles
        for _ in range(7):

            velocity = [random.uniform(-3, 3), random.uniform(-3, 3)]
            etincelles.append(Etincelle(m2_pos[0], m2_pos[1] + m2_size // 2, RED, 30, velocity))

        update_phase_diagram()

    # affichage étincelles
    for etincelle in etincelles[:]:

        etincelle.update()
        etincelle.draw(screen)
        if etincelle.lifespan <= 0:
            etincelles.remove(etincelle)

    # gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # affichage du compteur de collisions
    collision_text = font.render(f"# Collisions: {collision_count}", True, WHITE)
    screen.blit(collision_text, (10, 10))

    phase_diagram_surface = render_matplotlib(fig)
    screen.blit(phase_diagram_surface, (width - 450, 30))

    pygame.display.flip()
    clock.tick(100)

pygame.quit()

# fin
#----------------------------------------------------------------------------------------------------------------------#