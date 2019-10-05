import sys, logging, random, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 20
INITIAL_VELOCITY = 3
NUM_ENEMIES = 5
SCREEN_TITLE = "Collision Exercise"

   

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.blue_4)
        self.enemy_list = arcade.SpriteList()

    def setup(self):
        enemyships = ['ship2','ship3','ship4','ship6','ship7']
        for i in range(NUM_ENEMIES):
            enemy = random.choice(enemyships)
            x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y = random.randint(MARGIN,SCREEN_HEIGHT-MARGIN)
            dx = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            dy = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            self.enemy_sprite = arcade.Sprite("assets/{enemy}.jpg".format(enemy=enemy), 0.5)
            self.enemy_sprite.center_x = x
            self.enemy_sprite.center_y = y
            self.enemy_sprite.dx = dx
            self.enemy_sprite.dy = dy
            self.enemy_sprite.mass = 1
            self.enemy_list.append(self.enemy_sprite)            

    def update(self, delta_time):
        for a in self.enemy_list:
            a.center_x += a.dx
            a.center_y += a.dy



            collisions = a.collides_with_list(self.enemy_list)
            for c in collisions:
                tx = a.dx
                ty = a.dy
                a.dx = c.dx 
                a.dy = c.dy 
                c.dx = tx
                c.dy = ty
                pass

            if a.center_x <= MARGIN:
                a.center_x = MARGIN
                a.dx = abs(a.dx)
            if a.center_x >= SCREEN_WIDTH - MARGIN:
                a.center_x = SCREEN_WIDTH - MARGIN
                a.dx = abs(a.dx)*-1
            if a.center_x <= MARGIN:
                a.center_x = MARGIN
                a.dx = abs(a.dx)
            if a.center_y <= MARGIN:
                a.center_y = MARGIN
                a.dy = abs(a.dy)
            if a.center_y >= SCREEN_HEIGHT - MARGIN:
                a.center_y = SCREEN_HEIGHT - MARGIN
                a.dy = abs(a.dy)*-1


    def on_draw(self):
        arcade.start_render()
        self.enemy_list.draw()





def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()