from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

from panda3d.core import Texture

import pyaudio

# from panda3d.core import PStatClient

# PStatClient.connect() # 占用分析

app = Ursina()

Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

player = FirstPersonController(model='cube', color=color.white66, speed=8)
max_fps = 60
dtime = 1/max_fps

Entity(
    model='cube', origin_y=-.5, scale=1, 
    texture='brick', texture_scale=(1,2),
    x=2,
    z=2,
    collider='box',
    scale_y = 2,
    color=color.hsv(0, 0, random.uniform(.9, 1))
)

def update():
    '''
    # video frame update function
    '''
    global x, y, z 
    x, y, z = player.position[0], player.position[1], player.position[2]
    # time.sleep(dtime)
    pass


def callback(in_data, frame_count, time_info, status):
    '''
    # audio frame update function
    '''
    # print(round(x,1),round(y,1),round(z,1))


    return (in_data, pyaudio.paContinue)




p = pyaudio.PyAudio()
stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    input=True,
                    frames_per_buffer=1024,
                    stream_callback=callback
                )


app.run()


stream.close()

    # Release PortAudio system resources (6)
p.terminate()