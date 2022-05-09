_NAMES = """\
aircraft carrier,airplane,alarm clock,ambulance,angel
animal migration,ant,anvil,apple,arm
asparagus,axe,backpack,banana,bandage
barn,baseball bat,baseball,basket,basketball
bat,bathtub,beach,bear,beard
bed,bee,belt,bench,bicycle
binoculars,bird,birthday cake,blackberry,blueberry
book,boomerang,bottlecap,bowtie,bracelet
brain,bread,bridge,broccoli,broom
bucket,bulldozer,bus,bush,butterfly
cactus,cake,calculator,calendar,camel
camera,camouflage,campfire,candle,cannon
canoe,car,carrot,castle,cat
ceiling fan,cell phone,cello,chair,chandelier
church,circle,clarinet,clock,cloud
coffee cup,compass,computer,cookie,cooler
couch,cow,crab,crayon,crocodile
crown,cruise ship,cup,diamond,dishwasher
diving board,dog,dolphin,donut,door
dragon,dresser,drill,drums,duck
dumbbell,ear,elbow,elephant,envelope
eraser,eye,eyeglasses,face,fan
feather,fence,finger,fire hydrant,fireplace
firetruck,fish,flamingo,flashlight,flip flops
floor lamp,flower,flying saucer,foot,fork
frog,frying pan,garden hose,garden,giraffe
goatee,golf club,grapes,grass,guitar
hamburger,hammer,hand,harp,hat
headphones,hedgehog,helicopter,helmet,hexagon
hockey puck,hockey stick,horse,hospital,hot air balloon
hot dog,hot tub,hourglass,house plant,house
hurricane,ice cream,jacket,jail,kangaroo
key,keyboard,knee,knife,ladder
lantern,laptop,leaf,leg,light bulb
lighter,lighthouse,lightning,line,lion
lipstick,lobster,lollipop,mailbox,map
marker,matches,megaphone,mermaid,microphone
microwave,monkey,moon,mosquito,motorbike
mountain,mouse,moustache,mouth,mug
mushroom,nail,necklace,nose,ocean
octagon,octopus,onion,oven,owl
paint can,paintbrush,palm tree,panda,pants
paper clip,parachute,parrot,passport,peanut
pear,peas,pencil,penguin,piano
pickup truck,picture frame,pig,pillow,pineapple
pizza,pliers,police car,pond,pool
popsicle,postcard,potato,power outlet,purse
rabbit,raccoon,radio,rain,rainbow
rake,remote control,rhinoceros,rifle,river
roller coaster,rollerskates,sailboat,sandwich,saw
saxophone,school bus,scissors,scorpion,screwdriver
sea turtle,see saw,shark,sheep,shoe
shorts,shovel,sink,skateboard,skull
skyscraper,sleeping bag,smiley face,snail,snake
snorkel,snowflake,snowman,soccer ball,sock
speedboat,spider,spoon,spreadsheet,square
squiggle,squirrel,stairs,star,steak
stereo,stethoscope,stitches,stop sign,stove
strawberry,streetlight,string bean,submarine,suitcase
sun,swan,sweater,swing set,sword
syringe,t-shirt,table,teapot,teddy-bear
telephone,television,tennis racquet,tent,The Eiffel Tower
The Great Wall of China,The Mona Lisa,tiger,toaster,toe
toilet,tooth,toothbrush,toothpaste,tornado
tractor,traffic light,train,tree,triangle
trombone,truck,trumpet,umbrella,underwear
van,vase,violin,washing machine,watermelon
waterslide,whale,wheel,windmill,wine bottle
wine glass,wristwatch,yoga,zebra,zigzag
"""
_NAMES = [name for line in _NAMES.strip().splitlines() for name in line.strip().split(",")]

# from urllib.request import pathname2url
# import os

# with open(r"C:\Users\Mario\Downloads\bed.ndjson", encoding="utf-8") as f:
#     line = next(iter(f))

# for name in _NAMES:
#     with open(os.path.join("dummy", "raw", f"{name}.ndjson").replace(" ", "+"), "w", encoding="utf-8") as f:
#         f.write(line)

# import struct
# with open(r"C:\Users\Mario\Downloads\bed.bin", "rb") as f:
#     def process_struct(fileobj):
#         """
#         Process a struct from a binary file object.

#         The code for this function is borrowed from the following link:
#         https://github.com/googlecreativelab/quickdraw-dataset/blob/f0f3beef0fc86393b3771cdf1fc94828b76bc89b/examples/binary_file_parser.py#L19
#         """
#         (key_id,) = struct.unpack("Q", fileobj.read(8))
#         (country_code,) = struct.unpack("2s", fileobj.read(2))
#         (recognized,) = struct.unpack("b", fileobj.read(1))
#         (timestamp,) = struct.unpack("I", fileobj.read(4))
#         (n_strokes,) = struct.unpack("H", fileobj.read(2))
#         drawing = []
#         for _ in range(n_strokes):
#             (n_points,) = struct.unpack("H", fileobj.read(2))
#             fmt = str(n_points) + "B"
#             x = struct.unpack(fmt, fileobj.read(n_points))
#             y = struct.unpack(fmt, fileobj.read(n_points))
#             drawing.append({"x": list(x), "y": list(y)})

#     process_struct(f)
#     pos = f.tell()
#     f.seek(0)
#     line = f.read(pos)

# for name in _NAMES:
#     with open(os.path.join("dummy", "preprocessed_simplified_drawings", f"{name}.bin").replace(" ", "+"), "wb") as f:
#         f.write(line)

import os

import numpy as np


line = np.arange(28 * 28).reshape(1, 28, 28)
for i, name in enumerate(_NAMES):
    if i > 1:
        line = np.array([])
    with open(os.path.join("dummy", "preprocessed_bitmaps", f"{name}.npy").replace(" ", "+"), "wb") as f:
        np.save(f, line)
