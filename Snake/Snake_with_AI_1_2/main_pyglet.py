from Field_Snake import Map, Snake
import pyglet.app
from pyglet.window import key

from Snake.AI.AI_snake import AI

snake = Snake()
map_field = Map()

AI = AI()

fps = pyglet.window.FPSDisplay(map_field.window)

times = 0.125
missed = 0


@map_field.window.event
def on_key_press(*args):
    global times
    snake.change_direction(args[0])

    if args[0] == key.BACKSLASH:
        AI.is_drawing_numbers = not AI.is_drawing_numbers
    if args[0] == key.P:
        snake.game_over = not snake.game_over

    if args[0] == key.EQUAL:
        times *= 2
        print(f"time x{times}")
    elif args[0] == key.MINUS:
        times /= 2
        print(f"time x{times}")


def update():
    global missed

    if times >= 1:
        for k in range(int(times)):
            map_field.update(snake=snake)
            if AI.AI and not snake.game_over:
                AI.next_step(snake=snake, map_field=map_field)
                if AI.nextStep:
                    on_key_press(AI.nextStep)
    else:
        missed += 1
        if missed * times >= 1:
            map_field.update(snake=snake)
            if AI.AI and not snake.game_over:
                AI.next_step(snake=snake, map_field=map_field)
                if AI.nextStep:
                    on_key_press(AI.nextStep)
            missed = 0


@map_field.window.event
def on_draw():
    update()

    map_field.draw(snake=snake)
    fps.draw()

    # print(AI.numbers_list[snake.head_position.y - 2][snake.head_position.x - 2])

    if AI.is_drawing_numbers:
        AI.numbers_batch.draw()


if __name__ == '__main__':
    pyglet.app.run()
