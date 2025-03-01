import random
import pygame
from pygame import sprite, image, transform

# Ініціалізація Pygame
pygame.init()

# Константи
WIDTH, HEIGHT = 1620, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шляхи до зображень і звуків
img_back = "background.png"
img_hero = "volk.png"
img_gryvnas = 'gryvnas.png'
img_gryvnas_1 = '1 hryvna.png'
img_gryvnas_10 = '10_hryvna.png'
img_gryvnas_20 = '10_hryvna.png'
img_gryvnas_50 = '10_hryvna.png'
img_gryvnas_100 = '10_hryvna.png'
img_gryvnas_200 = '10_hryvna.png'
img_gryvnas_500 = '10_hryvna.png'
music_bg = 'svetofor.ogg'
miss_sound = 'krik-volka.ogg'

# Створення вікна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вовк ловить гривні")

# Завантаження музики та звуків
pygame.mixer.music.load(music_bg)
pygame.mixer.music.play(-1)  # Фонова музика в циклі
miss_sfx = pygame.mixer.Sound(miss_sound)

# Базовий клас спрайтів
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

# Клас Вовка
class Wolf(GameSprite):
    def __init__(self):
        super().__init__(img_hero, WIDTH // 2, HEIGHT - 180, 180, 180, 10)

# Клас Гривні
class Hryvnia(GameSprite):
    def __init__(self):
        super().__init__(img_gryvnas, random.randint(0, WIDTH - 130), 0, 130, 130, 5)
    
    def fall(self):
        self.rect.y += self.speed
    
    def is_caught(self, wolf):
        return self.rect.colliderect(wolf.rect)

# Основний ігровий цикл
def game_loop():
    running = True
    clock = pygame.time.Clock()
    wolf = Wolf()
    hryvnias = []
    score = 0
    missed = 0
    max_missed = 5
    font = pygame.font.SysFont(None, 36)
    game_over_font = pygame.font.SysFont(None, 72)
    
    background = pygame.image.load(img_back)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
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
        
        if random.randint(1, 50) == 1:
            hryvnias.append(Hryvnia())
        
        for hryvnia in hryvnias[:]:
            hryvnia.fall()
            if hryvnia.is_caught(wolf):
                hryvnias.remove(hryvnia)
                score += 1
                catch_sfx.play()
            elif hryvnia.rect.y > HEIGHT:
                hryvnias.remove(hryvnia)
                missed += 1
                miss_sfx.play()
        
        wolf.reset()
        for hryvnia in hryvnias:
            hryvnia.reset()
        
        score_text = font.render(f"Рахунок: {score}", True, BLACK)
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
    print(f"Ігра закінчена! Ваш рахунок: {score}")

if __name__ == "__main__":
    game_loop()
