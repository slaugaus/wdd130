import pygame
import random
from entities import Star, Bullet, Enemy, EnemyBullet, Explosion, Pickup


def check_events(settings, screen, ship, gamepad, bullets, stats, sounds,
                 enemies, images, enemy_bullets, splash, hud):
    """Respond to key, gamepad, and mouse events."""
    if stats.game_active:
        check_repeat_keys(settings, screen, ship, bullets, stats, gamepad,
                          sounds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score(hud)
            stats.done = True
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, ship, stats, splash, hud)
            # Uncomment to enable debug keys!
            # check_debug_keys(event, settings, screen, enemies, images, stats,
            #                  hud)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, settings, ship)
        elif event.type == pygame.JOYAXISMOTION:
            check_analog_events(gamepad, ship, settings)
        elif event.type == pygame.JOYHATMOTION:
            check_hat_events(gamepad, ship, settings)
        elif event.type == pygame.JOYBUTTONDOWN:
            check_joydown_events(event, settings, ship, stats, splash, hud)
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == settings.but_X:
                ship.dodge_mode = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, splash, stats, mouse_x, mouse_y, hud)


def check_repeat_keys(settings, screen, ship, bullets, stats, gamepad, sounds):
    """Check for keys that will repeat an action when held."""
    keys = pygame.key.get_pressed()
    if ship.ready and not ship.dodge_mode:
        if settings.autofire and stats.bullet_cooldown == 0:
            fire_bullet(settings, screen, ship, bullets, sounds, stats)
            stats.bullet_cooldown = settings.bullet_cooldown
        if not settings.autofire:
            if ((keys[pygame.K_SPACE] or keys[pygame.K_z])
                    and stats.bullet_cooldown == 0):
                fire_bullet(settings, screen, ship, bullets, sounds, stats)
                stats.bullet_cooldown = settings.bullet_cooldown
            if settings.gamepad_connected:
                if (gamepad.get_button(settings.but_A) and
                        stats.bullet_cooldown == 0):
                    fire_bullet(settings, screen, ship, bullets, sounds, stats)
                    stats.bullet_cooldown = settings.bullet_cooldown
        # If autofire is on, hold a fire button to NOT fire.
        elif keys[pygame.K_SPACE] or keys[pygame.K_z]:
            stats.bullet_cooldown = settings.bullet_cooldown
        elif settings.gamepad_connected:
            if gamepad.get_button(settings.but_A):
                stats.bullet_cooldown = settings.bullet_cooldown
        if stats.bullet_cooldown > 0:
            stats.bullet_cooldown -= 1


def check_keydown_events(event, settings, ship, stats, splash, hud):
    """Respond to pressed keys."""
    # Note: Any wacky keypress limits are your keyboard's fault.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_x:
        ship.dodge_mode = True
    if event.key == pygame.K_a:
        settings.autofire = True if settings.autofire is False else False
    if event.key == pygame.K_ESCAPE:
        stats.game_active = True if stats.game_active is False else False
        if stats.game_active:
            pygame.mouse.set_visible(False)
            pygame.mixer.music.unpause()
            hud.prep_life_amount()
            hud.prep_score()
        else:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.pause()
            splash.prep_msg("Resume")


def check_debug_keys(event, settings, screen, enemies, images, stats, hud):
    if event.key == pygame.K_q:
        stats.save_high_score(hud)
        stats.done = True
    # There's definitely a better way to do this, but none of these will be in
    # the final product (by default) anyway
    if event.key == pygame.K_1:
        spawn_enemy(settings, screen, enemies, images, 1)
    if event.key == pygame.K_2:
        spawn_enemy(settings, screen, enemies, images, 2)
    if event.key == pygame.K_3:
        spawn_enemy(settings, screen, enemies, images, 3)
    if event.key == pygame.K_4:
        spawn_enemy(settings, screen, enemies, images, 4)
    if event.key == pygame.K_5:
        spawn_enemy(settings, screen, enemies, images, 5)
    if event.key == pygame.K_6:
        spawn_enemy(settings, screen, enemies, images, 6)
    if event.key == pygame.K_l:
        print("Level up!")
        stats.ship_level += 1


def check_keyup_events(event, settings, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_x:
        ship.dodge_mode = False


def check_analog_events(gamepad, ship, settings):
    """Respond to analog stick movement."""
    deadzone = settings.deadzone
    axis_x = settings.axis_x
    axis_y = settings.axis_y
    # If the stick is out of the deadzone, tell the ship to move.
    if gamepad.get_axis(axis_x) >= deadzone:
        ship.an_right = gamepad.get_axis(axis_x)
    if gamepad.get_axis(axis_x) <= -deadzone:
        ship.an_left = gamepad.get_axis(axis_x)
    if gamepad.get_axis(axis_y) >= deadzone:
        ship.an_down = gamepad.get_axis(axis_y)
    if gamepad.get_axis(axis_y) <= -deadzone:
        ship.an_up = gamepad.get_axis(axis_y)
    # If the stick is in the deadzone, make sure the ship doesn't move.
    if -deadzone <= gamepad.get_axis(axis_x) <= deadzone:
        ship.an_left, ship.an_right = 0, 0
    if -deadzone <= gamepad.get_axis(axis_y) <= deadzone:
        ship.an_up, ship.an_down = 0, 0


def check_hat_events(gamepad, ship, settings):
    """Respond to hat events."""
    hat = settings.hat_id
    motion = gamepad.get_hat(hat)
    if motion[0] == -1:
        ship.moving_left = True
    elif motion[0] == 1:
        ship.moving_right = True
    else:
        ship.moving_left, ship.moving_right = False, False
    if motion[1] == -1:
        ship.moving_down = True
    elif motion[1] == 1:
        ship.moving_up = True
    else:
        ship.moving_down, ship.moving_up = False, False


def check_joydown_events(event, settings, ship, stats, splash, hud):
    if event.button == settings.but_X:
        ship.dodge_mode = True
    if event.button == settings.but_Y:
        settings.autofire = True if settings.autofire is False else False
    elif event.button == settings.but_S:
        stats.game_active = True if stats.game_active is False else False
        if stats.game_active:
            pygame.mouse.set_visible(False)
            pygame.mixer.music.unpause()
            hud.prep_life_amount()
            hud.prep_score()
        else:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.pause()
            splash.prep_msg("Resume")


def check_play_button(settings, splash, stats, mouse_x, mouse_y, hud):
    clicked = splash.button_rect.collidepoint(mouse_x, mouse_y)
    if clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        pygame.mixer.music.unpause()
        stats.game_active = True
        # Necessary if the game is lost, but not harmful if it isn't.
        hud.prep_life_amount()
        hud.prep_score()


def update_stars(settings, screen, stars, images):
    """Update the starry background."""
    if len(stars) < settings.star_limit:
        new_star = Star(settings, screen, images)
        stars.add(new_star)
    stars.update()
    for star in stars.copy():
        if star.rect.right <= 0:
            stars.remove(star)


def spawn_enemy(settings, screen, enemies, images, id):
    """Spawn one enemy."""
    enemy = Enemy(settings, screen, images, id)
    enemy.x = settings.screen_width
    enemy.y = random.randint(0, settings.screen_height - enemy.rect.height)
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y
    enemies.add(enemy)


def spawn_enemies(settings, screen, enemies, images, id, stats):
    """Spawn enemies based on a timer, random numbers, and the game level."""
    stats.enemy_timer -= 1
    if stats.enemy_timer <= 0:
        id = random.randint(1, stats.game_level)
        spawn_enemy(settings, screen, enemies, images, id)
        stats.enemy_timer = stats.next_timer


def manage_game_level(settings, stats):
    """Manage the game level (highest spawnable enemy ID) based on score."""
    if stats.game_level < 6:
        # Hardcoded curve
        if stats.score >= 250:
            stats.game_level = 2
            stats.next_timer = 110
        if stats.score >= 750:
            stats.game_level = 3
            stats.next_timer = 90
        if stats.score >= 1250:
            stats.game_level = 4
            stats.next_timer = 80
        if stats.score >= 1750:
            stats.game_level = 5
            stats.next_timer = 70
        if stats.score >= 2500:
            stats.game_level = 6
            stats.next_timer = 60
            stats.next_score = 3500
    elif stats.score >= stats.next_score:
        # Decrement timer and scale the next score
        if stats.next_timer > settings.enemy_timer_min:
            stats.next_timer -= 10
        stats.next_score_increment *= 1.2
        stats.next_score += int(stats.next_score_increment)


def explode(settings, entity, screen, images, explosions, sounds, size="s"):
    """Spawn an explosion where an enemy (or the ship) dies."""
    if size == "s":
        sounds.boom_small.play()
        explosion = Explosion(settings, screen, images, entity.rect.center)
    elif size == "l":
        sounds.boom_med.play()
        explosion = Explosion(settings, screen, images, entity.rect.center,
                              "l")
    explosions.add(explosion)


def spawn_pickup(entity, settings, stats, screen, images, pickups, type=None,
                 scatter=False):
    """Spawn a pickup where something dies."""
    if type is None:
        if stats.ship_health < settings.ship_health:
            type = random.choice(["p", "h"])
        else:
            type = "p"
    if not scatter:
        center = entity.rect.center
    else:
        center = (entity.rect.center[0] + random.randint(-25, 25),
                  entity.rect.center[1] + random.randint(-25, 25))
    pickup = Pickup(images, screen, center, type)
    pickups.add(pickup)


def update_enemy_stuff(settings, screen, ship, enemies, sounds, stats,
                       explosions, images, pickups, hud, bullets,
                       enemy_bullets, splash):
    """Update the enemies and pickups."""
    enemies.update()
    pickups.update()
    for enemy in enemies.sprites():
        if enemy.health <= 0:
            stats.score += enemy.point_value
            hud.prep_score()
            stats.update_high_score(hud)
            if random.randint(1, 100) <= settings.pickup_chance:
                spawn_pickup(enemy, settings, stats, screen, images, pickups)
                if enemy.id == 2:
                    # Enemy 2 drops an extra pickup.
                    spawn_pickup(enemy, settings, stats, screen, images,
                                 pickups)
            if enemy.id is not 2:
                explode(settings, enemy, screen, images, explosions, sounds)
            else:
                explode(settings, enemy, screen, images, explosions, sounds,
                        "l")
            enemies.remove(enemy)
        if enemy.rect.right <= 0:
            enemies.remove(enemy)
        if pygame.sprite.collide_circle(ship, enemy) and not stats.ship_inv:
            enemy.health -= 1
            damage_ship(settings, stats, sounds, ship, hud, screen, images,
                        explosions, pickups, enemies, enemy_bullets, bullets,
                        splash)
    for pickup in pickups.sprites():
        if (pickup.rect.right <= 0 or
                pickup.rect.left >= settings.screen_width or
                pickup.rect.bottom <= 0 or
                pickup.rect.top >= settings.screen_height):
            pickups.remove(pickup)
    check_pickup_collisions(settings, screen, ship, pickups, stats, sounds, hud
                            )


def update_explosions(explosions):
    """Update the explosions."""
    explosions.update()
    for explosion in explosions.sprites():
        if explosion.countdown == 0:
            explosions.remove(explosion)


def fire_bullet(settings, screen, ship, bullets, sounds, stats):
    """Fire a pattern of bullets based on the ship's level."""
    if len(bullets) < settings.bullet_limit:
        if 0 <= stats.ship_level:
            bullet1 = Bullet(settings, screen, ship)
        if 2 <= stats.ship_level < 4:
            bullet1 = Bullet(settings, screen, ship, damage=2, height=4)
        if 4 <= stats.ship_level < 6:
            bullet1 = Bullet(settings, screen, ship, y_offset=6)
            bullet2 = Bullet(settings, screen, ship, y_offset=-6)
            bullets.add(bullet2)
        if 6 <= stats.ship_level < 8:
            bullet1 = Bullet(settings, screen, ship, y_offset=6)
            bullet2 = Bullet(settings, screen, ship, y_offset=-6)
            bullet3 = Bullet(settings, screen, ship, speed=21)
            bullets.add(bullet2, bullet3)
        if 8 <= stats.ship_level:
            bullet1 = Bullet(settings, screen, ship, y_offset=6)
            bullet2 = Bullet(settings, screen, ship, y_offset=-6)
            bullet3 = Bullet(settings, screen, ship, 0, 4, 15, 2, 21)
            bullets.add(bullet2, bullet3)
        bullets.add(bullet1)
        sounds.pew.play()


def fire_enemy_bullets(settings, screen, images, enemies, enemy_bullets,
                       sounds):
    """Fire bullets from each of the enemies that can."""
    for enemy in enemies:
        if enemy.fire_cooldown == 0:
            if enemy.id > 2:
                sounds.pew.play()
            if enemy.id == 3:
                angle = random.choice([190, 185, 175, 170])
                bullet = EnemyBullet(settings, screen, images,
                                     enemy.rect.center, angle, 25)
                enemy_bullets.add(bullet)
            if enemy.id >= 4:
                angle = enemy.index * 3
                bullet1 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle, 25)
                bullet2 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle+180, 25)
                enemy_bullets.add(bullet1, bullet2)
            if enemy.id == 5:
                bullet3 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle+90, 25)
                bullet4 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle-90, 25)
                enemy_bullets.add(bullet3, bullet4)
            if enemy.id == 6:
                bullet3 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle+60, 25)
                bullet4 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle+120, 25)
                bullet5 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle-60, 25)
                bullet6 = EnemyBullet(settings, screen, images,
                                      enemy.rect.center, angle-120, 25)
                enemy_bullets.add(bullet3, bullet4, bullet5, bullet6)
            enemy.fire_cooldown = (settings.enemy_fire_cooldown[enemy.id-1] +
                                   random.randint(-10, 10))
        elif enemy.fire_cooldown > 0:
            enemy.fire_cooldown -= 1


def update_bullets(settings, screen, ship, bullets, enemies, sounds,
                   enemy_bullets, images, stats, hud, explosions, pickups,
                   splash):
    """Update everything related to bullets."""
    fire_enemy_bullets(settings, screen, images, enemies, enemy_bullets,
                       sounds)
    # Update bullet positions.
    bullets.update()
    enemy_bullets.update()
    # Delete offscreen bullets.
    for bullet in bullets.copy():
        if bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)
    for bullet in enemy_bullets.copy():
        if (bullet.rect.left >= settings.screen_width or
                bullet.rect.right <= 0 or
                bullet.rect.top >= settings.screen_height or
                bullet.rect.bottom <= 0):
            enemy_bullets.remove(bullet)
    check_bullet_collisions(settings, screen, enemies, bullets, sounds, ship,
                            enemy_bullets, stats, hud, images, explosions,
                            pickups, splash)


def check_bullet_collisions(settings, screen, enemies, bullets, sounds, ship,
                            enemy_bullets, stats, hud, images, explosions,
                            pickups, splash):
    """Respond to bullet-enemy or bullet-ship collisions."""
    for enemy in enemies.sprites():
        if enemy.id is not 3:
            # Enemy 3 isn't a circle.
            collide = pygame.sprite.spritecollide(enemy, bullets, True,
                                                  pygame.sprite.collide_circle)
        else:
            collide = pygame.sprite.spritecollide(enemy, bullets, True)
        for bullet in collide:
            enemy.health -= bullet.damage
            sounds.enemy_hit.play()
    for bullet in enemy_bullets.sprites():
        if pygame.sprite.collide_circle(ship, bullet) and not stats.ship_inv:
            enemy_bullets.remove(bullet)
            damage_ship(settings, stats, sounds, ship, hud, screen, images,
                        explosions, pickups, enemies, enemy_bullets, bullets,
                        splash)


def check_pickup_collisions(settings, screen, ship, pickups, stats, sounds, hud
                            ):
    """Respond to ship-pickup collisions."""
    for pickup in pickups.sprites():
        if pygame.sprite.collide_rect(ship, pickup) and ship.ready:
            sounds.levelup.play()
            if pickup.type == "h" and stats.ship_health < settings.ship_health:
                stats.ship_health += 1
            elif stats.ship_level < settings.max_ship_level:
                # If you get health when you don't need it, you just level up.
                stats.ship_level += 1
            else:
                # If you need neither pickup, just increase the score.
                stats.score += 500
                hud.prep_score()
                stats.update_high_score(hud)
            pickups.remove(pickup)


def damage_ship(settings, stats, sounds, ship, hud, screen, images, explosions,
                pickups, enemies, enemy_bullets, bullets, splash):
    """Damage the ship."""
    if stats.ship_health > 1:
        stats.ship_health -= 1
        if stats.ship_level > 0:
            sounds.leveldown.play()
            stats.ship_level -= 1
        stats.ship_inv_timer = settings.ship_mercy_inv
        sounds.ship_hit.play()
    elif stats.ship_lives > 0:
        stats.ship_health -= 1
        stats.ship_lives -= 1
        hud.prep_life_amount()
        explode(settings, ship, screen, images, explosions, sounds)
        ship.reset_pos()
        while stats.ship_level > 0:
            stats.ship_level -= 1
            spawn_pickup(ship, settings, stats, screen, images, pickups, "p",
                         True)
    else:
        stats.ship_health -= 1
        explode(settings, ship, screen, images, explosions, sounds)
        ship.reset_pos()
        ship.update(settings, images)  # so the ship "disappears"
        for enemy in enemies:
            enemies.remove(enemy)
            explode(settings, enemy, screen, images, explosions, sounds)
        bullets.empty()
        enemy_bullets.empty()
        pickups.empty()
        splash.prep_msg("Restart")
        stats.game_active = False
        pygame.mixer.music.pause()
        pygame.mouse.set_visible(True)
        stats.reset_stats()


def update_screen(settings, screen, stars, ship, bullets, enemies, explosions,
                  pickups, hud, stats, enemy_bullets, splash):
    """Update and flip any images onscreen."""
    screen.fill(settings.black)
    for star in stars.sprites():
        star.blitme()
    hud.update(stats)
    for enemy in enemies.sprites():
        enemy.blitme()
    for explosion in explosions.sprites():
        explosion.blitme()
    for pickup in pickups.sprites():
        pickup.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for bullet in enemy_bullets.sprites():
        bullet.blitme()
    if not stats.game_active:
        splash.draw()
    pygame.display.flip()
