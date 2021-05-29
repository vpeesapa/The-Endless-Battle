#!usr/bin/python3.6

import pygame
import math
import random
from colors import Colors
from controllers import ps4_controller,ps4_analog

# Class that contains the properties and functionalities of a bullet
class Bullet:

	# Parametrised constructor that initializes the bullet
	def __init__(self,color,point,radius,mouse_pos,velocity,damage):
		self.color = color
		self.x,self.y = point
		self.radius = radius
		self.damage = damage

		mouse_x,mouse_y = mouse_pos

		rel_x = mouse_x - self.x
		rel_y = mouse_y - self.y
		angle = math.atan2(rel_y,rel_x)

		self.x_change = math.cos(angle) * velocity
		self.y_change = math.sin(angle) * velocity

	# Function that updates the position of the bullet per frame
	def update(self):
		self.x += self.x_change
		self.y += self.y_change

# Class that contains the properties and functionalities of the enemy
class Enemy:

	# Parametrised constructor that initializes the enemy
	def __init__(self,color):
		self.x = 0
		self.y = 0
		self.color = color
		self.surface = pygame.Surface(surface_size)
		self.new_surface = self.surface
		self.new_surface_rect = self.surface.get_rect()
		self.position = (0,0)

		self.health = 100

		self.bullet_list = []
		self.start_bullet_timer = pygame.time.get_ticks()

		self.keep_moving = True

		self.randomize_position()

	# Function that randomizes the position of the enemy on the main display
	def randomize_position(self):
		while True:
			self.x = random.randint(surface_width,window_width - surface_width)
			self.y = random.randint(25 + surface_height,window_height - surface_height)

			player_radius = surface_width / math.sqrt(2)

			x_clashing = surface_pos[0] - player_radius <= self.x <= surface_pos[0] + player_radius
			y_clashing = surface_pos[1] - player_radius <= self.y <= surface_pos[1] + player_radius

			if not (x_clashing and y_clashing):
				self.position = (self.x,self.y)
				break

# Class that defines the functionalities of the first type of enemy
class EnemyType1(Enemy):

	# Parametrised constructor that initializes the first kind of enemy
	def __init__(self,color):
		# Calls the constructor of the parent class
		super().__init__(color)

		self.type = 1
		self.points = ((surface_width / 2,0),(0,surface_height),(surface_width,surface_height))
		self.velocity = 0.5
		self.hitbox = pygame.Rect(5,0,20,30)
		# Bullets are fired at an interval of 0.3s
		self.bullet_frequency = 300

	# Function that updates the enemy's position
	def update(self):
		if self.keep_moving:
			dx = surface_pos[0] - self.x
			dy = surface_pos[1] - self.y

			angle = math.atan2(dy,dx)

			x_change = math.cos(angle) * self.velocity
			y_change = math.sin(angle) * self.velocity

			# Updating the position of the enemy accordingly
			self.x += x_change
			self.y += y_change

			# Checking if the enemy is going out-of-bounds
			if self.x - (surface_width / 2) <= 0:
				self.x = surface_width / 2
			elif self.x + (surface_width / 2) >= window_width:
				self.x = window_width - (surface_width / 2)

			if self.y - (surface_height / 2) <= 25:
				self.y = 25 + (surface_height / 2)
			elif self.y + (surface_height / 2) >= window_height:
				self.y = window_height - (surface_height / 2)

			self.position = (self.x,self.y)
			self.hitbox = pygame.Rect(self.x - 10,self.y - 15,20,30)

	# Function which makes the enemy fire a bullet
	def fireBullet(self):
		enemy_bullet = Bullet(Colors["silver"],self.new_surface_rect.center,5,surface_pos,2,20)
		self.bullet_list.append(enemy_bullet)

	# Function that draws the enemy onto the screen
	def drawEnemy(self):
		window.blit(self.new_surface,self.new_surface_rect.topleft)
		pygame.draw.polygon(self.surface,self.color,self.points)

# Class the defines the functionalities of the second type of enemy
class EnemyType2(Enemy):

	# Parametrised constructor that initializes the second kind of enemy
	def __init__(self,color):
		# Calls the constructor of the parent class
		super().__init__(color)

		self.type = 2
		self.points = (surface_width / 2,surface_height / 2)
		self.hitbox = pygame.Rect(self.position[0] - 15,self.position[1] - 15,30,30)
		self.radius = 15
		self.new_surface_rect = self.surface.get_rect(center = self.position)
		self.angle = 0
		# Bullets are fired at an interval of 0.3s
		self.bullet_frequency = 300

	# Function that updates the enemy's rotation angle
	def update(self):
		self.angle = (self.angle + 1) % 360
		self.new_surface = pygame.transform.rotate(self.surface,self.angle)
		self.new_surface_rect = self.new_surface.get_rect(center = self.position)

	# Function which makes the enemy fire bullets
	def fireBullet(self):
		bullet_color = random.choice([Colors["silver"],Colors["magenta"]])
		bullet_dest_1 = ((math.cos(math.radians(self.angle)) * 15 + self.x),(math.sin(math.radians(self.angle)) * 15 + self.y))
		enemy_bullet_1 = Bullet(bullet_color,self.new_surface_rect.center,5,bullet_dest_1,2,20)
		self.bullet_list.append(enemy_bullet_1)
		bullet_dest_2 = (((-1) * math.cos(math.radians(self.angle)) * 15 + self.x),((-1) * math.sin(math.radians(self.angle)) * 15 + self.y))
		enemy_bullet_2 = Bullet(bullet_color,self.new_surface_rect.center,5,bullet_dest_2,2,20)
		self.bullet_list.append(enemy_bullet_2)
		bullet_dest_3 = ((math.cos(math.radians(self.angle - 90)) * 15 + self.x),(math.sin(math.radians(self.angle - 90)) * 15 + self.y))
		enemy_bullet_3 = Bullet(bullet_color,self.new_surface_rect.center,5,bullet_dest_3,2,20)
		self.bullet_list.append(enemy_bullet_3)
		bullet_dest_4 = (((-1) * math.cos(math.radians(self.angle - 90)) * 15 + self.x),((-1) * math.sin(math.radians(self.angle - 90)) * 15 + self.y))
		enemy_bullet_4 = Bullet(bullet_color,self.new_surface_rect.center,5,bullet_dest_4,2,20)
		self.bullet_list.append(enemy_bullet_4)

	# Function that draws the enemy onto the screen
	def drawEnemy(self):
		window.blit(self.new_surface,self.new_surface_rect.topleft)
		pygame.draw.circle(self.surface,self.color,self.points,self.radius)

# Class that defines the functionalities of the third type of enemy
class EnemyType3(Enemy):

	# Parametrised constructor that initializes the third type of enemy
	def __init__(self,color):
		# Calls the constructor of the parent class
		super().__init__(color)

		self.type = 3
		self.points = (surface_width / 2,surface_height / 2)
		self.hitbox = pygame.Rect(self.position[0] - 15,self.position[1] - 15,30,30)
		self.new_surface_rect = self.surface.get_rect(center = self.position)
		self.radius = 15
		# Bullets are fired at an interval of 0.5s
		self.bullet_frequency = 500

	# Function that updates the enemy (in this case does nothing)
	def update(self):
		return

	# Function which makes the enemy fire bullets
	def fireBullet(self):
		bullet_color = Colors["silver"]
		angles = [0,30,60,90,120,150,180,210,240,270,300,330]

		# Create bullets at every angle
		for angle in angles:
			bullet_dest = ((math.cos(math.radians(angle)) * 15 + self.x),(math.sin(math.radians(angle)) * 15 + self.y))
			enemy_bullet = Bullet(bullet_color,self.new_surface_rect.center,5,bullet_dest,2,20)
			self.bullet_list.append(enemy_bullet)

	# Function that draws the enemy onto the screen
	def drawEnemy(self):
		window.blit(self.new_surface,self.new_surface_rect.topleft)
		pygame.draw.circle(self.surface,self.color,self.points,self.radius)

# Initialize the game engine
pygame.init()

# Create a new window
window_width = 800
window_height = 600
window_size = (window_width,window_height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("The Endless Battle")

# Setting up a surface where the player will be blitted onto
surface_width = 30
surface_height = 30
surface_size = (surface_width,surface_height)
player_surface = pygame.Surface(surface_size)

# Stores the center of the main display
window_center = window.get_rect().center

# Set up the clock that controls the rate at which the window is updated
clock = pygame.time.Clock()

# --Global Variables--
# Empty Lists
bullet_list = []
enemy_list = []
dead_list = []

# Empty Dictionaries
controller_button_map = {}
analog_axes = {}

# Booleans
shooting = False
go_up = False
go_down = False
go_left = False
go_right = False
exit_game = False
mouse_read = True
first_hit = True
use_ps4_controller = False

# Miscellaneous
player_velocity = 3
surface_pos = window_center
player_hitbox = pygame.Rect(5,0,20,30)
player_health = 100
start_enemy_spawner = pygame.time.get_ticks()
start = pygame.time.get_ticks()
hits_taken = 0
player_color = Colors["green"]
# Player doesn't take damage for 5s after being damaged
player_recovery_time = 5000
start_player_recovery = pygame.time.get_ticks()
player_score = 0
font = pygame.font.Font(None,30)
# After taking damage, the player will keep blinking for 5s
start_blinker_timer = pygame.time.get_ticks()

# Tuples that indicate the direction in which the player moves
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

# Initialize the controller
joysticks = []
for i in range(pygame.joystick.get_count()):
	joystick = pygame.joystick.Joystick(i)
	joysticks.append(joystick)
	joystick.init()

for joystick in joysticks:
	controller_name = joystick.get_name()
	if controller_name == "Wireless Controller" or controller_name == "Sony Interactive Entertainment Wireless Controller":
		# If a PS4 controller is connected with the gane
		use_ps4_controller = True

if use_ps4_controller:
	controller_button_map = ps4_controller.copy()
	analog_axes = ps4_analog.copy()

# Function that creates the enemy block
# def createEnemyBlock():
# 	while True:
# 		enemy = Enemy()
# 		r = pygame.Rect(enemy.x,enemy.y,20,20)
#
# 		if len(block_list) != 0:
# 			if r.collidelist(block_list) == -1:
# 				block_list.append(r)
# 				return
# 		else:
# 			block_list.append(r)

# while len(block_list) != 10:
# 	createEnemyBlock()

# enemy = Enemy(Colors["blue"])
# enemy_list.append(enemy)

# Function that rotates the surface depending on the position of the mouse
def rotate(surface,mouse_pos,surface_pos):
	correction_angle = 90

	mouse_x,mouse_y = mouse_pos

	surface_rect = surface.get_rect(center = surface_pos)

	# Calculating the relative distances
	rel_x = mouse_x - surface_rect.centerx
	rel_y = mouse_y - surface_rect.centery

	# Calculating the angle of rotation (in degrees)
	angle = math.degrees(math.atan2(-rel_y,rel_x)) - correction_angle

	# Rotate the surface accordingly
	new_surface = pygame.transform.rotate(surface,angle)
	new_surface_rect = new_surface.get_rect(center = surface_rect.center)

	return new_surface,new_surface_rect

# Function that checks if the enemy has been hit by a bullet
def enemyHit(bullet,block):

	# If the center of the bullet collides with the enemy
	if block.collidepoint((bullet.x,bullet.y)):
		return True

	corners = [block.bottomleft,block.bottomright,block.topleft,block.topright]
	for corner in corners:
		corner_x,corner_y = corner

		# Calculating the relative distances in the x- and y-coordinates
		dx = corner_x - bullet.x
		dy = corner_y - bullet.y

		# Using the distance formula to calculate the distance between the rectangle's corners and the bullet's center
		distance = math.sqrt((dx * dx) + (dy * dy))

		if distance <= bullet.radius:
			return True

	return False

# Function that checks if the bullets from the player and enemies collide with each other
def bulletsHit(bullet,enemy_bullet):

	# Using the distance formula to calculate the relative distance between the centers of the two bullets
	dx = bullet.x - enemy_bullet.x
	dy = bullet.y - enemy_bullet.y

	distance = math.sqrt((dx * dx) + (dy * dy))

	if distance <= bullet.radius + enemy_bullet.radius:
		return True

	return False

# Function that moves the player accordingly
def movePlayer(direction):
	direction_x,direction_y = direction
	surface_x,surface_y = surface_pos

	new_x = surface_x + (direction_x * player_velocity)
	new_y = surface_y + (direction_y * player_velocity)

	# Checking if the player moves out of bounds
	if new_x + (surface_width / 2) >= window_width:
		new_x = window_width - (surface_width / 2)
	elif new_x - (surface_width / 2) <= 0:
		new_x = surface_width / 2

	if new_y + (surface_height / 2) >= window_height:
		new_y = window_height - (surface_height / 2)
	elif new_y - (surface_height / 2) <= 25:
		new_y = 25 + (surface_height / 2)

	return new_x,new_y

# Function that draws the player
def drawPlayer(player_surface,new_surface,new_surface_rect,recovery_diff):
	global start_blinker_timer

	current_blinker_timer = pygame.time.get_ticks()

	window.blit(new_surface,new_surface_rect.topleft)

	# The points of the triangle wrt the player surface
	points = ((surface_width / 2,0),(0,surface_height),(surface_width,surface_height))

	if recovery_diff < player_recovery_time and not first_hit:
		# If the player takes damage, they recover for 5s, indicated by the constant back and forth flickering
		if current_blinker_timer - start_blinker_timer < 100:
			pygame.draw.polygon(player_surface,Colors["black"],points)
		else:
			pygame.draw.polygon(player_surface,player_color,points)
			start_blinker_timer = current_blinker_timer
	else:
		pygame.draw.polygon(player_surface,player_color,points)

# Function that ensures that the player does not overlap with the enemy
def enemiesCollide(enemy):
	global surface_pos

	enemy_x,enemy_y = enemy.position
	player_x,player_y = surface_pos

	player_diagonal = surface_width / math.sqrt(2)

	enemy_width = enemy.new_surface_rect.width
	enemy_height = enemy.new_surface_rect.height
	enemy_diagonal = math.sqrt((enemy_width * enemy_width) + (enemy_height * enemy_height))

	dx = player_x - enemy_x
	dy = player_y - enemy_y

	distance = math.sqrt((dx * dx) + (dy * dy))
	angle = math.atan2(dy,dx)

	if distance <= (player_diagonal / 2) + (enemy_diagonal / 2):
		player_x = math.cos(angle) * ((player_diagonal / 2) + (enemy_diagonal / 2)) + enemy_x
		player_y = math.sin(angle) * ((player_diagonal / 2) + (enemy_diagonal / 2)) + enemy_y
		enemy.keep_moving = False

	surface_pos = player_x,player_y


# Main gameplay loop
while not exit_game:

	# --Main event loop--
	if mouse_read:
		mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		# If the user did something
		if event.type == pygame.QUIT:
			# The user voluntarily closed the window
			exit_game = True
		if event.type == pygame.KEYDOWN:
			# If a key is pressed
			if event.key == pygame.K_x:
				# If x is pressed the game closes
				exit_game = True
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				# If the up arrow key or 'w' is pressed
				go_up = True
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				# If the down arrow key or 's' is pressed
				go_down = True
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				# If the right arrow key or 'd' is pressed
				go_right = True
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				# If the left arrow key or 'a' is pressed
				go_left = True
		if event.type == pygame.KEYUP:
			# When a key is released
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				# If the up arrow key or 'w' is released
				go_up = False
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				# If the down arrow key or 's' is released
				go_down = False
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				# If the right arrow key or 'd' is released
				go_right = False
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				# If the left arrow key or 'a' is released
				go_left = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			shooting = True
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			shooting = False
		if event.type == pygame.MOUSEMOTION:
			mouse_read = True

		# Joystick events
		if event.type == pygame.JOYBUTTONDOWN:
			# If a button on the joystick is pressed
			if event.button == controller_button_map["x"]:
				exit_game = True
			if event.button == controller_button_map["r1"]:
				shooting = True
		if event.type == pygame.JOYBUTTONUP:
			if event.button == controller_button_map["r1"]:
				shooting = False
		if event.type == pygame.JOYHATMOTION:
			# If the directional buttons are pressed
			x,y = event.value

			if x == -1:
				go_left = True
			elif x == 1:
				go_right = True
			elif x == 0:
				go_left = False
				go_right = False

			if y == 1:
				go_up = True
			elif y == -1:
				go_down = True
			elif y == 0:
				go_up = False
				go_down = False
		if event.type == pygame.JOYAXISMOTION:
			# If the analog sticks are moved or trigger buttons are pressed
			analog_axes[event.axis] = event.value

			if abs(analog_axes[0]) > 0.4:
				# Reads horizontal values from the left analog stick
				if analog_axes[0] < -0.5:
					go_left = True
				else:
					go_left = False

				if analog_axes[0] > 0.5:
					go_right = True
				else:
					go_right = False

			if abs(analog_axes[1]) > 0.4:
				# Reads vertical values from the left analog stick
				if analog_axes[1] < -0.5:
					go_up = True
				else:
					go_up = False

				if analog_axes[1] > 0.5:
					go_down = True
				else:
					go_down = False

			if abs(analog_axes[3]) > 0.1 and abs(analog_axes[4]) > 0.1:
				# Reads horizontal and vertical values from the right analog stick
				mouse_read = False

				x,y = analog_axes[3],analog_axes[4]

				bullet_angle = math.atan2(y,x)
				mouse_radius = surface_width / math.sqrt(2)
				mouse_x = (math.cos(bullet_angle) * mouse_radius) + surface_pos[0]
				mouse_y = (math.sin(bullet_angle) * mouse_radius) + surface_pos[1]
				mouse_pos = mouse_x,mouse_y

	# --Game logic goes here--
	now = pygame.time.get_ticks()

	if go_up:
		surface_pos = movePlayer(up)
	if go_down:
		surface_pos = movePlayer(down)
	if go_right:
		surface_pos = movePlayer(right)
	if go_left:
		surface_pos = movePlayer(left)

	if shooting:
		if now - start >= 200:
			# Spawns a new bullet every 0.2 seconds
			start = now
			bullet = Bullet(Colors["silver"],new_surface_rect.center,7,mouse_pos,7,50)
			bullet_list.append(bullet)

	current_bullet_timer = pygame.time.get_ticks()
	for enemy in enemy_list:
		if current_bullet_timer - enemy.start_bullet_timer >= enemy.bullet_frequency:
			enemy.start_bullet_timer = current_bullet_timer
			enemy.fireBullet()

	new_surface,new_surface_rect = rotate(player_surface,mouse_pos,surface_pos)

	for enemy in enemy_list:
		if enemy.type == 1:
			enemy.new_surface,enemy.new_surface_rect = rotate(enemy.surface,surface_pos,enemy.position)

	# Check if the bullet is colliding with the enemy
	for bullet in bullet_list:
		for enemy in enemy_list:
			if enemyHit(bullet,enemy.hitbox):
				enemy.health -= bullet.damage

				if bullet in bullet_list:
					bullet_list.remove(bullet)

				if 0 < enemy.health < 100:
					enemy.color = Colors["cyan"]
				elif enemy.health <= 0:
					player_score += 1
					# If there are bullets fired by the enemy on the screen, they should not be destroyed even if the enemy is destroyed
					if len(enemy.bullet_list) != 0:
						dead_list.extend(enemy.bullet_list)

					enemy_list.remove(enemy)
					# Start timer to spawn new enemy after existing enemy is destroyed
					start_enemy_spawner = pygame.time.get_ticks()

	# Check if the bullets are colliding with each other
	for bullet in bullet_list:
		for enemy in enemy_list:
			for enemy_bullet in enemy.bullet_list:
				if bulletsHit(bullet,enemy_bullet) and enemy_bullet.color == Colors["silver"]:
					# Destroying both bullets if they collide with each other
					if bullet in bullet_list:
						bullet_list.remove(bullet)

					enemy.bullet_list.remove(enemy_bullet)

	for bullet in bullet_list:
		for dead_bullet in dead_list:
			if bulletsHit(bullet,dead_bullet) and dead_bullet.color == Colors["silver"]:
				if bullet in bullet_list:
					bullet_list.remove(bullet)

				dead_list.remove(dead_bullet)

	# Check if the player takes damage from enemy bullets
	current_recovery_time = pygame.time.get_ticks()
	for enemy in enemy_list:
		for enemy_bullet in enemy.bullet_list:
			if enemyHit(enemy_bullet,player_hitbox):
				if first_hit:
					first_hit = False
					start_player_recovery = current_recovery_time
					player_health -= enemy_bullet.damage
					enemy.bullet_list.remove(enemy_bullet)
				elif current_recovery_time - start_player_recovery >= player_recovery_time:
					start_player_recovery = current_recovery_time
					player_health -= enemy_bullet.damage
					enemy.bullet_list.remove(enemy_bullet)

				if 60 < player_health <= 80:
					player_color = Colors["yellowgreen"]
				elif 40 < player_health <= 60:
					player_color = Colors["yellow"]
				elif 20 < player_health <= 40:
					player_color = Colors["orange"]
				elif 0 < player_health <= 20:
					player_color = Colors["red"]
				else:
					exit_game = True

	current_recovery_time = pygame.time.get_ticks()
	for dead_bullet in dead_list:
		if enemyHit(dead_bullet,player_hitbox):
			if first_hit:
				first_hit = False
				start_player_recovery = current_recovery_time
				player_health -= dead_bullet.damage
				dead_list.remove(dead_bullet)
			elif current_recovery_time - start_player_recovery >= player_recovery_time:
				start_player_recovery = current_recovery_time
				player_health -= dead_bullet.damage
				dead_list.remove(dead_bullet)

			if 60 < player_health <= 80:
				player_color = Colors["yellowgreen"]
			elif 40 < player_health <= 60:
				player_color = Colors["yellow"]
			elif 20 < player_health <= 40:
				player_color = Colors["orange"]
			elif 0 < player_health <= 20:
				player_color = Colors["red"]
			else:
				exit_game = True

	# Checking if the bullets are going out-of-bounds
	for bullet in bullet_list:
		if bullet.x <= 0 or bullet.x >= window_width or bullet.y <= 25 or bullet.y >= window_height:
			bullet_list.remove(bullet)

	for dead_bullet in dead_list:
		if dead_bullet.x <= 0 or dead_bullet.x >= window_width or dead_bullet.y <= 25 or dead_bullet.y >= window_height:
			dead_list.remove(dead_bullet)

	for enemy in enemy_list:
		for enemy_bullet in enemy.bullet_list:
			if enemy_bullet.x <= 0 or enemy_bullet.x >= window_width or enemy_bullet.y <= 25 or enemy_bullet.y >= window_height:
				enemy.bullet_list.remove(enemy_bullet)

	# Check if the player is colliding with the enemy
	for enemy in enemy_list:
		if new_surface_rect.colliderect(enemy.new_surface_rect):
			enemiesCollide(enemy)
		else:
			enemy.keep_moving = True

	# If there are less than 10 enemies on the screen, create a new enemy
	current_enemy_spawner = pygame.time.get_ticks()
	if len(enemy_list) == 0:
		if current_enemy_spawner - start_enemy_spawner >= 1000:
			# Spawn an enemy only after 1 second
			start_enemy_spawner = current_enemy_spawner
			enemy_type = random.choice([1,2,3])
			if enemy_type == 1:
				enemy_list.append(EnemyType1(Colors["blue"]))
			elif enemy_type == 2:
				enemy_list.append(EnemyType2(Colors["blue"]))
			elif enemy_type == 3:
				enemy_list.append(EnemyType3(Colors["blue"]))

	# --Drawing all the components on the screen--
	window.fill(Colors["black"])

	# Drawing the enemy
	for enemy in enemy_list:
		enemy.drawEnemy()

	# Drawing the player and their bullets
	recovery_diff = current_recovery_time - start_player_recovery
	drawPlayer(player_surface,new_surface,new_surface_rect,recovery_diff)

	# Drawing the player's bullet
	for bullet in bullet_list:
		pygame.draw.circle(window,bullet.color,(bullet.x,bullet.y),bullet.radius)

	# Drawing the enemy's bullet
	for enemy in enemy_list:
		for enemy_bullet in enemy.bullet_list:
			pygame.draw.circle(window,enemy_bullet.color,(enemy_bullet.x,enemy_bullet.y),enemy_bullet.radius)

	for dead_bullet in dead_list:
		pygame.draw.circle(window,dead_bullet.color,(dead_bullet.x,dead_bullet.y),dead_bullet.radius)

	# Displaying the player's score and health at the top of the screen
	text = font.render("Score: " + str(player_score),1,Colors["white"])
	window.blit(text,(0,0))

	text = font.render("Health: " + str(player_health) + "%",1,player_color)
	window.blit(text,((window_width / 2) - 60,0))

	# Drawing a line that differentiates between the game and the HUD
	pygame.draw.line(window,Colors["white"],(0,25),(window_width,25))

	# --Updating the screen with whatever has been drawn so far--
	for bullet in bullet_list:
		bullet.update()

	# Updating the hitbox of the player
	player_hitbox = pygame.Rect(surface_pos[0] - 10,surface_pos[1] - 15,20,30)

	for enemy in enemy_list:
		for enemy_bullet in enemy.bullet_list:
			enemy_bullet.update()

	for dead_bullet in dead_list:
		dead_bullet.update()

	# Updating the enemies
	for enemy in enemy_list:
		enemy.update()

	pygame.display.update()

	# Limit the clock to 60 frames per second
	clock.tick(60)

# Stops the game engine after the user has exited the main gameplay loop
pygame.quit()