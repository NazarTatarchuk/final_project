import random
import pygame
from pygame import sprite, image, transform

pygame.init()

WIDTH, HEIGHT = 1620, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

img_back = "background.png"
img_hero = "volk.png"
img_gryvnas = {
    1: '1_hryvna.png',
    10: '10_hryvnias.jpg',
    20: '20_hryvas.jpg',
    50: '50_hryvnas.png',
    100: '100_hryvnas.jpg',
    200: '200.png',
    500: '500_hryvnas.png'
}

music_bg = 'svetofor.ogg'
miss_sound = 'krik-volka.ogg'
catch_sound = 'pogodi.ogg'

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вовк ловить гривні")

pygame.mixer.music.load(music_bg)
pygame.mixer.music.play(-1)
miss_sfx = pygame.mixer.Sound(miss_sound)
catch_sfx = pygame.mixer.Sound(catch_sound)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Wolf(GameSprite):
    def __init__(self):
        super().__init__(img_hero, WIDTH // 2, HEIGHT - 240, 240, 240, 10)
        self.balance = 0

class Hryvnia(GameSprite):
    def __init__(self):
        self.value = random.choice(list(img_gryvnas.keys()))
        super().__init__(img_gryvnas[self.value], random.randint(0, WIDTH - 130), 0, 130, 130, 5)
    
    def fall(self):
        self.rect.y += self.speed
    
    def is_caught(self, wolf):
        return self.rect.colliderect(wolf.rect)

def game_loop():
    running = True
    clock = pygame.time.Clock()
    wolf = Wolf()
    hryvnias = []
    missed = 0
    max_missed = 20
    font = pygame.font.SysFont(None, 36)
    game_over_font = pygame.font.SysFont(None, 72)
    background = pygame.transform.scale(pygame.image.load(img_back), (WIDTH, HEIGHT))
    
    while running:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and wolf.rect.x > 0:
            wolf.rect.x -= wolf.speed
        if keys[pygame.K_RIGHT] and wolf.rect.x < WIDTH - wolf.rect.width:
            wolf.rect.x += wolf.speed
        
        if random.randint(1, 30) == 1:
            hryvnias.append(Hryvnia())
        
        for hryvnia in hryvnias[:]:
            hryvnia.fall()
            if hryvnia.is_caught(wolf):
                hryvnias.remove(hryvnia)
                wolf.balance += hryvnia.value
                catch_sfx.play()
            elif hryvnia.rect.y > HEIGHT:
                hryvnias.remove(hryvnia)
                missed += 1
                miss_sfx.play()
        
        wolf.reset()
        for hryvnia in hryvnias:
            hryvnia.reset()
        
        score_text = font.render(f"Баланс: {wolf.balance} грн", True, BLACK)
        missed_text = font.render(f"Пропущено: {missed}/{max_missed}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(missed_text, (10, 50))
        
        if missed >= max_missed:
            game_over_text = game_over_font.render("ГРА ЗАКІНЧЕНА", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    print(f"Ігра закінчена! Ваш баланс: {wolf.balance} грн")

if __name__ == "__main__":
    game_loop()
