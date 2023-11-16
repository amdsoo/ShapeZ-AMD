# Ariel Morandy - first try at python! Jan 2023
import declaration as d
from declaration import *
import pygame
import classes as c
import method as m
import userinterface as ui
import simulation as simu

# local variables
deltax = 0
deltay = 0

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ariel Platformer')

# basic font for Large Text
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# small font for user typed
my_font_S = pygame.font.SysFont('Comic Sans MS', 12)

draw_relationships = False

# show a long message
display_long_message = False
long_message = ""

# list to manage button activity
button_list = []

# create the main Objects
world  = c.World()
grid   = c.Grid()
game   = c.Game()
camera = c.Camera (world_width//2-screen_width//2,world_height//2-screen_height//2)

# main creation of buttons
ui.menu_create(button_list)

# handling of mouse drag
mouse_handler = ui.MouseHandler()

# simulation and delete are independant
button_delete = ui.Button("delete", 7 * tile_size, screen_height - tile_size)
button_simulation = ui.Button("simulation", 9 * tile_size, screen_height - tile_size)
button_save = ui.Button("save", 11 * tile_size, screen_height - tile_size)
button_open = ui.Button("open", 12 * tile_size, screen_height - tile_size)

# game loop
inwork_mode = False
tmp_object = None
tmp_object_angle = 0
placement_type = ""

# creation of a target at center of world.
col = world_width//(2*tile_size)
row =  world_height//(2*tile_size)
target = c.Target_x1 (camera, col,row, 0)
target.target_dna= m.generate_random_dna (1,2,2)
target.rect.x = col * tile_size - camera.offsetx
target.rect.y = row * tile_size - camera.offsety
d.all_sprites_machines_list.add(target)
d.machine_list.append(target)
# we add a representation of the cargo
cargo = eval("c." + target.delivery)(col, row, 0)
cargo.generate(target.target_dna)
# and place it at the correct location, using the cmaera offset.
cargo.offset(camera.offsetx, camera.offsety)
cargo.moveable = False

# we register the special cargo
game.target_cargo = cargo
d.all_sprites_cargos_list.add(cargo)

run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			print([str(type(machine)) for machine in d.machine_list])
			run = False

		# handling Mouse moves
		Mouse_x, Mouse_y = pygame.mouse.get_pos()
		'''mouse_handler.handle_events(event)

		if mouse_handler.start_pos!= mouse_handler.end_pos and mouse_handler.end_pos != None:
			x0,y0 =  mouse_handler.start_pos
			x1,y1 =  mouse_handler.end_pos
			dx = x0-x1
			dy = y0-y1
			print("dx =", dx, "dy=",dy)
			# Reset the mouse handler
			mouse_handler.reset()
			deltax = (dx//tile_size)*tile_size
			deltay = (dy//tile_size)*tile_size
			print("deltax =", deltax, "deltay =", deltay)'''

		if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
			deltax = - scroll_step
			if camera.offsetx + deltax < 0:
				deltax = 0
				'''camera.offsetx = 0'''
				print(" limit on X-")

		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			deltax = scroll_step
			if camera.offsetx + deltax > (world_width - screen_width):
				deltax = 0
				'''camera.offsetx = world_width - screen_width'''

		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
			deltay = - scroll_step
			if camera.offsety + deltay < 0:
				deltay = 0
				'''camera.offsety = 0'''
				print(" limit on Y-")

		if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
			deltay = scroll_step
			if camera.offsety + deltay > (world_height - screen_height):
				deltay = 0
				'''camera.offsety = world_height - screen_height'''


		camera.offsetx = camera.offsetx + deltax
		camera.offsety = camera.offsety + deltay

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
			print("Screen coord   = ", Mouse_x, Mouse_y)
			col, row = m.get_colrow_from_coordinates(Mouse_x + camera.offsetx, Mouse_y + camera.offsety)
			print("World   coord   = ", Mouse_x + camera.offsetx, Mouse_y + camera.offsety)
			print("Col/Row coord   = ",   col, row)

			placement_type = ""
			button_simulation.click()
			button_delete.click()
			button_save.click()
			button_open.click()

			# we show the properties in the lower right corner
			if tile_size < Mouse_y < (screen_height - tile_size):
				long_message = game.get_tile_info(col,row)
				print ("we show properties")
				display_long_message = True

			if button_delete.state == "pressed" or button_save.state == "pressed" or button_open.state == "pressed":
				placement_type = ""

			# check all the buttons from button list, if something is clicked, deactivate all
			placement_type = ui.menu_state_from_event(button_list)

			if placement_type != "":
				button_delete.state = "depressed"
				button_save.state = "depressed"
				button_open.state = "depressed"

		if button_save.state == "pressed":
			game.save_game (camera)
			button_save.state = "depressed"

		if button_open.state == "pressed":
			camera =game.open_game (camera)
			button_open.state = "depressed"

		if button_delete.state == "pressed":

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:

				# check whatselection under the mouse position.
				result = False
				col, row = m.get_colrow_from_coordinates(Mouse_x+camera.offsetx, Mouse_y+camera.offsety)

				# is it a machine?

				objecttodelete = m.find_machine(col, row)
				if objecttodelete is not None:
					d.machine_list.remove(objecttodelete)
					pygame.sprite.Sprite.kill(objecttodelete)
					result = False
				result = m.delete_rel(objecttodelete,  result)

				# is it a cargo?

				objecttodelete = m.find_cargo("Above", col, row)
				if objecttodelete is not None:
					d.cargo_list.remove(objecttodelete)
					pygame.sprite.Sprite.kill(objecttodelete)

				objecttodelete = m.find_cargo("Below", col, row)
				if objecttodelete is not None:
					d.cargo_list.remove(objecttodelete)
					pygame.sprite.Sprite.kill(objecttodelete)

		if placement_type != "":

			# a temporary object is created on left click if its button is active.
			if not inwork_mode:
				col, row = m.get_colrow_from_coordinates(Mouse_x+camera.offsetx, Mouse_y+camera.offsety)

				# creation of object based on category selected from the active button
				object_class = ui.menu_selection_frombutton(button_list)

				if object_class != "":
					tmp_object = eval("c." + object_class)(camera, col, row, tmp_object_angle)

				print("Object of class" + object_class + "is created in tmp", tmp_object)
				all_sprites_tmp.add(tmp_object)
				inwork_mode = True
				event.button = None

			# the temporary object moves with the mouse
			if inwork_mode:
				col, row = m.get_colrow_from_coordinates(Mouse_x+camera.offsetx, Mouse_y+camera.offsety)
				tmp_object.rect.x = col * tile_size - camera.offsetx
				tmp_object.rect.y = row * tile_size - camera.offsety


				gets_hit = None
				'''gets_hit = pygame.sprite.spritecollideany(tmp_object, all_sprites_machines_list, None)'''

				# manual method for detection.
				something_found = m.find_machine(col, row)
				if something_found is not None:
					'''print("collision ")'''
					gets_hit = True

				if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
					c.Machine.rotate(tmp_object)
					tmp_object_angle = tmp_object.angle

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and \
				    tile_size < Mouse_y < (screen_height - tile_size) and gets_hit is None:

					print ("we enter the creation of " , tmp_object)
					col, row = m.get_colrow_from_coordinates(Mouse_x+camera.offsetx, Mouse_y+camera.offsety)
					tmp_object.col = col
					tmp_object.row = row
					# in Screen coordinates
					tmp_object.rect.x = col * tile_size - camera.offsetx
					tmp_object.rect.y = row * tile_size - camera.offsety
					# in W coordinates
					tmp_object.x = col * tile_size
					tmp_object.y = row * tile_size

					d.machine_list.append(tmp_object)
					inwork_mode = False

					# we remove the sprite from the tmp group, then we add it to the main sprite group
					pygame.sprite.Sprite.kill(tmp_object)
					d.all_sprites_machines_list.add(tmp_object)

					# now we have a fixed position , we set connector locations
					tmp_object.set_connectors_coord()

					result = False
					result = m.create_rel(tmp_object, result)

		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			print("Escape button used")
			# delete the temporary object, remove the sprite
			if tmp_object is not None:
				pygame.sprite.Sprite.kill(tmp_object)
				tmp_object = None
			inwork_mode = False
			ui.menu_reset(button_list)
			button_delete.state = "depressed"
			button_save.state   = "depressed"
			button_open.state   = "depressed"
			placement_type      = ""

			# we clear the message box
			long_message = ""
			display_long_message = False

	# initialisation of world , with machines
	screen.fill(BLACK)
	world.draw(screen)
	grid.draw(screen,camera)
	game.draw(screen)

	if display_long_message:
		game.draw_msg(screen, long_message)

	for machine in d.machine_list:
		machine.offset(deltax, deltay)
		c.Machine.draw_connectors(machine, screen, camera)

	for button in button_list:
		button.draw(screen)

	for cargo in d.all_sprites_cargos_list:
		cargo.offset(deltax, deltay)

	d.all_sprites_cargos_list.update()
	d.all_sprites_machines_list.draw(screen)
	d.all_sprites_cargos_list.draw(screen)

	all_sprites_tmp.draw(screen)

	if draw_relationships:
		m.draw_rel(screen,camera)

	button_simulation.draw(screen)
	button_delete.draw(screen)
	button_save.draw(screen)
	button_open.draw(screen)

	if button_simulation.state == "pressed":
		if game.iteration_index == game.iteration:
			simu.gameupdate(game, camera)
			game.iteration_index = 0
		game.iteration_index = game.iteration_index + 1

	pygame.display.update()

	deltax = 0
	deltay = 0

pygame.quit()
