import bpy
import math
import random
import mathutils
import os
import time 
# Import the object
# bpy.ops.import_scene.obj(filepath='C:\\Users\\Admin\\Desktop\\Materials\\20221\\Project I\\Blender\pallet.fbx')
pallet = bpy.data.objects["Pallet_1"]
pallet.scale = (1, 1, 1)  # increase the size along each axis

# Set the object's location to (0,0,0)
pallet.location = (0, 0, 0.072)

# Create an empty object as the target and set it to the center of the object
#target = bpy.data.objects.new('Target', None)
#target.location = pallet.location
#bpy.context.scene.collection.objects.link(target)

# Create a new camera
cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))

# Set the camera's field of view
cam.data.angle = math.radians(100)

# Make the camera follow the target
track = cam.constraints.new(type='TRACK_TO')
track.target = pallet

# Set the camera to follow the target
bpy.context.scene.camera = cam

# Add a light source to the scene
light = bpy.data.objects["Point"]

# Define the initial coordinates and step sizes
loc = pallet.location

for i in range(5):
    loc.x += 0.05
    for j in range(3):                
        loc.y += 0.05
        bpy.context.scene.frame_set(i+j + i* j +80)
        pallet.location.x = loc.x
        pallet.location.y = loc.y
        pallet.location.z = 0.079
        
        # Set the location of the camera for this frame
        x_2 = random.randint(-8, 8)
        y_2 = random.randint(-8, 8)
        z_2 = random.randint(2, 8)
        cam.location = (x_2, y_2, z_2)

        # Render the image
        image_name = f'render_{i*3+j}.tif'
        bpy.context.scene.render.filepath = f'C:\\Users\\Admin\\Desktop\\Materials\\20221\\Project I\\Blender\\rendered_image\\{image_name}'
        bpy.ops.render.render(write_still=True)

        # Get the object's mesh data
        mesh = pallet.data

        # Get the world matrix of the object
        world_mat = pallet.matrix_world

        # Get the coordinates of the mesh vertices in world space
        verts = [world_mat @ v.co for v in mesh.vertices]

        # Compute the 3D bounding box coordinates
        bbox_min = mathutils.Vector((min(v.x for v in verts), min(v.y for v in verts), min(v.z for v in verts)))
        bbox_max = mathutils.Vector((max(v.x for v in verts), max(v.y for v in verts), max(v.z for v in verts)))

        # Compute the width, height, and depth of the bounding box
        width = bbox_max.x - bbox_min.x
        height = bbox_max.y - bbox_min.y
        depth = bbox_max.z - bbox_min.z

        # Compute the center of the bounding box
        center = (bbox_max + bbox_min) / 2

        # Open the annotation file for writing
        with open("C:\\Users\\Admin\\Desktop\\annotations.txt", "a") as f:
            # Write the bounding box coordinates to the file
            f.write(f"{image_name},{pallet.name},{center.x},{center.y},{center.z},{width},{height},{depth}\n")
    
    


    
