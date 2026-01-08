import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


def populate_vertices(num_rings, gap_between_rings=1):
    if num_rings < 0:
        raise RuntimeError("`num_rings` must be >=0.")
    
    vertices = []
    counter = 0
    for ring in range(num_rings+1):
        if ring > 0:
            for corner in range(6):
                angle = (corner/6)*(2*math.pi)
                x = math.sin(angle) * (gap_between_rings*ring)
                y = math.cos(angle) * (gap_between_rings*ring)
                vertices.append({
                    "i": counter,
                    "x": x,
                    "y": y,
                    "ring": ring,
                    "angle": angle,
                    "vertex": 0
                })
                counter += 1
                edge_length = ring + 1
                next_angle = ((corner+1)/6)*(2*math.pi)
                next_x = math.sin(next_angle) * (gap_between_rings*ring)
                next_y = math.cos(next_angle) * (gap_between_rings*ring)
                for vertex in range(1,edge_length-1):
                    new_x = x + (vertex/(edge_length-1)) * (next_x-x)
                    new_y = y + (vertex/(edge_length-1)) * (next_y-y)
                    vertices.append({
                        "i": counter,
                        "x": new_x,
                        "y": new_y,
                        "ring": ring,
                        "angle": angle,
                        "vertex": vertex
                    })
                    counter += 1            
        else:
            vertices.append({
                "i": counter,
                "x": 0,
                "y": 0,
                "ring": ring,
                "angle": 0,
                "vertex": 0
            })
            counter += 1
    df = pd.DataFrame(vertices)
    return df

def get_num_vertices_in_ring(ring):
    if ring == 0:
        return 1
    edge_length = ring-1
    return 6 + edge_length*6

def get_starting_vertex_of_ring(ring):
    if ring < 0:
        raise RuntimeError("`num_rings` must be >=0.")
    
    total = 0
    for i in range(ring):
        total += get_num_vertices_in_ring(i)
    return total
    


num_rings = 10

vertices = populate_vertices(num_rings, gap_between_rings=1)


triangles = []

starting_a = 0
starting_b = 1
for ring in range(num_rings+1):
    working_a = starting_a + 0
    working_b = starting_b + 0
    for edge in range(6):
        for i in range(ring):
            if (edge == 5) and (i == ring-1):
                triangles.append((starting_a, starting_b, working_b))
                starting_a = working_a + 1
                starting_b = working_b + 1
            else:
                triangles.append((working_a, working_b, working_b+1))
            if i < ring-1:
                if (edge == 5) and (i == ring-2):
                    triangles.append((starting_a, working_a, working_b+1))
                else:
                    triangles.append((working_a, working_a+1, working_b+1))
                    working_a += 1
            working_b += 1

edges = []

for t,tri in enumerate(triangles):
    for i in range(len(tri)):
        if (i < len(tri)-1):
            edges.append((t, tri[i], tri[i+1]))
        else:
            edges.append((t, tri[0], tri[-1]))

faces = pd.DataFrame(edges, columns=["face", "vertex0", "vertex1"])
edges = faces.drop_duplicates().sort_values(by=["vertex0", "vertex1"]).reset_index(drop=True)
edges["locked"] = "blue"
edges["removed"] = False

starting_vertex = get_starting_vertex_of_ring(num_rings)
for i in range(get_num_vertices_in_ring(num_rings)):
    if (i == get_num_vertices_in_ring(num_rings)-1):
        a, b = starting_vertex, starting_vertex+i
    else:
        a, b = starting_vertex+i, starting_vertex+i+1
    edges.loc[(edges["vertex0"]==a)&(edges["vertex1"]==b),"locked"] = "red"




def remove_edge(e, edges, faces):
    if (edges.loc[(edges["vertex0"]==e["vertex0"])&(edges["vertex1"]==e["vertex1"]), "locked"].iloc[0] != "red"):
        relevant_edges = faces.loc[faces["face"].isin(faces.loc[(faces["vertex0"]==e["vertex0"])&(faces["vertex1"]==e["vertex1"]),"face"].values), ["vertex0", "vertex1"]].drop_duplicates().reset_index(drop=True)
        for _,edge in relevant_edges.iterrows():
            edges.loc[(edges["vertex0"]==edge["vertex0"])&(edges["vertex1"]==edge["vertex1"]), "locked"] = "red"
        edges.loc[(edges["vertex0"]==e["vertex0"])&(edges["vertex1"]==e["vertex1"]), "locked"] = "white"
        edges.loc[(edges["vertex0"]==e["vertex0"])&(edges["vertex1"]==e["vertex1"]), "removed"] = True
    return edges

removal_order = random.sample(range(len(edges.index)), len(edges.index))
for edge in removal_order:
    edges = remove_edge(edges.loc[edge], edges, faces)





        


for _,edge in edges.iterrows():
    vertex0 = vertices.loc[vertices["i"]==edge["vertex0"],].iloc[0]
    vertex1 = vertices.loc[vertices["i"]==edge["vertex1"],].iloc[0]
    plt.plot([vertex0["x"], vertex1["x"]], [vertex0["y"], vertex1["y"]], color=edge["locked"])

plt.scatter(vertices["x"], vertices["y"], color="black", zorder=100)
plt.axis("equal")
plt.axis("off")
plt.show()