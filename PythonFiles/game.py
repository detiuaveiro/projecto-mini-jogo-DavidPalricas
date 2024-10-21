import pygame as pg
import pygame.sprite as pgs
import map as mp
import player as pl

def main():
    pg.init()

    # Set up the display
    window = pg.display.set_mode((600, 400))
    pg.display.set_caption("Super Bowser")
    
    all_sprites = pgs.Group()

    game_map = mp.Map()

    running = True

    player = pl.Player()

    all_sprites.add(player)

    all_sprites.draw(window)

    clock = pg.time.Clock()
    
    # Set up the game loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                player.move(event.key)
        
        window.fill((0, 0, 0))

        player.handling_fall()

        game_map.draw(window)

        all_sprites.update()
        all_sprites.draw(window)
       

        # Update the display
        pg.display.update()
        
        # 60 fps
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()