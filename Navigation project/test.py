import pygame
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (106, 159, 181)

# Initialize Pygame
pygame.init()

# Set up of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ez-Nav SFIT')


title_font = pygame.font.Font(None, 48)
button_font = pygame.font.Font(None, 32)
table_font = pygame.font.Font(None, 24)

# Load background image for the welcome screen
background_image = pygame.image.load("background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BLUE
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def clicked(self):
        if self.action:
            self.action()

# Define pages
def welcome_page():
    screen.blit(background_image, (0, 0))  # Blit background image
    title_surf = title_font.render('Easy-Nav SFIT', True, WHITE)
    title_rect = title_surf.get_rect(center=(screen_width // 2, 100))
    screen.blit(title_surf, title_rect)

    start_button.draw(screen)

def floor_info_page():
    screen.fill(WHITE)
    title_surf = title_font.render('Floor Information', True, BLACK)
    title_rect = title_surf.get_rect(center=(screen_width // 2, 50))
    screen.blit(title_surf, title_rect)

    # Display table
    locations = ["Lift", "Director's Office", "Principal's Office", "Main Office",
                 "Exam Control Office", "Computer Center", "Account's Office",
                 "IT Staff room", "Seminar Hall", "Board Room", "Staff Pantry"]
    floor = "First Floor"
    row_height = 30
    y_offset = 100

    # Calculate the width of the longest text in the locations list
    max_text_width = max(table_font.size(text)[0] for text in locations)

    # Calculate the starting x-coordinate to center the table
    start_x = (screen_width - max_text_width - table_font.size(floor)[0] - 100) // 2

    for i, location in enumerate(locations):
        location_surf = table_font.render(location, True, BLACK)
        location_rect = location_surf.get_rect(topleft=(start_x, y_offset + i * row_height))
        screen.blit(location_surf, location_rect)

        floor_surf = table_font.render(floor, True, BLACK)
        floor_rect = floor_surf.get_rect(topleft=(start_x + max_text_width + 50, y_offset + i * row_height))
        screen.blit(floor_surf, floor_rect)

    # Add button to return to welcome page
    return_button.draw(screen)

    # Add button to go to pathfinding code
    pathfinding_button.draw(screen)


def start_game():
    current_page[0] = floor_info_page

def return_to_welcome():
    current_page[0] = welcome_page

def start_pathfinding():
    import pygame, sys
    from pathfinding.core.grid import Grid
    #name of the finder module
    from pathfinding.finder.a_star import AStarFinder
    from pathfinding.core.diagonal_movement import DiagonalMovement

    class Pathfinder:
        def __init__(self, matrix):
            # setup
            self.matrix = matrix
            self.grid = Grid(matrix=matrix)
            self.select_surf = pygame.image.load("selection.png").convert_alpha()
            self.new_path = []
            # pathfinding
            self.path = []

            # person
            self.user = pygame.sprite.GroupSingle(Person())

        # def empty_path(self):
        #     self.new_path= []
        # self.empty_path

        def draw_active_cell(self):
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // 32
            col = mouse_pos[0] // 32
            current_cell_value = self.matrix[row][col]

            # rect=pygame.Rect((left,top),(wid,hei))
            if current_cell_value == 1:
                # pygame object for storing rectangular coordinates
                rect = pygame.Rect((col * 32, row * 32), (32, 32))
                # convert coordinates system into a specific position on one map
                screen.blit(self.select_surf, rect)

        def create_path(self):
            # start

            start_x, start_y = self.user.sprite.get_coord()
            start = self.grid.node(start_x, start_y)

            # end
            mouse_pos = pygame.mouse.get_pos()
            end_x, end_y = mouse_pos[0] // 32, mouse_pos[1] // 32
            end = self.grid.node(end_x, end_y)

            # path
            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
            self.path, _ = finder.find_path(start, end, self.grid)
            self.new_path = [(path.__dict__["x"], path.__dict__["y"]) for path in self.path]

            # the above code is same as the below code
            # new_path = []
            # for i in self.path:
            #     new_path.append((path.__dict__["x"], path.__dict__["y"]))
            print(self.new_path)
            self.grid.cleanup()
            self.user.sprite.set_path(self.new_path)

        def draw_path(self):
            if self.new_path:
                point = []
                for points in self.new_path:
                    # if points[0] and points[1]==1:
                    x = (points[0] * 32) + 16
                    y = (points[1] * 32) + 16
                    point.append((x, y))

                    # pygame.draw.circle(screen,"#4a4a4a",(x,y),2)
                pygame.draw.lines(screen, "#4a4a4a", False, point, 5)
                # false is for having open or cosed lines if true we will have closed lines if false we will have open line

        def update(self):
            self.draw_active_cell()
            self.draw_path()
            # for the person
            self.user.update()
            self.user.draw(screen)

    class Person(pygame.sprite.Sprite):
        def __init__(self):
            # basics
            super().__init__()
            self.image = pygame.image.load("gg.png").convert_alpha()

            self.rect = self.image.get_rect(center=(608, 352))#currently value
            # movement
            self.pos = self.rect.center
            self.speed = 2
            self.direction = pygame.math.Vector2(0, 0)

            # path
            self.path = []
            self.collision_rects = []
            # self.empty_path=empty_path

        def get_coord(self):
            # location = input("Enter your current location: ")
            col = self.rect.centerx // 32
            row = self.rect.centery // 32
            return (col, row)

        def set_path(self, path):
            self.path = path
            self.create_collision_rects()
            self.get_directions()

        def create_collision_rects(self):
            if self.path:
                self.collision_rects = []
                for point in self.path:
                    x = (point[0] * 32) + 16
                    y = (point[1] * 32) + 16
                    # -2 is done because the rectangle will be placed exactly at the centre if this
                    # not done the rectangle will be placed slantingly which will generate an error
                    rect = pygame.Rect((x - 2, y - 2), (4, 4))
                    self.collision_rects.append(rect)

        def get_directions(self):
            # here if the collison_rects is empty the user tag won't move ahead
            if self.collision_rects:
                start = pygame.math.Vector2(self.pos)#current loc
                end = pygame.math.Vector2(self.collision_rects[0].center)#collirect_1
                self.direction = (end - start).normalize()
            else:
                self.direction = pygame.math.Vector2(0, 0)
                self.path = []

        def check_collision(self):
            if self.collision_rects:
                for rect in self.collision_rects:
                    if rect.collidepoint(self.pos):
                        del self.collision_rects[0]
                        self.get_directions()
            # else:
            #     self.empty_path()

        def update(self):
            self.pos += self.direction * self.speed
            self.check_collision()
            self.rect.center = self.pos


    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1230, 736))
    clock = pygame.time.Clock()

    # game setup

    bg_surf = pygame.image.load("R1.jpg")

    matrix = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
    ]


    # the creation of the instance of class
    pathfinder = Pathfinder(matrix)

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pathfinder.create_path()
        screen.blit(bg_surf, (0, 0))
        pathfinder.update()
        pygame.display.update()
        clock.tick(60)
    pass

# Create buttons
start_button = Button(300, 300, 200, 50, 'Start', action=start_game)
return_button = Button(50, screen_height - 70, 200, 50, 'Return to Welcome', action=return_to_welcome)
pathfinding_button = Button(screen_width - 250, screen_height - 70, 200, 50, 'Pathfinding', action=start_pathfinding)

# Set up page control
current_page = [welcome_page]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in [start_button, return_button, pathfinding_button]:
                if button.rect.collidepoint(event.pos):
                    button.clicked()

    current_page[0]()
    pygame.display.flip()

pygame.quit()
sys.exit()
