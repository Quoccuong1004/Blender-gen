import bpy
import math
import random
import mathutils
import os
import time 
from mathutils import Vector,Matrix
import bpy_extras
import shutil


# Import the object
# bpy.ops.import_scene.obj(filepath='C:\\Users\\Admin\\Desktop\\Project\\Blender\pallet.fbx')
pallet = bpy.data.objects['Pallet']
container = bpy.data.objects['Container20']
barrier = bpy.data.objects['Barrier']
transpallet = bpy.data.objects['transpallet']
transpallet_2 = bpy.data.objects['transpallet.001']
box = bpy.data.objects['box']
box_2 = bpy.data.objects['box.001']
box_3 = bpy.data.objects['box.002']
abs = bpy.data.objects['abs']
abs_2 = bpy.data.objects['abs.001']
circle = bpy.data.objects['Circle']
circle_2 = bpy.data.objects['Circle.001']

pallet.scale = (6, 6, 6)  # increase the size along each axis
container.scale = (0.08,0.08,0.08)
barrier.scale = (3, 3, 3)
transpallet.scale = (0.08,0.08,0.08)
transpallet_2.scale = (0.08,0.08,0.08)
abs.scale = (4,4,4)
abs_2.scale = (4,4,4)
circle.scale = (3,3,3)
circle_2.scale = (3,3,3)

# Set the object's location to (0,0,5)
pallet.location = (0, 0, 0.474)
container.location = (-25, 12, 0)
barrier.location = (0,0,2)
transpallet.location = (6,5,0.5)
transpallet_2.location = (10,5,0.5)
box.location = (-8,8,2)
box_2.location = (-12,8,2)
box_3.location = (-16,8,2)
abs.location = (7,-7,2)
abs_2.location = (9,-7,2)
circle.location = (-8,-8,2)
circle_2.location = (-8,-11,2)
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

def project_by_object_utils(cam, point):
    """returns normalized (x, y) image coordinates in OpenCV frame for a given blender world point."""
    
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, point)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    # convert y coordinate to opencv coordinate system!
    # return Vector((co_2d.x * render_size[0], render_size[1] - co_2d.y * render_size[1]))
    return Vector((co_2d.x, 1 - co_2d.y))  # normalized

def get_camera_KRT(camera):
    """return 3x3 camera matrix K and 4x4 rotation, translation matrix RT.
    Experimental feature, the matrix might be wrong!"""
    # https://www.blender.org/forum/viewtopic.php?t=20231
    # Extrinsic and Intrinsic Camera Matrices
    scn = bpy.data.scenes['Scene']
    w = scn.render.resolution_x * scn.render.resolution_percentage / 100.
    h = scn.render.resolution_y * scn.render.resolution_percentage / 100.
    # Extrinsic
    RT = cam.matrix_world.inverted()
    # Intrinsic
    K = Matrix().to_3x3()
    K[0][0] = -w / 2 / math.tan(camera.data.angle / 2)
    ratio = w / h
    K[1][1] = -h / 2. / math.tan(camera.data.angle / 2) * ratio
    K[0][2] = w / 2.
    K[1][2] = h / 2.
    K[2][2] = 1.
    return K, RT

def orderCorners(objBB):
    """change bounding box corner order."""
    # change bounding box order according to
    # https://github.com/Microsoft/singleshotpose/blob/master/label_file_creation.md
    out = []
    corners = [v[:] for v in objBB]  # list of tuples (x,y,z)
    out.append(corners[0])  # -1 -1 -1
    out.append(corners[1])  # -1 -1 1
    out.append(corners[3])  # -1 1 -1
    out.append(corners[2])  # -1 1 1
    out.append(corners[4])  # 1 -1 -1
    out.append(corners[5])  # 1 -1 1
    out.append(corners[7])  # 1 1 -1
    out.append(corners[6])  # 1 1 1
    return out


for i in range(100):
    # Move pallet along x-axis by 1 unit
#    loc.x += 0.5
    # Loop through 10 iterations
    for j in range(10):
#        # Move pallet along y-axis by 0.015 units
#        loc.y += 0.5
        # Set the current frame
        bpy.context.scene.frame_set(100)
#        # Set the pallet's location for this frame
#        pallet.location.x = loc.x
#        pallet.location.y = loc.y
#        pallet.location.z = 0.079

        # Set the location of the camera for this frame
        x_2 = random.uniform(-6, -3) if random.random() < 0.5 else random.uniform(3, 6)
        y_2 = random.uniform(-6, -3) if random.random() < 0.5 else random.uniform(3, 6)
        z_2 = random.uniform(1,6)
        cam.location = (x_2, y_2, z_2)

        # Render the image and save it to disk
        image_name = f'render_{i*10+j}.jpg'
        bpy.context.scene.render.filepath = f'C:\\Users\\Admin\\Desktop\\Project\\Blender\\test_images\\{image_name}'
        bpy.ops.render.render(write_still=True)

#        # Get the width and height of the camera viewport
#        
        cam_width = bpy.context.scene.render.resolution_x
        cam_height = bpy.context.scene.render.resolution_y

        center = project_by_object_utils(cam, pallet.location)
        class_ = 0  # class label for object
        labels = [class_]
        labels.append(center[0])  # center x coordinate in image space
        labels.append(center[1])
        corners = orderCorners(pallet.bound_box)
        kps = []
        repeat = False
        for corner in corners:
            p = pallet.matrix_world @ Vector(corner)  # object space to world space
            p = project_by_object_utils(cam, p)  # world space to image space
            labels.append(p[0])
            labels.append(p[1])
            if (p[0] < 0 or p[0] > 1 or p[1] < 0 or p[1] > 1):
                v = 1  # v=1: labeled but not visible
            else:
                v = 2  # v=2: labeled and visible
        P = cam.matrix_world.inverted() @ pallet.matrix_world
        min_x, max_x, min_y, max_y = 1, 0, 1, 0
        vertices = pallet.data.vertices
        for v in vertices:
            vec = project_by_object_utils(cam,pallet.matrix_world @ Vector(v.co))
            x = vec[0]
            y = vec[1]
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y
        # save labels in txt file (deprecated)
        x_range = max_x - min_x
        y_range = max_y - min_y
        x = (max_x + min_x)/2
        y = (max_y + min_y)/2
        labels.append(x_range)
        labels.append(y_range)
        
        # fix center point
        labels[1] = (max_x + min_x) / 2
        labels[2] = (max_y + min_y) / 2        
        
        width = x_range 
        height = y_range 
        # Open the annotation file for writing and write the bounding box coordinates in YOLO format
        with open("C:\\Users\\Admin\\Desktop\\annotations.txt", "a") as f:
            f.write(f"{image_name},{pallet.name},{x},{y},{width},{height}\n")
        

