from ursina import Ursina,Entity,color,DirectionalLight,Vec3,Sky
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader


# from panda3d.core import PStatClient
# PStatClient.connect() # 占用分析

app = Ursina()

Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))

class betterFPP(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


player = betterFPP(model='cube', color=color.white66, speed=8)

def update():
    pass

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()