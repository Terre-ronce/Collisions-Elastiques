import pygame


# couleurs
WHITE = (255, 255, 255)

def draw_arrow(screen, pos, velocity, masse_size, color, size=40):
    """
    Dessine une flèche à partir de la position de l'objet, avec une longueur fixe et affiche la vitesse.

    Paramètres:
        screen (pygame.Surface): La surface sur laquelle la flèche sera dessinée.
        pos (tuple): La position de l'objet.
        velocity (tuple): La vitesse de l'objet.
        color (tuple): La couleur de la flèche.
        masse_size (int): La taille de la masse.
        size (int, optional): La longueur de la flèche. Par défaut, 40.

    Retours:
        None
    """
    # police
    speed_font = pygame.font.SysFont(None, 24)

    # NNormaliser la vitesse
    if velocity[0] != 0 or velocity[1] != 0:  # pas de cuck norris
        norm = (velocity[0] ** 2 + velocity[1] ** 2) ** 0.5
        unit_velocity = [velocity[0] / norm, velocity[1] / norm]
    else:
        norm = 0  # pas de mouvement
        unit_velocity = [0, 0]  # pas de flèche

    # position de la flèche
    start_pos = (pos[0] + masse_size // 2, pos[1] + masse_size // 2)  # centre de la masse
    end_pos = (
        start_pos[0] + unit_velocity[0] * size,
        start_pos[1] + unit_velocity[1] * size,
    )

    # tige
    pygame.draw.line(screen, color, start_pos, end_pos, 3)

    # pointe
    arrow_size = 10
    angle = pygame.math.Vector2(unit_velocity).angle_to((1, 0))
    arrow_point1 = (
        end_pos[0] + arrow_size * pygame.math.Vector2(1, 0).rotate(angle + 150).x,
        end_pos[1] - arrow_size * pygame.math.Vector2(1, 0).rotate(angle + 150).y,
    )
    arrow_point2 = (
        end_pos[0] + arrow_size * pygame.math.Vector2(1, 0).rotate(angle - 150).x,
        end_pos[1] - arrow_size * pygame.math.Vector2(1, 0).rotate(angle - 150).y,
    )
    pygame.draw.polygon(screen, color, [end_pos, arrow_point1, arrow_point2])

    # valeur de la vitesse (avec maj)
    speed_text = speed_font.render(f"{norm:.2f}", True, WHITE)
    text_pos = (pos[0] + masse_size // 2 - speed_text.get_width() // 2, pos[1] - 20)
    screen.blit(speed_text, text_pos)