import pygame
# This is a list of every sprite. For machines
all_sprites_machines_list = pygame.sprite.Group()

# This is a group to handle tmp object
all_sprites_tmp = pygame.sprite.Group()

# This is a list of every sprite. For Cargos
all_sprites_cargos_list = pygame.sprite.Group()

# two lists to manage all the machines and the cargos
cargo_list = []
machine_list = []

# structure of relationship
# machine1, connector1 IN name, machine2, connector2 OUT name, Flag
# Flag is not used and default is True
relationship_list = []

# define game variables
tile_size = 50
screen_width = 1600
screen_height = 800

world_width = 6400
world_height = 3200

scroll_step = tile_size

# geometry of shape and quadrants
qz = tile_size*0.8/2
snipe_ratio = 4
# snipes sizes
sr = qz/snipe_ratio
ss = qz/snipe_ratio

# fibonaci quadrant size :5->3->2->1
quadrant_size = {'0': 0, '1': qz, '2': 4*qz//5 , '3' : 3*qz//5 , '4': 2*qz//5}


# an empty shape
empty_shape_dna = "N0d/n/n/n/n:N0d/n/n/n/n:N0d/n/n/n/n:N0d/n/n/n/n"

# Define some colors
BLACK = (0  ,  0,  0)
WHITE = (255,255,255)

RED   = (255,  0,  0)
GREEN = (0  ,255,  0)
BLUE  = (0  ,0 , 255)

YELLOW  = (255,255,  0)
CYAN    = (0  ,255,255)
MAGENTA = (255,  0,255)

LIGHTSHADE = (170, 170, 170)
DARKSHADE = (100, 100, 100)

RUSTY = (99, 11, 27)
GREY = (126,132,140)

# mouse click index
LEFT = 1
RIGHT = 3

# initialisation of images paths
path_tmp = 'img/machine.png'
tmp_img = pygame.image.load(path_tmp)

path_splitter_right_img = 'img/splitter_right.bmp'
splitter_right_img = pygame.image.load(path_splitter_right_img)

path_splitter_left_img = 'img/splitter_left.bmp'
splitter_left_img = pygame.image.load(path_splitter_left_img)

path_cv = 'img/conveyor.bmp'
cv_img = pygame.image.load(path_cv)

path_elb_right_img = 'img/elbow_right.bmp'
elb_right_img = pygame.image.load(path_elb_right_img)

path_elb_left_img = 'img/elbow_left.bmp'
elb_left_img = pygame.image.load(path_elb_left_img)

path_merger_right_img = 'img/merger_right.bmp'
merger_right_img = pygame.image.load(path_merger_right_img)

path_merger_left_img ='img/merger_left.bmp'
merger_left_img = pygame.image.load(path_merger_left_img)

path_cv_tunnel_img = 'img/tunnel.bmp'
cv_tunnel_img = pygame.image.load(path_cv_tunnel_img)

path_trash_img = 'img/trash.png'
trash_img = pygame.image.load(path_trash_img)

path_target_img = 'img/target.png'
target_img = pygame.image.load(path_target_img)

path_src_square_plate_deliver_img = 'img/sqr_plate_deliver.bmp'
src_square_plate_deliver_img = pygame.image.load(path_src_square_plate_deliver_img)

path_src_circle_plate_deliver_img = 'img/cir_plate_deliver.bmp'
src_circle_plate_deliver_img = pygame.image.load(path_src_circle_plate_deliver_img)

path_src_triangle_plate_deliver_img = 'img/tri_plate_deliver.bmp'
src_triangle_plate_deliver_img = pygame.image.load(path_src_triangle_plate_deliver_img)

path_cutter_obj_img = 'img/cutter_obj.png'
cutter_obj_img = pygame.image.load(path_cutter_obj_img)

path_rotator_ccw_obj_img ='img/rotator_CCW.bmp'
rotator_ccw_obj_img = pygame.image.load(path_rotator_ccw_obj_img)

path_assembler_obj_img  = 'img/assembler_obj.png'
assembler_obj_img = pygame.image.load(path_assembler_obj_img)

path_sorter_img = 'img/sorter.bmp'
sorter_img = pygame.image.load(path_sorter_img)

path_painter_obj_img = 'img/painter_obj.png'
painter_obj_img = pygame.image.load(path_painter_obj_img)

path_red_paint_obj_img = 'img/red_paint_obj.png'
red_paint_obj_img = pygame.image.load(path_red_paint_obj_img)

path_blue_paint_obj_img = 'img/blue_paint_obj.png'
blue_paint_obj_img = pygame.image.load(path_blue_paint_obj_img)

path_green_paint_obj_img = 'img/green_paint_obj.png'
green_paint_obj_img = pygame.image.load(path_green_paint_obj_img)

path_red_paint_deliver_img = 'img/red_paint_deliver.png'
red_paint_deliver_img = pygame.image.load(path_red_paint_deliver_img)

path_blue_paint_deliver_img = 'img/blue_paint_deliver.png'
blue_paint_deliver_img = pygame.image.load(path_blue_paint_deliver_img)

path_green_paint_deliver_img = 'img/green_paint_deliver.png'
green_paint_deliver_img = pygame.image.load(path_green_paint_deliver_img)


# initialisation of images (no selection)

elb_right_ns_img = pygame.image.load('img/elbow_right_ns.bmp')
elb_left_ns_img = pygame.image.load('img/elbow_left_ns.bmp')
cv_ns_img = pygame.image.load('img/conveyor_ns.bmp')


merger_right_ns_img = pygame.image.load('img/merger_right_ns.bmp')
merger_left_ns_img = pygame.image.load('img/merger_left_ns.bmp')


cv_tunnel_ns_img = pygame.image.load('img/tunnel_ns.bmp')
trash_ns_img = pygame.image.load('img/trash_ns.png')

splitter_right_ns_img = pygame.image.load('img/splitter_right_ns.bmp')
splitter_left_ns_img = pygame.image.load('img/splitter_left_ns.bmp')

sqr_plate_img = pygame.image.load('img/sqr_plate_deliver.bmp')
sqr_plate_ns_img = pygame.image.load('img/sqr_plate_deliver_ns.bmp')

cir_plate_img = pygame.image.load('img/cir_plate_deliver.bmp')
cir_plate_ns_img = pygame.image.load('img/cir_plate_deliver_ns.bmp')

tri_plate_img = pygame.image.load('img/tri_plate_deliver.bmp')
tri_plate_ns_img = pygame.image.load('img/tri_plate_deliver_ns.bmp')

simu_off_img = pygame.image.load('img/simulationOFF.bmp')
simu_on_img = pygame.image.load('img/simulationON.bmp')

delete_img = pygame.image.load('img/delete.bmp')
delete_ns_img = pygame.image.load('img/delete_ns.bmp')

cutter_ui_img = pygame.image.load('img/cutter_ui.bmp')
cutter_ui_ns_img = pygame.image.load('img/cutter_ui_ns.bmp')

rotator_ccw_ui_img = pygame.image.load('img/rotator_CCW.bmp')
rotator_ccw_ui_ns_img = pygame.image.load('img/rotator_CCW_ns.bmp')

assembler_ui_img = pygame.image.load('img/assembler_ui.bmp')
assembler_ui_ns_img = pygame.image.load('img/assembler_ui_ns.bmp')

sorter_ns_img = pygame.image.load('img/sorter_ns.bmp')

painter_ui_img = pygame.image.load('img/painter_ui.bmp')
painter_ui_ns_img = pygame.image.load('img/painter_ui_ns.bmp')

save_img = pygame.image.load('img/save.png')
save_ns_img = pygame.image.load('img/save_ns.png')

open_img = pygame.image.load('img/open.png')
open_ns_img = pygame.image.load('img/open_ns.png')

red_paint_deliver_ns_img   = pygame.image.load('img/red_paint_deliver_ns.png')
blue_paint_deliver_ns_img  = pygame.image.load('img/blue_paint_deliver_ns.png')
green_paint_deliver_ns_img = pygame.image.load('img/green_paint_deliver_ns.png')
