# https://blender.stackexchange.com/questions/23086/add-a-simple-vertex-via-python
# https://blenderartists.org/t/create-vertex-and-edges-using-this-code/648786/11
# https://realpython.com/python-json/

# load in contour points generated from opencv into blender to create a new mesh

import bpy
import json

def collect_vertices(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
        
        # map [1,2,3] to (1,2,3) from data
        return list(map(lambda x: (x[0], x[1], x[2]), data))


def create_mesh(json_file, mesh_name="Test"):
    new_mesh = bpy.data.meshes.new(mesh_name)
    new_obj = bpy.data.objects.new(mesh_name, new_mesh)
    
    vertices = collect_vertices(json_file)
    
    new_mesh.from_pydata(vertices, [], []) # TODO: how about edges and faces?
    new_obj.show_name = True # do i really need this?
    new_mesh.update() # what does this do?

    bpy.context.collection.objects.link(new_obj)
    

json_file = "C:/Users/Nicholas/Desktop/programming/opencv-homography/contours.json"
create_mesh(json_file)