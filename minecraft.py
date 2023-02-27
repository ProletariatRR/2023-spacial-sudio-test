
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random as rd
 
app=Ursina()
 
grass_texture=load_texture("texture/grass.jpg")
dirt_texture=load_texture("texture/dirt.jpg")
sky_texture=load_texture("texture/sky.jpg")
cobblestone_texture=load_texture("texture/cobblestone.png")
plank_texture=load_texture("texture/plank.jpg")
stone_texture=load_texture("texture/stone.jpg")
bedrock_texture=load_texture("texture/bedrock.jpg")
brick_texture=load_texture("texture/brick.png")
endstone_texture=load_texture("texture/endstone.jpg")
lapis_texture=load_texture("texture/lapis.jpg")
leaf_texture=load_texture("texture/leaf.jpg")
lucky_block_texture=load_texture("texture/luckyblock.png")
log_texture=load_texture("texture/log.jpg")
select_texture=grass_texture
 
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            scale=1500,
            texture=sky_texture,
            double_sided=True,
            position=(0,0,0)
        )
 
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="cube",
            scale=(0.2,0.3),
            color=color.white,
            rotation=Vec3(150,-10,0),
            position=Vec2(0.4,-0.4)
        )
 
    def active(self):
        self.position=Vec2(0.1,-0.5)
        self.rotation=Vec3(90,-10,0)
 
    def passive(self):
        self.rotation=Vec3(150,-10,0)
        self.position=Vec2(0.4,-0.4)
 
class Block(Button):
    def __init__(self,position=(0,0,0),texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            highlight_color=color.lime,
            color=color.white,
            texture=texture,
            origin_y=0.5
        )
 
    def input(self,key):
        if self.hovered:
            if key=="right mouse down":
                Block(position=self.position+mouse.normal,texture=select_texture)
            if key=="left mouse down":
                if self.texture!=bedrock_texture:
                    destroy(self)
 
    def update(self):
        global select_texture
        if held_keys["1"]: select_texture=grass_texture
        if held_keys["2"]: select_texture=dirt_texture
        if held_keys["3"]: select_texture=cobblestone_texture
        if held_keys["4"]: select_texture=plank_texture
        if held_keys["5"]: select_texture=stone_texture
        if held_keys["6"]: select_texture=brick_texture
        if held_keys["7"]: select_texture=endstone_texture
        if held_keys["8"]: select_texture=lapis_texture
        if held_keys["9"]: select_texture=leaf_texture
        if held_keys["0"]: select_texture=lucky_block_texture
        if held_keys["-"]: select_texture=log_texture
        if held_keys["left mouse"] or held_keys["right mouse"]:
            hand.active()
        else:
            hand.passive()
 
class Tree:
    def __init__(self,pos=False,_height=False):
        global trees
        global height
        if pos==False:
            pos=rd.randint(-15,15),rd.randint(-15,15)
        for i,y in enumerate(range(height+3,height+1+_height+2)):
            n=_height-2-i
            for x in range(-n,n):
                for z in range(-n,n):
                    Block(position=(pos[0]+x,y,pos[1]+z),texture=leaf_texture)
        for i in range(_height):
            y=height+i
            Block(position=(pos[0],y,pos[1]),texture=log_texture)
 
height=2
for y in range(0,height):
    for z in range(-15,16):
        for x in range(-15,16):
            print(f"Position:({x},{y},{z})")
            if y==height-1:
                texture=grass_texture
            else:
                texture=bedrock_texture
            Block(position=(x,y,z),texture=texture)
 
Tree(_height=5)
 
player=FirstPersonController()
sky=Sky()
hand=Hand()
 
app.run()