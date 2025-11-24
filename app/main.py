import pygame
from objects.screen import Window
from objects.cameleon import Cameleon

def main():
    pygame.init()
    pygame.font.init()

    window = Window()
    window.set_title()
    window.update_clock()

    cameleon = Cameleon(w_height=window.height,
                        w_width=window.width,
                        w_hud=window.hud_height,
                        n_blocks=10)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.screen.fill(window.background)

        cameleon.handle_input()
        cameleon.draw(window.screen)

        window.step()

if __name__ == "__main__":
    main()
