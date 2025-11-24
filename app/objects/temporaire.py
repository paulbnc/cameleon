import numpy as np
import random
import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
TAILLE_CASE = 40
MARGE = 50
COULEUR_FOND = (189, 189, 189)
COULEUR_CASE_CACHEE = (150, 150, 150)
COULEUR_CASE_REVELEE = (220, 220, 220)
COULEUR_BOMBE = (255, 0, 0)
COULEUR_TEXTE = (0, 0, 0)
COULEUR_GRILLE = (100, 100, 100)
COULEUR_DRAPEAU = (255, 100, 0)

# Couleurs pour les nombres
COULEURS_NOMBRES = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128)
}

def bombe(lignes=8, colonnes=8, premier_clic=None):
    bombes = np.zeros((lignes, colonnes), dtype=int)
    cases_interdites = set()
    
    # Si c'est après le premier clic, interdire la case cliquée et ses voisines
    if premier_clic is not None:
        i_clic, j_clic = premier_clic
        for ligne in range(i_clic-1, i_clic+2):
            if ligne > -1 and ligne < lignes:
                for colonne in range(j_clic-1, j_clic+2):
                    if colonne > -1 and colonne < colonnes:
                        cases_interdites.add((ligne, colonne))
    
    for i in range(lignes):
        for j in range(colonnes):
            if (i, j) not in cases_interdites:
                x = random.randint(1, 4)
                if x == 1:
                    bombes[i][j] = -1
    return bombes

def compter(bombes, i, j):
    if bombes[i][j] == -1:
        return -1
    nbre = 0
    for ligne in range(i-1, i+2):
        if ligne > -1 and ligne < len(bombes):
            for colonne in range(j-1, j+2):
                if colonne > -1 and colonne < len(bombes[0]):
                    if bombes[ligne][colonne] == -1:
                        nbre += 1
    return nbre

def afficher_case(affichage, bombes, i, j, drapeaux):
    if (i, j) in drapeaux:
        return
    
    valeur = compter(bombes, i, j)
    affichage[i][j] = valeur
    
    if valeur == 0:
        for ligne in range(i-1, i+2):
            if ligne > -1 and ligne < len(bombes):
                for colonne in range(j-1, j+2):
                    if colonne > -1 and colonne < len(bombes[0]):
                        if affichage[ligne][colonne] == -2 and (ligne, colonne) not in drapeaux:
                            afficher_case(affichage, bombes, ligne, colonne, drapeaux)

def dessiner_grille(ecran, affichage, bombes, lignes, colonnes, perdu, drapeaux):
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    
    for i in range(lignes):
        for j in range(colonnes):
            x = MARGE + j * TAILLE_CASE
            y = MARGE + i * TAILLE_CASE
            
            # Dessiner la case
            if affichage[i][j] == -2:  # Case non révélée
                couleur = COULEUR_CASE_CACHEE
                pygame.draw.rect(ecran, couleur, (x, y, TAILLE_CASE, TAILLE_CASE))
                pygame.draw.rect(ecran, COULEUR_GRILLE, (x, y, TAILLE_CASE, TAILLE_CASE), 2)
                
                # Dessiner le drapeau si présent
                if (i, j) in drapeaux:
                    pygame.draw.polygon(ecran, COULEUR_DRAPEAU, [
                        (x + 10, y + 10),
                        (x + 30, y + 20),
                        (x + 10, y + 30)
                    ])
                    pygame.draw.line(ecran, COULEUR_TEXTE, (x + 10, y + 10), (x + 10, y + 35), 2)
            else:  # Case révélée
                pygame.draw.rect(ecran, COULEUR_CASE_REVELEE, (x, y, TAILLE_CASE, TAILLE_CASE))
                pygame.draw.rect(ecran, COULEUR_GRILLE, (x, y, TAILLE_CASE, TAILLE_CASE), 1)
                
                if affichage[i][j] == -1 or (perdu and bombes[i][j] == -1):  # Bombe
                    pygame.draw.circle(ecran, COULEUR_BOMBE, (x + TAILLE_CASE//2, y + TAILLE_CASE//2), TAILLE_CASE//3)
                elif affichage[i][j] > 0:  # Nombre
                    texte = font.render(str(affichage[i][j]), True, COULEURS_NOMBRES[affichage[i][j]])
                    rect_texte = texte.get_rect(center=(x + TAILLE_CASE//2, y + TAILLE_CASE//2))
                    ecran.blit(texte, rect_texte)

def dessiner_menu(ecran, largeur, hauteur):
    font_title = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 48)
    
    ecran.fill(COULEUR_FOND)
    
    titre = font_title.render("DÉMINEUR", True, COULEUR_TEXTE)
    rect_titre = titre.get_rect(center=(largeur//2, hauteur//3))
    ecran.blit(titre, rect_titre)
    
    texte1 = font.render("Cliquez pour commencer", True, COULEUR_TEXTE)
    rect1 = texte1.get_rect(center=(largeur//2, hauteur//2))
    ecran.blit(texte1, rect1)
    
    texte2 = font.render("Clic gauche: révéler", True, (50, 50, 50))
    rect2 = texte2.get_rect(center=(largeur//2, hauteur//2 + 60))
    ecran.blit(texte2, rect2)
    
    texte3 = font.render("Clic droit: drapeau", True, (50, 50, 50))
    rect3 = texte3.get_rect(center=(largeur//2, hauteur//2 + 100))
    ecran.blit(texte3, rect3)

def dessiner_fin(ecran, largeur, hauteur, gagne):
    font = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    overlay = pygame.Surface((largeur, hauteur))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    ecran.blit(overlay, (0, 0))
    
    if gagne:
        texte = font.render("GAGNÉ !", True, (0, 255, 0))
    else:
        texte = font.render("PERDU !", True, (255, 0, 0))
    
    rect_texte = texte.get_rect(center=(largeur//2, hauteur//2 - 50))
    ecran.blit(texte, rect_texte)
    
    texte2 = font_small.render("Cliquez pour rejouer", True, (255, 255, 255))
    rect2 = texte2.get_rect(center=(largeur//2, hauteur//2 + 50))
    ecran.blit(texte2, rect2)

def main():
    lignes = 10
    colonnes = 10
    
    largeur = colonnes * TAILLE_CASE + 2 * MARGE
    hauteur = lignes * TAILLE_CASE + 2 * MARGE
    
    ecran = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Démineur")
    horloge = pygame.time.Clock()
    
    # États du jeu
    MENU = 0
    JEU = 1
    FIN = 2
    
    etat = MENU
    perdu = False
    gagne = False
    drapeaux = set()
    bombes = None
    premier_clic_fait = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if etat == MENU:
                    # Initialiser une nouvelle partie (sans générer les bombes)
                    bombes = None
                    affichage = np.full((lignes, colonnes), -2, dtype=int)
                    perdu = False
                    gagne = False
                    drapeaux = set()
                    premier_clic_fait = False
                    etat = JEU
                
                elif etat == JEU:
                    x, y = event.pos
                    j = (x - MARGE) // TAILLE_CASE
                    i = (y - MARGE) // TAILLE_CASE
                    
                    if 0 <= i < lignes and 0 <= j < colonnes:
                        if event.button == 1:  # Clic gauche
                            # Générer les bombes au premier clic
                            if not premier_clic_fait:
                                bombes = bombe(lignes, colonnes, (i, j))
                                premier_clic_fait = True
                            
                            if (i, j) not in drapeaux and affichage[i][j] == -2:
                                valeur = compter(bombes, i, j)
                                if valeur == -1:
                                    affichage[i][j] = -1
                                    perdu = True
                                    etat = FIN
                                else:
                                    afficher_case(affichage, bombes, i, j, drapeaux)
                                    
                                    # Vérifier si gagné
                                    cases_cachees = np.sum(affichage == -2)
                                    bombes_total = np.sum(bombes == -1)
                                    if cases_cachees == bombes_total - len(drapeaux):
                                        gagne = True
                                        etat = FIN
                        
                        elif event.button == 3:  # Clic droit
                            if affichage[i][j] == -2:
                                if (i, j) in drapeaux:
                                    drapeaux.remove((i, j))
                                else:
                                    drapeaux.add((i, j))
                
                elif etat == FIN:
                    etat = MENU
        
        # Dessiner
        ecran.fill(COULEUR_FOND)
        
        if etat == MENU:
            dessiner_menu(ecran, largeur, hauteur)
        elif etat == JEU:
            if bombes is not None:
                dessiner_grille(ecran, affichage, bombes, lignes, colonnes, False, drapeaux)
            else:
                # Afficher la grille vide avant le premier clic
                dessiner_grille(ecran, affichage, np.zeros((lignes, colonnes), dtype=int), lignes, colonnes, False, drapeaux)
        elif etat == FIN:
            dessiner_grille(ecran, affichage, bombes, lignes, colonnes, perdu, drapeaux)
            dessiner_fin(ecran, largeur, hauteur, gagne)
        
        pygame.display.flip()
        horloge.tick(30)

if __name__ == "__main__":
    main()