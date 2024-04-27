from pygame import *

init()
font.init()  # підключаємо шрифти
mixer.init()  # підключаємо музику
run = True
TILE_SIZE = 40
MAP_WIDTH = 38
MAP_HEIGHT = 19
WIDTH, HEIGHT = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE   
FPS = 60
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Лабіринт")
clock = time.Clock()
player_image = image.load("images/troll_male.png")
monster_image = image.load("images/sphinx_new.png")
ground_image = image.load("images/map/tomb_3_old.png")
wall_image = image.load("images/map/stone_brick_9.png")
poison_image = image.load("images/map/brilliant_blue_new.png")

sprites = sprite.Group()


class Sprite(sprite.Sprite):  # створюємо батьківський клас
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed=0) -> None:
        super().__init__()
        self.image = transform.scale(
            sprite_image, (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = sprite_speed
        self.mask = mask.from_surface(self.image)
        sprites.add(self)

    def draw(self, window):
        window.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed):
        super().__init__(sprite_image, x, y, sprite_width, sprite_height, sprite_speed)
        self.hp = 100
        self.coins = 0
        
    def update(self): # створюємо функцію яка дозволяє рухатись кораблю
        keyes = key.get_pressed() # створюємо змінну з натисканням кнопки
        if keyes[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keyes[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keyes[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keyes[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed


wall_group = sprite.Group()
player = Player(player_image,50,50,TILE_SIZE,TILE_SIZE,5)
with open("map.txt","r") as file:
    x,y = TILE_SIZE/2,TILE_SIZE/2
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == "w":
                wall_group.add(Sprite(wall_image, x, y,TILE_SIZE,TILE_SIZE))
            if symbol == "p":
                player.rect.x = x
                player.rect.y = y

            if symbol == "z":
                Sprite(poison_image, x, y,TILE_SIZE - 10,TILE_SIZE - 10)


            
            x += TILE_SIZE
        y +=   TILE_SIZE  
        x = TILE_SIZE/2

while run:
    window.fill((0,0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
    sprites.draw(window)
    sprites.update()
    display.update()
    clock.tick(FPS)
