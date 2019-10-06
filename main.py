import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 20
SCREEN_TITLE = "Space Shooter"

NUM_ENEMIES = 20
INITIAL_VELOCITY = 3
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
PLAYER_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/new_bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy
        

    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/ship.png", 0.5)
        self.hp = PLAYER_HP
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, hp, position):
        '''
        initializes an enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__(0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
     

        
class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.gray_9)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.health = 100
        self.health = self.health - 10
        self.enemy_bullet_list = arcade.SpriteList()


    def setup(self):
        '''
        Set up enemies
        '''
        enemyships = ['enemyship','rock','enemyship2']
        for i in range(NUM_ENEMIES):
            enemy = random.choice(enemyships)
            x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y = random.randint(MARGIN,SCREEN_HEIGHT-MARGIN)
            dx = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            dy = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            self.enemy_sprite = arcade.Sprite("assets/{enemy}.png".format(enemy=enemy), 0.5)
            self.enemy_sprite.center_x = x
            self.enemy_sprite.center_y = y
            self.enemy_sprite.dx = dx
            self.enemy_sprite.dy = dy
            self.enemy_sprite.mass = 1
            self.enemy_list.append(self.enemy_sprite)            
            

    def update(self, delta_time):
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        
        for e in self.enemy_list:

            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp < 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE
            
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
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x
        self.player.center_y = y
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
        pass

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()