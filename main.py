from pygame import*
from random import randint
import time as pytime

mixer.init()
mixer.music.load('assets\\music\\svetofor')
mixer.music.play()
volk_voice = mixer.Sounds('assets\\music\\krik-volka')


font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN', True, (255,255,255))
lose = font1.render('YOU LOSE', True, (255,0,0))

img_back = "assets\\pictures\\background.png"  
img_hero = "assets\\pictures\\volk.png" 
img_gryvnas = 'assets\\pictures\\gryvnas.png'

clock = time.Clock()
FPS = 30

score = 0
goal = 50 
lost = 0

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        super().__init__()
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
