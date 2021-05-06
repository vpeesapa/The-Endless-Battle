#!usr/bin/python3.6

import pygame
import math
import random
from colors import Colors
from controllers import ps4_controller,ps4_analog

# Class that contains the properties and functionalities of a bullet
class Bullet:

	# Parametrised constructor that initializes the bullet
	def __init__(self,color,point,radius,mouse_pos,velocity):
		self.color = color
		self.x,self.y = point
		self.radius = radius

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
	def __init__(self):
		self.x = 0
		self.y = 0

		self.randomize_position()

	# Function that randomizes the position of the enemy on the main display
	def randomize_position(self):
		while True:
			self.x = random.randint(0,window_width - 20)
			self.y = random.randint(0,window_height - 20)

			if not (window_center[0] - 15 <= self.x <= window_center[0] + 15 and window_center[1] - 15 <= self.y <= window_center[1] + 15):
				break

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
bullet_list = []
block_list = []

shooting = False
go_up = False
go_down = False
go_left = False
go_right = False
exit_game = False
mouse_read = True
use_ps4_controller = False
controller_button_map = {}
analog_axes = {}
player_velocity = 3
surface_pos = window_center
start = pygame.time.get_ticks()

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
def createEnemyBlock():
	while True:
		enemy = Enemy()
		r = pygame.Rect(enemy.x,enemy.y,20,20)

		if len(block_list) != 0:
			if r.collidelist(block_list) == -1:
				block_list.append(r)
				return
		else:
			block_list.append(r)

# while len(block_list) != 10:
# 	createEnemyBlock()

# Function that rotates the surface depending on the position of the mouse
def rotate(surface,mouse_pos):
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
	elif new_y - (surface_height / 2) <= 0:
		new_y = surface_height / 2

	return new_x,new_y

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
			bullet = Bullet(Colors["green"],new_surface_rect.center,7,mouse_pos,7)
			bullet_list.append(bullet)

	new_surface,new_surface_rect = rotate(player_surface,mouse_pos)

	# Check if the bullet is colliding with the enemy
	for bullet in bullet_list:
		for block in block_list:
			if enemyHit(bullet,block):
				if bullet in bullet_list:
					bullet_list.remove(bullet)

				block_list.remove(block)

	# If there are less than 10 enemies on the screen, create a new enemy
	# if len(block_list) == 0:
	# 	for i in range(1,random.randint(2,11)):
	# 		createEnemyBlock()

	# --Drawing all the components on the screen
	window.fill(Colors["black"])

	window.blit(new_surface,new_surface_rect.topleft)

	# The points of the triangle wrt the player surface
	points = ((surface_width / 2,0),(0,surface_height),(surface_width,surface_height))
	pygame.draw.polygon(player_surface,Colors["red"],points)

	for bullet in bullet_list:
		pygame.draw.circle(window,bullet.color,(bullet.x,bullet.y),bullet.radius)

	for block in block_list:
		pygame.draw.rect(window,Colors["blue"],block)

	# Updating the screen with whatever has been drawn so
	for bullet in bullet_list:
		bullet.update()

	pygame.display.update()

	# Limit the clock to 60 frames per second
	clock.tick(60)

# Stops the game engine after the user has exited the main gameplay loop
pygame.quit()