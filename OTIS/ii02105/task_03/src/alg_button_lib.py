from ipywidgets import (VBox, HBox, Button, Layout)


def alg_buttons(editor, G):


    def func_button(name):
        return Button(
            description=name,
            disabled=False,
            button_style='',
            tooltip=name,
            icon=''
        )


    num_verts = func_button("num_verts")
    num_verts.on_click(lambda x: print("num_verts:", G.num_verts()))

    num_edges = func_button("num_edges")
    num_edges.on_click(lambda x: print("num_edges:" ,G.num_edges()))

    degree = func_button("degree")
    degree.on_click(lambda x: print("degree:", G.degree()))

    degree_one = func_button("degree (select one vertice)")
    degree_one.on_click(lambda x: print(f"degree ({editor._selected_vertices}):", \
                                        G.degree(*editor._selected_vertices)))

    incidence_matrix = func_button("incidence_matrix")
    incidence_matrix.on_click(lambda x: print("incidence_matrix:\n", G.incidence_matrix()))

    adjacency_matrix = func_button("adjacency_matrix")
    adjacency_matrix.on_click(lambda x: print("adjacency_matrix:\n", G.adjacency_matrix()))

    is_tree = func_button("is_tree")
    is_tree.on_click(lambda x: print("is_tree:", G.is_tree()))

    is_self_complementary = func_button("is_self_complementary")
    is_self_complementary.on_click(lambda x: print("is_self_complementary:", G.is_self_complementary()))

    is_connected = func_button("is_connected")
    is_connected.on_click(lambda x: print("is_connected:", G.is_connected()))

    is_eulerian = func_button("is_eulerian")
    is_eulerian.on_click(lambda x: print("is_eulerian:", G.is_eulerian()))

    is_hamiltonian = func_button("is_hamiltonian")
    is_hamiltonian.on_click(lambda x: print("is_hamiltonian:", G.is_hamiltonian()))

    is_planar = func_button("is_planar")
    is_planar.on_click(lambda x: print("is_planar:", G.is_planar()))

    all_paths = func_button("all_paths (select two vertice):")
    all_paths.on_click(lambda x: print(f"all_paths ({editor._selected_vertices})", \
                                    G.all_paths(*editor._selected_vertices)))

    shortest_path = func_button("shortest_path (select two vertice):")
    shortest_path.on_click(lambda x: print(f"shortest_path ({editor._selected_vertices})", \
                                        G.shortest_path(*editor._selected_vertices)))

    distance = func_button("distance (select two vertice)")
    distance.on_click(lambda x: print(f"distance ({editor._selected_vertices}):", \
                                        G.distance(*editor._selected_vertices)))

    diameter = func_button("diameter")
    diameter.on_click(lambda x: print("diameter:", G.diameter()))

    radius = func_button("radius")
    radius.on_click(lambda x: print("radius:", G.radius()))

    center = func_button("center")
    center.on_click(lambda x: print("center:", G.center()))

    def eulerian_cycle_func(self):
        if not self.is_connected():
            return "no cycle"
        for i in range(self.num_verts()):
            if self.degree(i) % 2:
                return "no cycle"
        cycle = [0]
        visited = [False for i in range(self.num_verts())]
        visited[0] = True
        while len(cycle) < self.num_edges():
            for i in range(self.num_verts()):
                if self.adjacency_matrix()[cycle[-1]][i] and not visited[i]:
                    cycle.append(i)
                    visited[i] = True
                    break
            else:
                return None
        return cycle

    eulerian_cycle = func_button("eulerian_cycle")
    eulerian_cycle.on_click(lambda x: print("eulerian_cycle:", eulerian_cycle_func(G)))

    buttons_array = [num_verts, num_edges, degree, degree_one, incidence_matrix, adjacency_matrix, \
                     is_tree, is_self_complementary, is_connected, is_eulerian, is_hamiltonian, \
                    is_planar, all_paths, shortest_path, distance, diameter, radius, center, eulerian_cycle]

    return VBox([HBox(buttons_array[i:i + 3],
    layout=Layout(margin="1px 2px ")) for i in range(0, 19, 3)])
