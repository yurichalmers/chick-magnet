import arcade
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "cHiCk mAgNeT game"
CHARACTER_SCALING = 1
TILE_SCALING = 1

PLAYER_MOVEMENT_SPEED = 6
ANGLE_SPEED = 2

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 450
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

view_left = 0
view_bottom = 0

image_source = "./img"

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_SAD = 2

PLAYER_HEIGHT = 81
PLAYER_WIDTH = 82

class Ceiling(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = TILE_SCALING
        self.textures = []

        texture = arcade.load_texture(f"{image_source}/ceiling.png")
        self.textures.append(texture)
        self.texture = texture

class Ground(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = TILE_SCALING
        self.textures = []

        texture = arcade.load_texture(f"{image_source}/ground.png")
        self.textures.append(texture)
        self.texture = texture

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.scale = CHARACTER_SCALING
        self.textures = []

        texture = arcade.load_texture(f"{image_source}/cm2_left.png")
        self.textures.append(texture)
        texture = arcade.load_texture(f"{image_source}/cm2_right.png")
        self.textures.append(texture)
        texture = arcade.load_texture(f"{image_source}/cm2_right_sad.png")
        self.textures.append(texture)

        texture_front = arcade.load_texture(f"{image_source}/cm2_front.png")

        self.texture = texture_front

        self.speed = 0
        self.change_x = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.cos(angle_rad)
        self.center_y += self.speed * math.sin(angle_rad)


class BadGuy(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = CHARACTER_SCALING
        self.textures = []

        texture = arcade.load_texture(f"{image_source}/magnet_guy.png")
        self.textures.append(texture)

        self.texture = texture

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture(f"{image_source}/title_screen_simple.png")

        self.view_bottom = 0
        self.view_left = 0

        self.cast_list = None
        self.hero = None
        self.badguy = None

        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.csscolor.LIGHT_YELLOW)

    def setup(self):
        self.view_bottom = 0
        self.view_left = 0

        self.cast_list = arcade.SpriteList()
        self.hero = Player()
        self.hero.center_x = SCREEN_WIDTH/4
        self.hero.center_y = SCREEN_HEIGHT/4
        self.cast_list.append(self.hero)
        self.badguy = BadGuy()
        self.badguy.center_x = 3* (SCREEN_WIDTH/4)
        self.badguy.center_y = SCREEN_HEIGHT/4
        self.cast_list.append(self.badguy)

    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.cast_list.draw()
        arcade.draw_text("Press Enter to Continue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT /2) - 50, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_update(self, delta_time):
        self.cast_list.update()

    def on_key_press(self, key,modifiers):
        if key == arcade.key.ENTER:
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)

class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
    def on_show(self):
        # arcade.set_background_color(arcade.csscolor.LIGHT_GRAY)
        arcade.set_viewport(view_left, SCREEN_WIDTH+view_left, view_bottom, SCREEN_HEIGHT+view_bottom)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Press UP and DOWN to travel through the magnetic tunnel without getting stuck!", SCREEN_WIDTH / 2, (SCREEN_HEIGHT /2) - 50, arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press Enter to Continue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT /2) - 150, arcade.color.BLACK, font_size=20, anchor_x="center")
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

class WinScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(f"{image_source}/win_screen.png")
        self.view_bottom = 0
        self.view_left = 0

        self.window.set_mouse_visible(False)
    def on_show(self):
        arcade.set_viewport(self.view_left, SCREEN_WIDTH+self.view_left, self.view_bottom, SCREEN_HEIGHT+self.view_bottom)

    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.draw_text("YOU WIN!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.PURPLE, font_size=50, anchor_x="center")
        arcade.draw_lrtb_rectangle_filled(left=view_left-100,
                                          right=self.game_view.player_sprite.right+RIGHT_VIEWPORT_MARGIN+200,
                                          top=SCREEN_HEIGHT+1000,
                                          bottom=view_bottom-100,
                                          color=arcade.color.RED + (50,))
    def on_key_press(self, key, modifier):
        if key==arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class DeadScreen(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    # def on_show(self):
    #     arcade.set_background_color(arcade.color.RED)
    def on_draw(self):
        arcade.start_render()
        player_sprite=self.game_view.player_sprite
        ceiling_list=self.game_view.ceiling_list
        ground_list=self.game_view.ground_list
        player_sprite.draw()
        ceiling_list.draw()
        ground_list.draw()
        arcade.draw_lrtb_rectangle_filled(left=view_left-100,
                                          right=self.game_view.player_sprite.right+RIGHT_VIEWPORT_MARGIN+200,
                                          top=SCREEN_HEIGHT+1000,
                                          bottom=view_bottom-100,
                                          color=arcade.color.RED + (50,))
        arcade.draw_text("GAME OVER", self.game_view.player_sprite.center_x, (SCREEN_HEIGHT/2), arcade.csscolor.WHITE, font_size = 100, anchor_x = "center")
        arcade.draw_text("Press Enter to Restart", self.game_view.player_sprite.center_x, (SCREEN_HEIGHT/2)-150, arcade.csscolor.WHITE, font_size = 30, anchor_x = "center")
    def on_update(self, delta_time):
        self.game_view.player_sprite.texture = self.game_view.player_sprite.textures[TEXTURE_SAD]
    
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = None
        self.boundary_list = None
        self.ceiling_list = None
        self.ground_list = None

        self.player_sprite = None

        self.left_pressed = False
        self.right_pressed = True
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None

        self.level = 1

        self.view_bottom = 0
        self.view_left = 0

        self.window.set_mouse_visible(False)

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.LIGHT_PINK)

    def level_1(self):
        easy = 100
        for x in range(400, 800, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+100
            ground.top =easy+100
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        for x in range(800, 1600, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+50
            ground.top = easy+50
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        for x in range(1600, 2000, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+0
            ground.top = easy+0
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        for x in range(2000, 2800, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT-40
            ground.top = easy-40
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        for x in range(2800, 3200, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+10
            ground.top = easy+10
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        for x in range(3200, 3600, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+60
            ground.top = easy+60
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.boundary_list)

        self.player_sprite.speed = PLAYER_MOVEMENT_SPEED

    def level_2(self):
        easy = 100
        for x in range(400, 800, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+100
            ground.top =easy+100
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(800, 1200, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+40
            ground.top =easy+40
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(1200, 1600, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+90
            ground.top =easy+90
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(1600, 2000, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+50
            ground.top =easy+50
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(2000, 2400, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT
            ground.top =easy
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(2400, 2800, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT-15
            ground.top =easy-15
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(2800, 3200, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT
            ground.top =easy
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(3200, 3600, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+60
            ground.top =easy+60
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.boundary_list)
    def level_3(self):
        easy = 100
        for x in range(400, 800, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+40
            ground.top =easy+40
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(800, 1200, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT-30
            ground.top =easy-30
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(1200, 1600, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT-70
            ground.top =easy-70
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(1600, 2000, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT-90
            ground.top =easy-90
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(2000, 2400, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT-50
            ground.top =easy-50
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(2400, 2800, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+10
            ground.top =easy+10
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(2800, 3200, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+75
            ground.top =easy+75
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)
        for x in range(3200, 3600, 400):
            ceiling = Ceiling()
            ground = Ground()
            ceiling.left = x
            ground.left = x
            ceiling.top = SCREEN_HEIGHT+50
            ground.top =easy+50
            self.boundary_list.append(ceiling)
            self.boundary_list.append(ground)
            self.ceiling_list.append(ceiling)
            self.ground_list.append(ground)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.boundary_list)

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.ceiling_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.boundary_list = arcade.SpriteList()

        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0
        self.level = 1

        self.level_1()

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.boundary_list.draw()


        score_text = f"Score: {self.score}"
        level = f"Level: {self.level}"
        arcade.draw_text(score_text, 10 + self.view_left, 10+self.view_bottom, arcade.csscolor.WHITE, 18)
        arcade.draw_text(level, 10 + self.view_left, 27+self.view_bottom, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.player_sprite.change_angle = -ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            self.player_sprite.change_angle = 0
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.player_sprite.change_angle = 0
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.player_sprite.texture = self.player_sprite.textures[TEXTURE_RIGHT]
            self.right_pressed = True

    def on_update(self, delta_time):
        angle_rad = math.radians(self.player_sprite.angle)
        self.score += int(abs(self.player_sprite.speed *math.sin(angle_rad))/2)

        self.player_sprite.center_x = int(self.player_sprite.center_x)
        for ceiling in self.ceiling_list:
            if self.player_sprite.center_x in range(int(ceiling.left), int(ceiling.right)) and self.player_sprite.top > ceiling.bottom-12:
                self.player_sprite.angle = -90
                self.player_sprite.speed = 0
                self.player_sprite.change_x = 0
                self.player_sprite.top = ceiling.bottom
                dead_screen = DeadScreen(self)
                self.window.show_view(dead_screen)

        self.player_sprite.center_x = int(self.player_sprite.center_x)
        for ground in self.ground_list:
            if self.player_sprite.center_x in range(int(ground.left), int(ground.right)) and self.player_sprite.bottom < ground.top+12:
                self.player_sprite.angle = 90
                self.player_sprite.speed = 0
                self.player_sprite.change_x = 0
                self.player_sprite.bottom = ground.top
                dead_screen = DeadScreen(self)
                self.window.show_view(dead_screen)
                

        if self.player_sprite.center_x >= 3700 and self.level == 1:
            self.player_sprite.center_x = SCREEN_WIDTH/2
            self.player_sprite.center_y = SCREEN_HEIGHT/2
            self.level+=1
            for ceiling in self.ceiling_list:
                ceiling.remove_from_sprite_lists()
            for ground in self.ground_list:
                ground.remove_from_sprite_lists()
            for ceiling in self.boundary_list:
                ceiling.remove_from_sprite_lists()
            for ground in self.boundary_list:
                ground.remove_from_sprite_lists()
            self.level_2()
        elif self.player_sprite.center_x >= 3700 and self.level == 2:
            self.player_sprite.center_x = SCREEN_WIDTH/2
            self.player_sprite.center_y = SCREEN_HEIGHT/2
            self.level+=1
            for ceiling in self.ceiling_list:
                ceiling.remove_from_sprite_lists()
            for ground in self.ground_list:
                ground.remove_from_sprite_lists()
            for ceiling in self.boundary_list:
                ceiling.remove_from_sprite_lists()
            for ground in self.boundary_list:
                ground.remove_from_sprite_lists()
            self.level_3()
        elif self.player_sprite.center_x >= 3700 and self.level == 3:
            win_screen_view = WinScreenView()
            self.window.show_view(win_screen_view)



        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_angle = ANGLE_SPEED
            if self.player_sprite.angle > 90:
                self.player_sprite.change_angle = 0
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_angle = -ANGLE_SPEED
            if self.player_sprite.angle < -90:
                self.player_sprite.change_angle = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED / 2
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        
        self.physics_engine.update()
        self.player_list.update()
        self.ceiling_list.update()
        self.ground_list.update()

        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    title_view = TitleView()
    window.show_view(title_view)
    title_view.setup()
    arcade.run()
    # win_screen_view = WinScreenView()
    # window.show_view(win_screen_view)
    # arcade.run()

if __name__ == "__main__":
    main()
        
