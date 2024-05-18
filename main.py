from pygame import *
from random import choice

init()
font.init()  # підключаємо шрифти
font1 = font.SysFont("Impact", 30)
font2 = font.SysFont("Impact", 100)
advise_font = font.SysFont("Arial", 20, True)
mixer.init()  # підключаємо музику
run = True
finish = False
TILE_SIZE = 40
MAP_WIDTH = 38
MAP_HEIGHT = 19
WIDTH, HEIGHT = MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE
FPS = 60
MAX_TIME = 30
SPEED_POISON_TIME = 4000
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Лабіринт")
clock = time.Clock()
player_image = image.load("images/troll_male.png")
monster_image = image.load("images/sphinx_new.png")
ground_image = transform.scale(image.load(
    "images/map/tomb_3_old.png"), (TILE_SIZE, TILE_SIZE))
wall_image = image.load("images/map/stone_brick_9.png")
poison_image = image.load("images/map/brilliant_blue_new.png")
coins_image = image.load("images\\map\\gold_pile_10.png")
doors_image = image.load("images/map/detected_secret_door.png")
map_image = image.load("images/map/scroll-grey.png")
speed_poison_image = image.load("images/map/ruby_old.png")

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
        self.hp = 50
        self.coins = 0
        self.maps = 0
        self.hit = False
        self.old_position = self.rect.x , self.rect.y
        self.speed_poison_time = None
        self.start_speed = sprite_speed
        self.poison_time_left  = 0

    def check_collision(self):
        global hp_label, coins_label, maps_label
        coins_collide = sprite.spritecollide(
            self, coins_group, True, sprite.collide_mask)
        if coins_collide:
            self.coins += 50
            coins_label = font1.render(f"Coins:{self.coins}", True, (0, 0, 0))

        maps_collide = sprite.spritecollide(
            self, maps_group, True, sprite.collide_mask)
        if maps_collide:
            self.maps += 1
            maps_label = font1.render(
                f"Maps:{self.maps}/{maps_ammount}", True, (0, 0, 0))

        check_collide = sprite.spritecollide(
            self, enemy_group, False, sprite.collide_mask)
        if check_collide and not self.hit:
            self.hit = True
            self.hp -= 50
            hp_label = font1.render(f"Hp:{self.hp}", True, (0, 0, 0))
            print(self.hp)

        if len(check_collide) == 0:
            self.hit = False

        poison_collide = sprite.spritecollide(
            self, poison_group, True, sprite.collide_mask)
        if poison_collide:
            self.hp += 50
            hp_label = font1.render(f"Hp:{self.hp}", True, (0, 0, 0))

        speed_poison_collide = sprite.spritecollide(
            self, speed_poison_group, True, sprite.collide_mask)
        if speed_poison_collide:
            self.speed += 2
            self.speed_poison_time = time.get_ticks()
        
    def update(self):  # створюємо функцію яка дозволяє рухатись кораблю
        keyes = key.get_pressed()  # створюємо змінну з натисканням кнопки
        self.old_position = self.rect.x, self.rect.y
        if keyes[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keyes[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keyes[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keyes[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if sprite.spritecollide(self, wall_group, False, sprite.collide_mask):
            self.rect.x, self.rect.y = self.old_position

        self.check_collision()
        if self.speed_poison_time:
            now = time.get_ticks()
            self.poison_time_left = (SPEED_POISON_TIME - (now -  self.speed_poison_time)) / 1000
            if now - self.speed_poison_time > SPEED_POISON_TIME:
                self.speed = self.start_speed
                self.speed_poison_time = None
            


enemy_group = sprite.Group()


class Enemy(Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed=3):
        super().__init__(sprite_image, x, y, sprite_width, sprite_height, sprite_speed)
        self.hp = 100
        self.directions = ["left", "right", "up", "down"]
        self.current_dir = choice(self.directions)
        self.left_image = self.image
        self.right_image = transform.flip(self.image, True, False)

    def update(self):
        old_position = self.rect.x, self.rect.y

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

        if sprite.spritecollide(self, wall_group, False) or sprite.spritecollide(self, doors_group, False) :
            self.current_dir = choice(self.directions)
            self.rect.x, self.rect.y = old_position


wall_group = sprite.Group()
player = Player(player_image, 50, 50, TILE_SIZE, TILE_SIZE, 5)

coins_group = sprite.Group()  # група спрайтів
doors_group = sprite.Group()
maps_group = sprite.Group()
poison_group = sprite.Group()
speed_poison_group = sprite.Group()

def load_map(level=1):
    global maps_ammount,maps_label,start_time,timer_label,timer
    for s in sprites:
        if s != player:
            s.kill()
    with open(f"map{level}.txt", "r") as file:
        x, y = TILE_SIZE/2, TILE_SIZE/2
        map = file.readlines()
        for line in map:
            for symbol in line:

                if symbol == "w":
                    wall_group.add(Sprite(wall_image, x, y, TILE_SIZE, TILE_SIZE))
                if symbol == "p":
                    player.rect.centerx = x
                    player.rect.centery = y

                if symbol == "z":
                    poison_group.add(
                        Sprite(poison_image, x, y, TILE_SIZE - 10, TILE_SIZE - 10))
                if symbol == "e":
                    enemy_group.add(Enemy(monster_image, x, y,
                                    TILE_SIZE - 10, TILE_SIZE - 10))
                if symbol == "c":
                    coins_group.add(
                        Sprite(coins_image, x, y, TILE_SIZE - 10, TILE_SIZE - 10))

                if symbol == "d":
                    doors_group.add(
                        Sprite(doors_image, x, y, TILE_SIZE, TILE_SIZE))

                if symbol == "s":
                    maps_group.add(
                        Sprite(map_image, x, y, TILE_SIZE - 10, TILE_SIZE - 10))
                    
                if symbol == "r":
                    speed_poison_group.add(Sprite(speed_poison_image, x, y, TILE_SIZE - 10, TILE_SIZE - 10))

                x += TILE_SIZE
            y += TILE_SIZE
            x = TILE_SIZE/2
        maps_ammount = len(maps_group)
        player.maps = 0
        maps_label = font1.render(f"Maps:0/{maps_ammount}", True, (0, 0, 0))
        start_time = time.get_ticks()
        timer_label = font1.render(f"Time left:{MAX_TIME}",True,(71, 8, 5))
        timer = MAX_TIME


level = 1
load_map(level)

coins_label = font1.render(f"Coins:0", True, (0, 0, 0))

hp_label = font1.render(f"Hp:{player.hp}", True, (0, 0, 0))

finish_label = font2.render("Game over!", True, (255, 0, 0))
advise_label = advise_font.render("You need to collect all maps!!!", True,(255,255,255))
poison_timer_label = font1.render(f"", True, (0, 0, 0))

while run:

    window.fill((0, 0, 0))
    
    
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            window.blit(ground_image, (x, y))
        y = 0
    sprites.draw(window)
    player.draw(window)
    window.blit(timer_label,(5,5))
    window.blit(hp_label, (300, 5))
    window.blit(coins_label, (WIDTH - 150, 5))
    window.blit(maps_label, (WIDTH/2, 5))

    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        now = time.get_ticks()
        timer =  MAX_TIME - (now - start_time) / 1000
        timer_label = font1.render(f"Time left:{round(timer,1)}", True,(71, 8, 5))


        sprites.update()
        if player.hp <= 0 or timer<= 0:
            finish = True
        doors_collide = sprite.spritecollide(player,doors_group,False,sprite.collide_mask )
        for door in doors_collide:
            if len(maps_group) == 0:
                level += 1
                if level == 3:
                    finish = True
                    finish_label = font2.render("You win!", True, (0, 255, 0))
                else:
                    load_map(level)


            
                
            else:
                if door.rect.x < player.rect.x:
                    window.blit(advise_label,(player.rect.right,player.rect.y))
                else:
                    window.blit(advise_label,(player.rect.left - advise_label.get_width(),player.rect.y))
                player.rect.x,player.rect.y = player.old_position
        if player.speed_poison_time:
            poison_timer_label = font1.render(f"Speed poison active: {round (player.poison_time_left,1)}", True, (166, 23, 17))
            window.blit(poison_timer_label,(WIDTH/2-poison_timer_label.get_width()/2, HEIGHT - poison_timer_label.get_height() ))


    
    if finish:
        window.blit(finish_label, (WIDTH/2-finish_label.get_width() /
                    2, HEIGHT/2 - finish_label.get_height()/2))
    display.update()
    clock.tick(FPS)
