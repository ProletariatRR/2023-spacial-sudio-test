from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

# from panda3d.core import Texture

import pyaudio

# import librosa


 # 性能占用分析
# from panda3d.core import PStatClient
# PStatClient.connect()


class FPP(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def speed_factor(self):
        if held_keys['shift'] == True:
            return 1.5
        else:
            return 1

    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed * self.speed_factor

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity


app = Ursina()

Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

player = FPP(model='cube', color=color.white66, speed=8)
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
                    frames_per_buffer=32,
                    stream_callback=callback
                )


app.run()

# release audio source
stream.close()
p.terminate()