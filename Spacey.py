import pygame
import random
import numpy as np


class Background_scroll(pygame.sprite.Sprite):
    def __init__(self, background_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = background_image
        self.n_pixel_roll = 2 # Number of rows to roll from bottom to top
        self.update_speed = 2 # Roll ever n frames

        gameDisplay.blit(self.image, (0,0))

    def update(self):
        if frame_count % self.update_speed == 0:
            # Convert surface to numpy array
            imgarr = pygame.surfarray.array3d(self.image)
            # Roll the image array
            imgarr = np.roll(imgarr, self.n_pixel_roll, axis=1)
            # Convert numpy array back to pygame surface
            self.image  = pygame.pixelcopy.make_surface(imgarr)

        gameDisplay.blit(self.image, (0,0))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, xcoord, ycoord, scale=1.5, update_n=1):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.frame = 0
        self.frames = frames
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.x = xcoord
        self.y = ycoord
        self.scale = scale
        self.update_n = update_n
        self.update_counter = self.update_n


    def update(self):
        self.update_counter -= 1
        if self.frame >= len(self.frames) - 1:
            self.kill()
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(self.rect.size[0] * self.scale),
                                                         int(self.rect.size[1] * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.update_counter == 0:
            self.frame += 1
            self.update_counter = self.update_n

        gameDisplay.blit(self.image, self.rect)

    def update_moving(self, xspeedboss, yspeedboss):
        if self.frame >= len(self.frames) - 1:
            self.kill()
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(self.rect.size[0] * 1.5), int(self.rect.size[1] * 1.5)))
        self.rect = self.image.get_rect()
        self.x += xspeedboss
        self.y += yspeedboss
        self.rect.x = self.x
        self.rect.y = self.y
        self.frame += 1
        gameDisplay.blit(self.image, self.rect)


class Explosion2(pygame.sprite.Sprite):
    def __init__(self, frames, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.frame = 0
        self.frames = frames
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.x = xcoord
        self.y = ycoord
        self.expansion = 0.8
        self.update_counter = 3

    def update(self):
        self.update_counter -= 1
        if self.frame >= len(self.frames) - 1:
            self.kill()
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(self.rect.size[0] * self.expansion),
                                                         int(self.rect.size[1] * self.expansion)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.update_counter == 0:
            self.expansion += 0.045
            self.frame += 1
            self.update_counter = 4
        gameDisplay.blit(self.image, self.rect)


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = player_ship
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = (display_width - self.width) * 0.5
        self.y = display_height - self.height * 1.2
        self.speed = 0  # This variable changes with key presses
        self.endspeed = 1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Update variables of the game for next update
        self.x += self.speed
        if self.x > display_width - self.width:
            self.x = display_width - self.width  # boundaries for ship
        elif self.x < 0:
            self.x = 0  # boundaries for ship

        self.rect.x = self.x
        self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
        gameDisplay.blit(self.image, self.rect)

    def to_end_position(self, xcoord):
        statement = False
        self.speed = 0
        if self.x < xcoord - 1:
            self.x += self.endspeed
        elif self.x > xcoord + 1:
            self.x -= self.endspeed
        else:
            statement = True

        self.rect.x = self.x
        self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
        gameDisplay.blit(self.image, self.rect)

        return statement


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        meteor_choices = [meteor1, meteor2, meteor3, meteor4]
        self.image = meteor_choices[random.randrange(0, 3)]
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = random.randrange(0, display_width - self.width)
        self.y = -200
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 7

    def update(self):
        self.y += self.speed
        self.rect.x = self.x
        self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
        gameDisplay.blit(self.image, self.rect)


class Laser(pygame.sprite.Sprite):
    def __init__(self, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_blue
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = xcoord - 0.5 * self.width  # depends on ship location
        self.y = ycoord  # These will be set at spawn because it depends on ship location
        self.speed = -20
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.y += self.speed
        if self.y < 0 - self.height:
            self.kill()
        else:
            self.rect.x = self.x
            self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
            gameDisplay.blit(self.image, self.rect)


class EnemyGoon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        enemy_choices = [enemy1, enemy2, enemy3]
        self.image = enemy_choices[random.randrange(0, 2)]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(self.rect.size[0] / 1.5), int(self.rect.size[1] / 1.5)))
        self.rect = self.image.get_rect()  # after transforming need to acquire new rect
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = random.choice(np.linspace(0, display_width - self.width, 10))
        self.y = 100 + self.height
        self.mask = pygame.mask.from_surface(self.image)
        self.update_timer = fps * 2  # update every 60 frames
        self.x_speed = random.choice([-3, 3])

    def update(self):
        self.update_timer -= 1
        if self.update_timer == 0:
            self.fire()
            self.update_timer = fps * 2
        self.y = 100 * np.sin(timer / 500) + 100

        self.x += self.x_speed
        if self.x > display_width - self.width:
            self.x = display_width - self.width  # boundaries for enemy
            self.x_speed = -self.x_speed  # flip speed so that enemy moves into opposite direction
        elif self.x < 0:
            self.x = 0  # boundaries for ship
            self.x_speed = -self.x_speed  # flip speed so that enemy moves into opposite direction
        self.rect.x = self.x
        self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
        gameDisplay.blit(self.image, self.rect)

    def fire(self):
        enemy_lasers.add(EnemyLaser(self.x + 0.5 * self.width, self.y))
        pygame.mixer.Channel(2).play(enemy_laser_sound)


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_red
        self.image = pygame.transform.flip(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = xcoord - 0.5 * self.width  # depends on ship location
        self.y = ycoord  # These will be set at spawn because it depends on ship location
        self.speed = 7
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.y += self.speed
        if self.y > display_height:
            self.kill()
        else:
            self.rect.x = self.x
            self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
            gameDisplay.blit(self.image, self.rect)


class ChooseFont(object):
    def __init__(self, fonttype, fontsize, color):
        self.font = pygame.font.Font(fonttype, fontsize)
        self.color = color

    def message(self, text, xcoord, ycoord, centered=False):
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        if centered is True:
            text_rect.center = (xcoord, ycoord)
        elif centered is False:
            text_rect.x = xcoord
            text_rect.y = ycoord
        gameDisplay.blit(text_surface, text_rect)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = display_width * 0.5 - self.width * 0.5
        self.y = 50
        self.y_speed = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.laser_timer_max = fps * 2  # update every 120 frames
        self.laser_timer = fps * 2  # update every 120 frames
        self.laser_list = [5, 10, 15, 20, 25]
        self.bomb_timer_max = fps * 4
        self.bomb_timer = self.bomb_timer_max
        self.x_speed = 3
        self.hp = 100
        self.maxhp = self.hp
        self.dead_timer = 170
        self.add_explosion_timer = 10
        self.randx = None
        self.randy = None
        self.hp_50 = False
        self.hp_25 = False

    def update(self):
        if self.hp > 0:
            self.laser_timer -= 1
            self.bomb_timer -= 1
            if self.laser_timer in self.laser_list:  # frames at which ship fires
                self.fire_laser()
            if self.laser_timer == 0:
                self.laser_timer = self.laser_timer_max
            if self.bomb_timer == 0:
                self.bomb_timer = self.bomb_timer_max
                self.fire_bomb()

            if self.hp < self.maxhp * 0.5 and self.hp_50 is False:
                if self.x_speed > 0:
                    self.x_speed = 5
                elif self.x_speed < 0:
                    self.x_speed = -5
                self.laser_timer_max = fps * 1.7
                self.bomb_timer_max = fps * 3.5
                self.hp_50 = True

            if self.hp < self.maxhp * 0.25 and self.hp_25 is False:
                if self.x_speed > 0:
                    self.x_speed = 7
                elif self.x_speed < 0:
                    self.x_speed = -7
                self.laser_timer_max = fps * 1.5
                self.bomb_timer_max = fps * 3
                self.hp_25 = True

        elif self.dead_timer > 0:
            self.x_speed = 1
            self.add_explosion_timer -= 1
            self.dead_timer -= 1
            if self.add_explosion_timer == 0:
                self.add_explosions()

                self.add_explosion_timer = 10

            for explosion in explosions_boss:
                explosion.update_moving(self.x_speed, self.y_speed)

        self.x += self.x_speed
        if self.x > display_width - self.width:
            self.x = display_width - self.width  # boundaries for enemy
            self.x_speed = -self.x_speed  # flip speed so that enemy moves into opposite direction
        elif self.x < 0:
            self.x = 0  # boundaries for ship
            self.x_speed = -self.x_speed  # flip speed so that enemy moves into opposite direction
        self.rect.x = self.x
        self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
        gameDisplay.blit(self.image, self.rect)

        self.draw_health()

    def fire_laser(self):
        enemy_lasers.add(EnemyLaser(self.x + 0.35 * self.width, self.y + 0.8 * self.height))
        enemy_lasers.add(EnemyLaser(self.x + 0.65 * self.width, self.y + 0.8 * self.height))
        pygame.mixer.Channel(2).play(enemy_laser_sound)

    def fire_bomb(self):
        boss_bomb.add(BossBomb(self.x, self.y))
        pygame.mixer.Channel(4).play(bomb_release_sound)

    def draw_health(self):
        color = red
        width_hp = self.width * (self.hp / self.maxhp)
        healthbar = pygame.Rect((self.x, self.y - 10, width_hp, 10))
        pygame.draw.rect(gameDisplay, color, healthbar)

    def add_explosions(self):
        for i in range(2):
            self.randx = random.randint(np.round(self.x) + 10 - 32, np.round(self.x) + self.width - 10 - 32)
            self.randy = random.randint(np.round(self.y) + 10 - 64, np.round(self.y) + self.height - 10 - 64)
            explosions_boss.add(Explosion(explosion1, self.randx, self.randy))
        pygame.mixer.Channel(3).play(explosion_sound)


class BossBomb(pygame.sprite.Sprite):
    def __init__(self, xcoord, ycoord):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile
        self.image = pygame.transform.flip(self.image, 0, 1)
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.x = xcoord - 0.5 * self.width  # depends on ship location
        self.y = ycoord  # These will be set at spawn because it depends on ship location
        self.xspeed = 0
        self.xspeedincr = 0.3
        self.xspeedmax = 5
        self.yspeed = 3
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, xship, yship):
        if xship > self.x:
            if self.xspeed < self.xspeedmax:
                self.xspeed += self.xspeedincr
        elif xship < self.x:
            if self.xspeed > -self.xspeedmax:
                self.xspeed -= self.xspeedincr
        self.x += self.xspeed

        self.y += self.yspeed

        if self.y >= display_height - 200:
            self.kill()
            explosions.add(Explosion2(explosion2, self.x, self.y))
            pygame.mixer.Channel(5).play(bomb_explosion_sound)
        else:
            self.rect.x = self.x
            self.rect.y = self.y  # set the rect (not just blit) or collision won't work!
            gameDisplay.blit(self.image, self.rect)


def main_menu():
    button_width = start_button.get_rect().size[0]
    scheme_width = controlscheme.get_rect().size[0]
    button_x_center = (display_width - button_width) * 0.5
    scheme_x_center = (display_width - scheme_width) * 0.5

    # End game when this becomes true
    in_main_menu = True
    # Play the soundtrack
    pygame.mixer.Channel(0).play(game_music, loops=-1)

    # This is the game loop where all game logic happens
    while in_main_menu:

        # This checks all events that happen (which are located in pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if startbutton.collidepoint(pos):
                    pygame.mixer.Channel(1).play(button_sound)
                    global time_since_startbutton
                    time_since_startbutton = pygame.time.get_ticks()
                    game_loop()
                elif creditbutton.collidepoint(pos):
                    credit_loop()
                elif quitbutton.collidepoint(pos):
                    pygame.mixer.Channel(1).play(button_sound)
                    pygame.quit()
                    quit()

        # Update main menu
        gameDisplay.blit(background_img, (0, 0))
        startbutton = gameDisplay.blit(start_button, (button_x_center, display_height * 0.4))
        creditbutton = gameDisplay.blit(credit_button, (button_x_center, display_height * 0.5))
        quitbutton = gameDisplay.blit(quit_button, (button_x_center, display_height * 0.6))
        gameDisplay.blit(controlscheme, (scheme_x_center, display_height * 0.7))
        pygame.display.update()


def credit_loop():
    credits = True
    while credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    credits = False
        # Update
        gameDisplay.blit(credit_background, (0, 0))

        pygame.display.update()


def game_loop():

    # Instantiate background
    global background_img, frame_count
    frame_count = 0
    background = Background_scroll(background_img)

    # Instantiate Ship & Meteor and create a group for lasersprites
    global ship, ship_group, meteors, lasers, score_count, enemies, fps, timer, enemy_lasers, score_count
    global boss_bomb, explosions, explosions_boss
    ship_group = pygame.sprite.GroupSingle()
    boss_group = pygame.sprite.GroupSingle()
    boss_bomb = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    enemy_lasers = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    explosions_boss = pygame.sprite.Group()

    # Set variables and events needed for meteor shower
    add_meteor_event = pygame.USEREVENT + 1
    add_meteor_timer = 300  # add new meteor evert 300 ms
    ms_event = pygame.USEREVENT + 2
    ms_start = 60000  # ms after which meteor shower arrives
    ms_duration = 20000
    pygame.time.set_timer(add_meteor_event, add_meteor_timer)
    pygame.time.set_timer(ms_event, ms_start)
    ms_passed = False
    ms_announcement = False

    # Set variables needed to spawn enemies
    add_enemies_event = pygame.USEREVENT + 3
    add_enemies_timer = 5000  # add new enemies every 5000 ms
    pygame.time.set_timer(add_enemies_event, add_enemies_timer)
    num_enemies = 3
    enemies_meteors_spawning = True

    # Set variables for boss battle
    boss_battle = False
    won = False
    ship_centered = False
    boss_announcement = False

    # Instatiate other variables
    score_count = 0  # score
    meteors_dodged = 0
    enemies_killed = 0
    bosses_killed = 0
    fps = 60
    ship = Ship()
    ship_group.add(ship)  # Add ship once before playing loop starts

    # This is the game loop where all game logic happens
    playing = True
    while playing:
        timer = pygame.time.get_ticks() - time_since_startbutton  # ms that have passed since start

        if 30000 < timer <= 40000:
            num_enemies = 4
        elif 40000 < timer <= 50000:
            num_enemies = 5
        elif 50000 < timer <= 60000:
            num_enemies = 6

        # Check for global events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if not won:
                # Check for user-inputted event
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        ship.speed = -10
                    elif event.key == pygame.K_RIGHT:
                        ship.speed = 10
                    elif event.key == pygame.K_SPACE:
                        lasers.add(Laser(ship.x + 0.5*ship.width, ship.y))
                        pygame.mixer.Channel(1).play(laser_sound)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        ship.speed = 0

            if ship_centered is True:
                # Button to return to main menu after defeating boss
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        playing = False

            # Check for events that only happen within certain time range
            if event.type == ms_event and ms_passed is False:  # This only occurs once
                ms_announcement_timer = timer
                ms_announcement = True
                enemies_meteors_spawning = False

            if event.type == add_enemies_event and enemies_meteors_spawning:
                for i in range(num_enemies):
                    enemies.add(EnemyGoon())

            try:
                if timer - ms_announcement_timer < 2000 and ms_announcement is True:  # display message 2000 ms
                    continue
                elif ms_announcement is True:
                    ms_announcement = False  # This makes sure announcement doesn't return anymore
                    ms_start_timer = timer  # Timestamp start of meteor shower
            except UnboundLocalError:
                continue
            try:
                if timer - ms_start_timer < ms_duration and ms_passed is False:
                    if event.type == add_meteor_event:  # add a meteor every time event is in event queue
                        meteors.add(Meteor())
                elif ms_passed is False:
                    ms_passed = True  # This makes sure ms doesn't return after it passed event is queued again
                    boss_announcement_timer = timer
                    boss_announcement = True
            except UnboundLocalError:
                continue

            try:
                if timer - boss_announcement_timer < 2000 and boss_announcement is True:
                    continue
                elif boss_announcement is True:
                    boss_announcement = False
                    boss_battle = True
                    boss = Boss()
                    boss_group.add(boss)
            except UnboundLocalError:
                continue

        # Update display and sprites
        background.update()    
        ship.update()

        if len(meteors) < 1 and enemies_meteors_spawning:
            meteors.add(Meteor())
        for meteor in meteors:
            meteor.update()
            if meteor.y > display_height:
                meteor.kill()
                meteors_dodged += 1
                score_count += 10

        for laser in lasers:
            laser.update()

        for enemy in enemies:
            enemy.update()

        for laser in enemy_lasers:
            laser.update()

        if boss_battle is True:
            boss.update()
            for bomb in boss_bomb:
                bomb.update(ship.x + 0.5 * ship.width, ship.y + 0.5 * ship.height)

            boss_hit = pygame.sprite.groupcollide(lasers, boss_group, 1, 0, pygame.sprite.collide_mask)
            for sprite in boss_hit:
                if boss_hit[sprite]:
                    explosions_boss.add(Explosion(explosion1, sprite.x - 32, sprite.y - 64))  # 64 is w/l of explosion
                    pygame.mixer.Channel(3).play(explosion_sound)
                    boss.hp -= 1

            for explosion in explosions_boss:
                explosion.update_moving(boss.x_speed, boss.y_speed)

            if boss.dead_timer <= 0:
                explosions.add(Explosion(explosion3, boss.x - boss.width*0.5, boss.y - boss.height*0.5, 3, 5))
                del boss
                boss_battle = False
                won = True
                score_count += 1000
                bosses_killed += 1

        for explosion in explosions:
            explosion.update()

            if boss_battle is True:
                burned = pygame.sprite.groupcollide(ship_group, explosions, 0, 0, pygame.sprite.collide_mask)
                if burned:
                    explosions.add(Explosion(explosion3, ship.x - ship.width * 0.5, ship.y - ship.height * 0.5, 2, 5))
                    crashed_text.message('you died. BUT DO NOT PANIC!',
                                         display_width * 0.5, display_height * 0.5, centered=True)
                    pygame.display.update()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    waiting = False
                                    playing = False
                        for explosion in explosions:
                            explosion.update()
                        performance_text.message('Return to main menu by pressing Enter and try again.',
                                                 display_width * 0.5, 500, centered=True)
                        pygame.display.update()

        if boss_battle is False and won is True:
            if ship_centered is False:
                ship_centered = ship.to_end_position(display_width*0.5 - ship.width * 0.5)

        # Check for collisions after new display if updated
        crashed = pygame.sprite.groupcollide(ship_group, meteors, 0, 0, pygame.sprite.collide_mask)
        hit = pygame.sprite.groupcollide(enemy_lasers, ship_group, 1, 0, pygame.sprite.collide_mask)
        if crashed or hit:
            explosions.add(Explosion(explosion3, ship.x - ship.width * 0.5, ship.y - ship.height * 0.5, 2, 5))
            crashed_text.message('you died. BUT DO NOT PANIC!',
                                 display_width * 0.5, display_height * 0.5, centered=True)
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            waiting = False
                            playing = False

                for explosion in explosions:
                    explosion.update()
                performance_text.message('Return to main menu by pressing Enter and try again.',
                                         display_width * 0.5, 500, centered=True)
                pygame.display.update()

        # Kill sprites after collision
        pygame.sprite.groupcollide(lasers, meteors, 1, 0, pygame.sprite.collide_mask)
        pygame.sprite.groupcollide(enemy_lasers, meteors, 1, 0, pygame.sprite.collide_mask)

        enemy_hit = pygame.sprite.groupcollide(enemies, lasers, 1, 1, pygame.sprite.collide_mask)
        for sprite in enemy_hit:
            if enemy_hit[sprite]:
                explosions.add(Explosion(explosion1, sprite.x, sprite.y))
                pygame.mixer.Channel(3).play(explosion_sound)
                score_count += 100
                enemies_killed += 1

        # Lastly, show text
        performance_text.message('score: ' + str(score_count), 5, 0)
        performance_text.message('%i' % (timer/1000), display_width - 45, 0)

        if ms_announcement:
            shower_text.message('METEOR SHOWER INCOMING', display_width * 0.5, display_height * 0.5, centered=True)

        if boss_announcement:
            shower_text.message('FINAL BOSS INCOMING', display_width * 0.5, display_height * 0.5, centered=True)

        if ship_centered is True:
            performance_text.message('meteors dodged: %i' % meteors_dodged, display_width * 0.5, 360, centered=True)
            performance_text.message('enemies destroyed: %i:' % enemies_killed, display_width * 0.5, 380, centered=True)
            performance_text.message('bosses destroyed: %i' % bosses_killed, display_width * 0.5, 400, centered=True)
            endgame_score_text.message('Final score: %i' % score_count, display_width * 0.5, 430, centered=True)
            performance_text.message('press enter to return to main menu', display_width * 0.5, 500, centered=True)

        pygame.display.update()

        # Set FPS
        clock.tick(fps)

        #frame counter
        frame_count += 1



# Here we initialize pygame, set variables and start the actual game
pygame.init()
# pygame.mouse.set_cursor(*pygame.cursors.diamond)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)


# Define some colors
black = (0, 0, 0)  # (R,G,B)
red = (255, 0, 0)
green = (0, 255, 0)

# Setup a window for the game
display_width = 800
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('MyFirstGame')  # Window Title

# -- Load sprites from spritesheets
spritesheet_explosion1 = pygame.image.load('Textures/explosions.png')
explosion1 = []
x_all = [628, 628, 628, 628, 576, 566, 562, 562, 562, 562, 924, 858, 792, 726, 660, 594, 924, 858, 792, 726, 660, 594,
         924, 764]
y_all = [772, 706, 640, 574, 938, 872, 772, 706, 640, 574, 502, 496, 496, 496, 496, 496, 436, 430, 430, 430, 430, 430,
         370, 826]
height = 64
width = 64

for i in range(24):
    frame = str(i)
    if len(frame) is 1:
        frame = '0' + frame
    x = x_all[i]
    y = y_all[i]
    explosion1.append(spritesheet_explosion1.subsurface(pygame.Rect(x, y, width, height)))

explosion3 = []
x_all = [100, 100, 100, 100, 888, 790, 692, 594, 496, 398, 300, 202, 104, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 100]
y_all = [398, 300, 202, 104, 2, 2, 2, 2, 2, 2, 2, 2, 2, 884, 786, 688, 590, 492, 394, 296, 198, 100, 2, 496]
h = 96
w = 96

for i in range(24):
    frame = str(i)
    if len(frame) is 1:
        frame = '0' + frame
    x = x_all[i]
    y = y_all[i]

    explosion3.append(spritesheet_explosion1.subsurface(pygame.Rect(x, y, h, w)))

spritesheet_explosion2 = pygame.image.load('Textures/particlefx_06.png')
height_exp = 128
width_exp = 128
explosion2 = []
for i in range(8):
    for j in range(8):
        explosion2.append(spritesheet_explosion2.subsurface(pygame.Rect(
            i*height_exp, j*width_exp, height_exp, width_exp)))

spritesheetspace = pygame.image.load('Textures/spritesheet_space.png')
start_button = spritesheetspace.subsurface(pygame.Rect(0, 117, 222, 39))
credit_button = spritesheetspace.subsurface(pygame.Rect(0, 78, 222, 39))
quit_button = spritesheetspace.subsurface(pygame.Rect(0, 0, 222, 39))
enemy1 = spritesheetspace.subsurface(pygame.Rect(423, 728, 93, 84))
enemy2 = spritesheetspace.subsurface(pygame.Rect(120, 604, 104, 84))
enemy3 = spritesheetspace.subsurface(pygame.Rect(144, 156, 103, 84))
laser_blue = spritesheetspace.subsurface(pygame.Rect(856, 421, 9, 54))
laser_red = spritesheetspace.subsurface(pygame.Rect(858, 230, 9, 54))
meteor1 = spritesheetspace.subsurface(pygame.Rect(224, 664, 101, 84))
meteor2 = spritesheetspace.subsurface(pygame.Rect(0, 520, 120, 98))
meteor3 = spritesheetspace.subsurface(pygame.Rect(518, 810, 89, 82))
meteor4 = spritesheetspace.subsurface(pygame.Rect(327, 452, 98, 96))
player_ship = spritesheetspace.subsurface(pygame.Rect(224, 832, 99, 75))
spritesheetspace2 = pygame.image.load('Textures/spritesheet_space2.png')
missile = spritesheetspace2.subsurface(pygame.Rect(1093, 711, 19, 40))
boss_image = spritesheetspace2.subsurface(pygame.Rect(276, 0, 172, 151))
controlscheme = pygame.image.load('Textures/controlscheme.png')
background_img = pygame.image.load('Textures/space_background.png').convert()
credit_background = pygame.image.load('Textures/credits.png').convert()

# Load files used in the game
game_music = pygame.mixer.Sound('Sounds/desert-travel.ogg')  # Channel 0
game_music.set_volume(0.5)
button_sound = pygame.mixer.Sound('Sounds/click_menu_sound.wav')  # Channel 1
laser_sound = pygame.mixer.Sound('Sounds/laser5.wav')  # Channel 1
enemy_laser_sound = pygame.mixer.Sound('Sounds/laser8.wav')  # Channel 2
enemy_laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound('Sounds/explodemini.wav')  # Channel 3
bomb_release_sound = pygame.mixer.Sound('Sounds/weaponfire4.wav')  # Channel 4
bomb_explosion_sound = pygame.mixer.Sound('Sounds/explosion2.wav')  # Channel 5

# Load fonts to use in the game
performance_text = ChooseFont('Fonts/xirod.ttf', 15, green)
endgame_score_text = ChooseFont('Fonts/xirod.ttf', 30, green)
crashed_text = ChooseFont('Fonts/xirod.ttf', 30, red)
shower_text = ChooseFont('Fonts/xirod.ttf', 30, red)

# Define game clock to time things
clock = pygame.time.Clock()

main_menu()
