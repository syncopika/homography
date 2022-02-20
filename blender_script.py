# https://blender.stackexchange.com/questions/23086/add-a-simple-vertex-via-python
# https://blenderartists.org/t/create-vertex-and-edges-using-this-code/648786/11
# https://realpython.com/python-json/

# load in contour points/edges generated from opencv (via collect_contour_test.py) into blender to create a new mesh

import bpy
import json

def collect_vertices_and_edges(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
        
        # map [1,2,3] to (1,2,3) from data
        vertices = list(map(lambda x: (x[0], x[1], x[2]), data["coords"]))
        edges = list(map(lambda x: (x[0], x[1]), data["edges"]))
        
        return vertices, edges

def create_mesh(json_file, mesh_name="Test"):
    new_mesh = bpy.data.meshes.new(mesh_name)
    new_obj = bpy.data.objects.new(mesh_name, new_mesh)
    
    vertices, edges = collect_vertices_and_edges(json_file)
    
    new_mesh.from_pydata(vertices, edges, []) # TODO: how about faces?
    new_obj.show_name = True # do i really need this?
    new_mesh.update()

    bpy.context.collection.objects.link(new_obj)
    

json_file = "C:/Users/Nicholas/Desktop/programming/opencv-homography/contours.json"
create_mesh(json_file)