from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint

app = Ursina()


start_position = Vec3(0, 6, 0)


player = FirstPersonController(
    collider='box',
    position=start_position
)

ground = Entity(
    model='plane',
    texture='grass',
    collider='mesh',
    scale=(30, 0, 3)
)


garis1 = Entity(
    model='cube',
    color=color.violet,
    scale=(0.4, 0.1, 53),
    z=29, x=-0.7
)

garis2 = duplicate(garis1, x=-3.7)
garis3 = duplicate(garis1, x=0.6)
garis4 = duplicate(garis1, x=3.6)


goal = Entity(
    color=color.brown,
    model='cube',
    collider='box',
    scale=(10, 1, 10), z=55
)


pillar = Entity(
    model='cube',
    color=color.red,
    scale=(1, 15, 1),
    x=-3.7, y=8, z=58
)
pillar2 = duplicate(pillar, x=3.6)


goal_sound = Audio('sound/Different Heaven - Safe And Sound  House  NCS - Copyright Free Music.mp3', autoplay=False)
destroy_sound = Audio('sound/Sound  Effect   -  Kaca Pecah.mp3', autoplay=False)


fall_count = -1
fall_count_text = Text(f"Falls: {fall_count}", position=(0, 0.45), origin=(0, 0), scale=2)
timer = 0
timer_text = Text(f"Time: {timer:.2f}", position=(0, 0.40), origin=(0, 0), scale=2)
goal_reached = False

def create_blocks():
    blocks = []
    for i in range(12):
        block = Entity(
            model='cube', collider='box',
            color=color.white33,
            position=(2, 0.1, 3 + i * 4),
            scale=(3, 0.1, 2.5)
        )
        block2 = duplicate(block, x=-2.2)

        blocks.append(
            (block, block2, randint(0, 3) > 0,
             randint(0, 3) > 0
             )
        )
    return blocks

blocks = create_blocks()

def reset_game():
    global fall_count, timer, goal_reached, blocks
    fall_count = 0
    fall_count_text.text = f"Falls: {fall_count}"
    timer = 0
    timer_text.text = f"Time: {timer:.2f}"
    goal_reached = False
    player.position = start_position
    for block, block2, k, n in blocks:
        destroy(block)
        destroy(block2)
    blocks = create_blocks()

def update():
    global fall_count, timer, goal_reached
    for block, block2, k, n in blocks:
        if player.intersects(block).hit and k:
            destroy_sound.play()
            destroy(block)
            block.fade_out(duration=0.1)
            blocks.remove((block, block2, k, n))
            break  
        elif player.intersects(block2).hit and n:
            destroy_sound.play()
            destroy(block2)
            block2.fade_out(duration=0.1)
            blocks.remove((block, block2, k, n))
            break  

    
    if not goal_reached:
        timer += time.dt
        timer_text.text = f"Time: {timer:.2f}"

    if player.y < -10:
        fall_count += 1
        fall_count_text.text = f"Falls: {fall_count}"
        player.position = start_position  
   
    if player.intersects(goal).hit and not goal_reached:
        goal_sound.play()
        show_success_message()
        goal_reached = True

def input(key):
    global goal_reached
    if key == 'escape':
        application.quit()
    if key == 'r' and goal_reached:
        goal_sound.stop()
        reset_game()

def show_success_message():
    success_message = Text("Selamat Kamu Telah Menamatkan Game ini", origin=(0, 0), scale=2)
    invoke(destroy, success_message, delay=5)  
app.run()
