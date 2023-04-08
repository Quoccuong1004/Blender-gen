import bpy
import math
import random
import mathutils
import os
import time 
from mathutils import Vector


# Import the object
# bpy.ops.import_scene.obj(filepath='C:\\Users\\Admin\\Desktop\\Project\\Blender\pallet.fbx')
pallet = bpy.data.objects['Pallet']

pallet.scale = (6, 6, 6)  # increase the size along each axis

# Set the object's location to (0,0,5)
pallet.location = (0, 0, 0.474)

# Create an empty object as the target and set it to the center of the object
#target = bpy.data.objects.new('Target', None)
#target.location = pallet.location
#bpy.context.scene.collection.objects.link(target)

cam = bpy.data.objects['Camera']

# Make the camera follow the target
track = cam.constraints.new(type='TRACK_TO')
track.target = pallet

scene = bpy.context.scene

# Set the camera to follow the target
bpy.context.scene.camera = cam

# Add a light source to the scene
light = bpy.data.objects["Point"]

# Set the render engine to Cycles
scene.render.engine = 'BLENDER_EEVEE'



#Setup the output properties
#scene.render.image_settings.file_format = 'OPEN_EXR'
#scene.render.image_settings.color_mode = 'RGBA'
#scene.render.image_settings.color_depth = '32' # Set color depth to Float (Full)
#scene.render.image_settings.use_zbuffer = True

# Set the render resolution
bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480

# Get the focal length of the camera
focal_length = cam.data.lens

# Define the initial coordinates and step sizes
loc = pallet.location

for i in range(1):
    # Move pallet along x-axis by 1 unit
#    loc.x += 0.5
    # Loop through 10 iterations
    for j in range(10):
#        # Move pallet along y-axis by 0.015 units
#        loc.y += 0.5
        # Set the current frame
        bpy.context.scene.frame_set(i+j + i* j +40)
#        # Set the pallet's location for this frame
#        pallet.location.x = loc.x
#        pallet.location.y = loc.y
#        pallet.location.z = 0.079

        # Set the location of the camera for this frame
        x_2 = random.randint(-5, 5)
        y_2 = random.randint(-5,5)
        z_2 = random.randint(6,7)
        cam.location = (x_2, y_2, z_2)

        # Render the image and save it to disk
        image_name = f'render_{i*10+j}.jpg'
        bpy.context.scene.render.filepath = f'C:\\Users\\Admin\\Desktop\\Project\\Blender\\test_images\\{image_name}'
        bpy.ops.render.render(write_still=True)

        # Get the width and height of the camera viewport
        
        cam_width = bpy.context.scene.render.resolution_x
        cam_height = bpy.context.scene.render.resolution_y

        # Compute the projection matrix from camera space to 2D image space
        proj_mat = cam.calc_matrix_camera(
        bpy.context.evaluated_depsgraph_get(),
        x=cam_width, y=cam_height
        ).to_4x4()
        
        # Get the pallet's mesh data
        mesh = pallet.data
        
        # Compute the pallet's vertices in camera space
        camera_mat = cam.matrix_world.inverted()
        world_mat = pallet.matrix_world
        verts_cam = [camera_mat @ world_mat @ v.co for v in mesh.vertices]

        # Tính toán khoảng cách giữa các đỉnh trong không gian camera
        width = (verts_cam[1] - verts_cam[0]).length
        height = (verts_cam[3] - verts_cam[0]).length
        
        # Tính toán chiều dài và chiều rộng của vật thể trong viewport
        scale_x = cam_width / cam.data.sensor_width
        scale_y = cam_height / cam.data.sensor_height
        width_pixels = width * scale_x
        height_pixels = height * scale_y
        # Compute the bounding box coordinates in camera space
        bbox_min_cam = mathutils.Vector((min(v.x for v in verts_cam), min(v.y for v in verts_cam), min(v.z for v in verts_cam)))
        bbox_max_cam = mathutils.Vector((max(v.x for v in verts_cam), max(v.y for v in verts_cam), max(v.z for v in verts_cam)))

        # Compute the center of the bounding box in camera space
        center_cam = (bbox_max_cam + bbox_min_cam) / 2

        # Project the bounding box center onto the 2D image plane
        center_2d = proj_mat @ center_cam.to_4d()
        center_2d /= center_2d.w

#        # Compute the width and height of the bounding box in 2D image space
#        width_2d = abs((bbox_max_cam.x - bbox_min_cam.x) / center_cam.z * focal_length/1000 * cam_width)
#        height_2d = abs((bbox_max_cam.y - bbox_min_cam.y) / center_cam.z * focal_length/1000 * cam_height)
#        
        # Scale the coordinates to the range [0, 1]            
        x_2d = center_2d.x / cam_width
        y_2d = center_2d.y / cam_height
        width_2d = width_pixels / cam_width
        height_2d = height_pixels / cam_height
        
#        x_2d = round(x_2d,4)
#        y_2d = round(y_2d,4)
#        width_2d = round(width_2d,4)
#        height_2d = round(height_2d,4)

        # Open the annotation file for writing and write the bounding box coordinates in YOLO format
        with open("C:\\Users\\Admin\\Desktop\\annotations.txt", "a") as f:
            f.write(f"{image_name},{pallet.name},{x_2d},{y_2d},{width_2d},{height_2d}\n")


