
from declaration import *
'''import declaration as d'''

pygame.font.init()
# basic font for user typed
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_small_font = pygame.font.SysFont('Comic Sans MS', 15)

button_width = tile_size*0.8
button_height =tile_size*0.8


class MouseHandler:
    def __init__(self):
        self.right_click = False
        self.start_pos = None
        self.end_pos = None

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.right_click = False
                self.end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.right_click = True
                self.start_pos = event.pos

    def reset(self):
        self.right_click = False
        self.start_pos = None
        self.end_pos = None


class Button:
    def __init__(self, button_class, x, y):
        self.button_class = button_class
        self.color = LIGHTSHADE
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = "depressed"
        self.parent = "parent"

        # default image
        self.image = pygame.transform.scale(tmp_img, (self.width, self.height))

        if self.button_class == "Conveyor":
            self.image = pygame.transform.scale(cv_img , (self.width, self.height))
            self.image_ns = pygame.transform.scale(cv_ns_img , (self.width, self.height))
        if self.button_class == "Elbow_right":
            self.image = pygame.transform.scale(elb_right_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(elb_right_ns_img, (self.width, self.height))
        if self.button_class == "Elbow_left":
            self.image = pygame.transform.scale(elb_left_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(elb_left_ns_img, (self.width, self.height))
        if self.button_class == "Splitter_right":
            self.image = pygame.transform.scale(splitter_right_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(splitter_right_ns_img, (self.width, self.height))
        if self.button_class == "Splitter_left":
            self.image = pygame.transform.scale(splitter_left_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(splitter_left_ns_img, (self.width, self.height))
        if self.button_class == "Merger_right":
            self.image = pygame.transform.scale(merger_right_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(merger_right_ns_img, (self.width, self.height))
        if self.button_class == "Merger_left":
            self.image = pygame.transform.scale(merger_left_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(merger_left_ns_img, (self.width, self.height))
        if self.button_class == "Sqr_plate_deliver":
            self.image = pygame.transform.scale(sqr_plate_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(sqr_plate_ns_img, (self.width, self.height))
        if self.button_class == "Cir_plate_deliver":
            self.image = pygame.transform.scale(cir_plate_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(cir_plate_ns_img, (self.width, self.height))
        if self.button_class == "Tri_plate_deliver":
            self.image = pygame.transform.scale(tri_plate_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(tri_plate_ns_img, (self.width, self.height))
        if self.button_class == "Tunnel":
            self.image = pygame.transform.scale(cv_tunnel_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(cv_tunnel_ns_img, (self.width, self.height))
        if self.button_class == "Trash":
            self.image = pygame.transform.scale(trash_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(trash_ns_img, (self.width, self.height))
        if self.button_class == "Cutter":
            self.image = pygame.transform.scale(cutter_ui_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(cutter_ui_ns_img, (self.width, self.height))
        if self.button_class == "Rotator_ccw":
            self.image = pygame.transform.scale(rotator_ccw_ui_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(rotator_ccw_ui_ns_img, (self.width, self.height))
        if self.button_class == "Assembler":
            self.image = pygame.transform.scale(assembler_ui_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(assembler_ui_ns_img, (self.width, self.height))
        if self.button_class == "Sorter":
            self.image = pygame.transform.scale(sorter_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(sorter_ns_img, (self.width, self.height))
        if self.button_class == "Painter":
            self.image = pygame.transform.scale(painter_ui_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(painter_ui_ns_img, (self.width, self.height))

        if self.button_class == "Red_paint_deliver":
            self.image = pygame.transform.scale(red_paint_deliver_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(red_paint_deliver_ns_img, (self.width, self.height))
        if self.button_class == "Green_paint_deliver":
            self.image = pygame.transform.scale(green_paint_deliver_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(green_paint_deliver_ns_img, (self.width, self.height))
        if self.button_class == "Blue_paint_deliver":
            self.image = pygame.transform.scale(blue_paint_deliver_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(blue_paint_deliver_ns_img, (self.width, self.height))

        if self.button_class == "delete":
            self.image = pygame.transform.scale(delete_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(delete_ns_img, (self.width, self.height))
        if self.button_class == "simulation":
            self.image = pygame.transform.scale(simu_on_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(simu_off_img, (self.width, self.height))
        if self.button_class == "save":
            self.image = pygame.transform.scale(save_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(save_ns_img, (self.width, self.height))
        if self.button_class == "open":
            self.image = pygame.transform.scale(open_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(open_ns_img, (self.width, self.height))




    def draw(self, screen):
        # Call this method to draw the button on the screen if visible.
        if self.state == "depressed":
            self.color = LIGHTSHADE
            screen.blit(self.image_ns, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x , self.y))


    def click (self):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y) :
            print ("button clicked -> ", "Status before change", self.state)
            # special treatment for Simulation
            if self.button_class == "simulation":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            elif self.button_class == "delete":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            elif self.button_class == "save":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            elif self.button_class == "open":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            else:
                # if this is the creation button
                if self.state == "pressed":  # the button was pressed, so now we must be depressed it and hide all
                    print("this button becomes inactive")
                    self.state = "depressed"
                    '''for button in button_list:
                        button.state = "depressed"'''
                else:
                    print("this button becomes active")
                    self.state = "pressed"


def menu_reset (button_list):
    for button in button_list:
        button.state = "depressed"


def menu_selection_frombutton (button_list):
    object_class_pressed = ""
    for button in button_list:
        if button.state == "pressed":
            object_class_pressed = button.button_class
    return object_class_pressed


def menu_state_from_event (button_list):

    placement_type = ""
    for button in button_list:
        button.click()
        if button.state == "pressed":
            placement_type = button.button_class
    return placement_type


def menu_create (button_list):
    # create the buttons of the Interface
    button_position_x = 6 * tile_size + tile_size / 10
    button_position_y = tile_size / 10

    button_position_x = button_position_x + tile_size
    button_sqr_plate_deliver = Button("Sqr_plate_deliver", button_position_x, button_position_y)
    button_list.append(button_sqr_plate_deliver)

    button_position_x = button_position_x + tile_size
    button_cir_plate_deliver = Button("Cir_plate_deliver", button_position_x, button_position_y)
    button_list.append(button_cir_plate_deliver)

    button_position_x = button_position_x + tile_size
    button_tri_plate_deliver = Button("Tri_plate_deliver", button_position_x, button_position_y)
    button_list.append(button_tri_plate_deliver)

    button_position_x = button_position_x + tile_size
    button_trash = Button("Trash", button_position_x, button_position_y)
    button_list.append(button_trash)

    button_position_x = button_position_x + tile_size
    button_conveyor = Button("Conveyor", button_position_x, button_position_y)
    button_list.append(button_conveyor)

    button_position_x = button_position_x + tile_size
    button_splitter_right = Button("Splitter_right", button_position_x, button_position_y)
    button_list.append(button_splitter_right)

    button_position_x = button_position_x + tile_size
    button_splitter_left = Button("Splitter_left", button_position_x, button_position_y)
    button_list.append(button_splitter_left)

    button_position_x = button_position_x + tile_size
    button_merger_right = Button("Merger_right", button_position_x, button_position_y)
    button_list.append(button_merger_right)

    button_position_x = button_position_x + tile_size
    button_merger_left = Button("Merger_left", button_position_x, button_position_y)
    button_list.append(button_merger_left)

    button_position_x = button_position_x + tile_size
    button_tunnel = Button("Tunnel", button_position_x, button_position_y)
    button_list.append(button_tunnel)

    button_position_x = button_position_x + tile_size
    button_elbowr = Button("Elbow_right", button_position_x, button_position_y)
    button_list.append(button_elbowr)

    button_position_x = button_position_x + tile_size
    button_elbowl = Button("Elbow_left", button_position_x, button_position_y)
    button_list.append(button_elbowl)

    button_position_x = button_position_x + 2*tile_size
    button_cutter = Button("Cutter", button_position_x, button_position_y)
    button_list.append(button_cutter)

    button_position_x = button_position_x + tile_size
    button_rotator_ccw = Button("Rotator_ccw", button_position_x, button_position_y)
    button_list.append(button_rotator_ccw)

    button_position_x = button_position_x + tile_size
    button_assembler = Button("Assembler", button_position_x, button_position_y)
    button_list.append(button_assembler)

    button_position_x = button_position_x + tile_size
    button_sorter = Button("Sorter", button_position_x, button_position_y)
    button_list.append(button_sorter)

    button_position_x = button_position_x + tile_size
    button_painter = Button("Painter", button_position_x, button_position_y)
    button_list.append(button_painter)

    button_position_x = button_position_x + 2*tile_size
    button_red_paint_deliver = Button("Red_paint_deliver", button_position_x, button_position_y)
    button_list.append(button_red_paint_deliver)
    button_position_x = button_position_x + tile_size
    button_green_paint_deliver = Button("Green_paint_deliver", button_position_x, button_position_y)
    button_list.append(button_green_paint_deliver)
    button_position_x = button_position_x + tile_size
    button_blue_paint_deliver = Button("Blue_paint_deliver", button_position_x, button_position_y)
    button_list.append(button_blue_paint_deliver)

    return button_list
