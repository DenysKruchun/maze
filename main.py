from pygame import *
from random import choice

init()
font.init()  # підключаємо шрифти
font1 = font.SysFont("Arial",30,True)

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
ground_image = transform.scale(image.load("images/map/tomb_3_old.png"), (TILE_SIZE, TILE_SIZE))
wall_image = image.load("images/map/stone_brick_9.png")
poison_image = image.load("images/map/brilliant_blue_new.png")
coins_image = image.load("images\map\gold_pile_10.png")

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
        self.hit = False

        
    def update(self): # створюємо функцію яка дозволяє рухатись кораблю
        global hp_label
        global coins_label
        keyes = key.get_pressed() # створюємо змінну з натисканням кнопки
        old_position = self.rect.x , self.rect.y
        if keyes[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keyes[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keyes[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keyes[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if sprite.spritecollide(self,wall_group,False,sprite.collide_mask):
            self.rect.x , self.rect.y = old_position

        check_collide = sprite.spritecollide(self,enemy_group,False,sprite.collide_mask)
        coins_collide = sprite.spritecollide(self,coins_group,True,sprite.collide_mask)
        if check_collide  and not self.hit:
            self.hit = True
            self.hp -= 50
            hp_label = font1.render(f"Hp:{player.hp}",True,(0,0,0))
            print(self.hp)
        
        if len(check_collide) == 0:
            self.hit = False
        
        if coins_collide:
            self.coins += 50 
            coins_label = font1.render(f"Coins:{self.coins}",True,(0,0,0))        


        
        

enemy_group = sprite.Group()
class Enemy(Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed=3):
        super().__init__(sprite_image, x, y, sprite_width, sprite_height, sprite_speed)
        self.hp = 100
        self.directions = ["left","right","up","down"]
        self.current_dir = choice(self.directions)
        self.left_image = self.image
        self.right_image = transform.flip(self.image,True,False)

    def update(self):
        old_position = self.rect.x , self.rect.y

        if self.current_dir == "left":
            self.rect.x -= self.speed
            self.image = self.left_image

        if self.current_dir == "right":
            self.rect.x += self.speed
            self.image = self.right_image


        if self.current_dir == "up":
            self.rect.y -= self.speed

        if self.current_dir == "down":
            self.rect.y += self.speed

        if sprite.spritecollide(self,wall_group,False):
            self.current_dir = choice(self.directions)
            self.rect.x , self.rect.y = old_position


wall_group = sprite.Group()
player = Player(player_image,50,50,TILE_SIZE,TILE_SIZE,5)
hp_label = font1.render(f"Hp:{player.hp}",True,(0,0,0))


coins_group = sprite.Group() # група спрайтів
coins_collide = sprite.spritecollide(player,coins_group,True,sprite.collide_mask)
coins_label = font1.render(f"Coins:0",True,(0,0,0)) 

if coins_collide:
    coins_label = font1.render(f"Coins:{player.coins}",True,(0,0,0))  


with open("map.txt","r") as file:
    x,y = TILE_SIZE/2,TILE_SIZE/2
    map = file.readlines()
    for line in map:
        for symbol in line:
           
            if symbol == "w":
                wall_group.add(Sprite(wall_image, x, y,TILE_SIZE,TILE_SIZE))
            if symbol == "p":
                player.rect.centerx = x
                player.rect.centery = y

            if symbol == "z":
                Sprite(poison_image, x, y,TILE_SIZE - 10,TILE_SIZE - 10)
            if symbol == "e":
                enemy_group.add(Enemy(monster_image, x, y,TILE_SIZE - 10,TILE_SIZE - 10))
            if symbol == "c":
                coins_group.add(Sprite(coins_image,x,y,TILE_SIZE - 10,TILE_SIZE - 10))

            
            x += TILE_SIZE
        y +=   TILE_SIZE  
        x = TILE_SIZE/2

while run:

    window.fill((0,0,0))
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT,TILE_SIZE):
            window.blit(ground_image,(x,y))
        y = 0
        
    
    for e in event.get():
        if e.type == QUIT:
            run = False
    sprites.draw(window)
    player.draw(window)
    window.blit(hp_label, (5,5))
    window.blit(coins_label,(WIDTH - 150,5))
    sprites.update()
    display.update()
    clock.tick(FPS)
