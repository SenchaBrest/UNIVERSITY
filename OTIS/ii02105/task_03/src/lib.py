#!/usr/bin/env sage
"""
Graph editor for sage on jupyter

A simple graph editor where one can see the graph, add vertices/edges,
etc.

**Main methods:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GraphEditor.show` | Show the widget
    :meth:`~GraphEditor.refresh` | Redraw everything

**Widget appearance:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GraphEditor.set_vertex_pos` | Set the position of a vertex
    :meth:`~GraphEditor.set_vertices_pos` | Set the position of vertices
    :meth:`~GraphEditor.get_vertex_pos` | Get the position of a vertex
    :meth:`~GraphEditor.get_vertices_pos` | Get the position of vertices
    :meth:`~GraphEditor.set_vertex_radius` | Set the radius of a vertex
    :meth:`~GraphEditor.get_vertex_radius` | Get the radius of a vertex
    :meth:`~GraphEditor.set_vertex_color` | Set the color of a vertex
    :meth:`~GraphEditor.get_vertex_color` | Get the color of a vertex
    :meth:`~GraphEditor.set_edge_color` | Set the color of an edge
    :meth:`~GraphEditor.get_edge_color` | Get the color of an edge
    :meth:`~GraphEditor.get_vertex_label` | Get the label of a vertex
    :meth:`~GraphEditor.output_text` | Write text below the drawing


There are more methods to edit the graph (adding vertices / edges), that
are private and can be discovered if needed by looking at the source.

EXAMPLES:

When the editor is called with no argument, an empty graph is created::

    sage: from phitigra import GraphEditor
    sage: ed = GraphEditor()
    sage: ed.show() # random
    # The canvas is empty and you can add vertices and edges with the mouse

When a graph is given to the editor constructor, this graph is drawn and all
the changes done with the widget (adding or removing vertices for instance)
are performed on the given graph::

    sage: from phitigra import GraphEditor
    sage: G = graphs.RandomGNP(10, 0.5)
    sage: ed = GraphEditor(G)
    sage: ed.show() # random
    # Any change done now in the widget is done on G
    # The graph in the widget can be accessed with .graph
    sage: ed.graph is G
    True

A copy of the drawn graph can be obtained with the
:meth:`~GraphEditor.get_graph` method::

    sage: from phitigra import GraphEditor
    sage: G = graphs.RandomGNP(10, 0.5)
    sage: ed = GraphEditor(G)
    sage: H = ed.get_graph()
    sage: H == G
    True
    sage: H is G
    False

Changing the color of vertices or edges is possible with the widget but also by
calling the appropriate methods::

    sage: from phitigra import GraphEditor
    sage: G = graphs.CompleteGraph(10)
    sage: ed = GraphEditor(G)

At first the vertices have the default color::

    sage: ed.show() # random

We set vertices color depending on parity:

    sage: for v in G: ed.set_vertex_color(v, 'blue' if is_odd(v) else 'red')
    sage: ed.refresh()

Same for edges::

    sage: for (u, v, _) in G.edge_iterator():
    ....:     ed.set_edge_color((u, v), 'green' if is_odd(u+v) else 'orange')
    sage: ed.refresh()

One of the text boxes of the widget can be edited::

    sage: from phitigra import GraphEditor
    sage: ed = GraphEditor()
    sage: ed.show() # random
    sage: ed.output_text("Hello world!")

"Hello world" should appear below the drawing.

AUTHORS:

- Jean-Florent Raymond (2020-04-05): initial version
"""

# ***********************************************************************
#     Copyright (C) 2020 Jean-Florent Raymond <j-florent.raymond@uca.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ***********************************************************************

from ipycanvas import MultiCanvas, hold_canvas
from ipywidgets import (Label, BoundedIntText, Text, VBox, HBox, Output, Button,
                        Dropdown, ColorPicker, ToggleButton,
                        Layout, ToggleButtons)
from numpy import randrange
from numpy.random import randint as randint
from math import pi, sqrt, atan2
from copy import copy

from sage.graphs.all import Graph
from sage.modules.free_module_element import vector


class GraphEditor():
    """
    Base class for the graph editor.
    """

    # Output widget used to print error messages (for debug)
    _output = Output()

    @staticmethod
    def _draw_arrow(canvas):
        """
        Draw an arrow at with tip at `(0,0)`, pointing to the left.

        Used when drawing directed graphs.

        INPUT:

        - ``canvas`` -- canvas; the canvas where to draw the arrow.

        OUTPUT:

        No output, only side effects. Draws an arrow on the canvas.

        TESTS::

        A dummy test, for this drawing function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: ed._draw_arrow(ed._multi_canvas[0])
        """
        a_x = 15  # Length of the arrow
        a_y = 8   # Half-width of the arrow
        canvas.begin_path()
        canvas.move_to(0, 0)
        canvas.line_to(a_x, a_y)
        canvas.line_to(0.75*a_x, 0)
        canvas.line_to(a_x, -a_y)
        canvas.move_to(0, 0)
        canvas.fill()

    def __init__(self, G=None,
                 width=600, height=400, default_radius=20,
                 default_vertex_color=None, default_edge_color='black',
                 show_vertex_labels=True, show_edge_labels=True):
        """
        Prepare the widget with the given graph.

        The graph should not allow loops neither multiedges.
        In this function the properties of vertices and eges (width, color)
        are initialized and the elements of the graph editor (widgets, canvas,
        callbacks) are defined.

        INPUT:

        - ``G`` -- graph from :class:`Graph` or :class:`DiGraph` that does not
          allow loops neither multiedges (default: `None`); the graph to
          plot and edit. If `None`, an empty graph will be used instead.

        - ``width`` and ``height`` -- integers (default 600 and 400
          respectively); the sizes in pixel of the canvas where
          the graph is drawn;
        - ``default_radius`` -- integer (default 20); the default radius for
          the shape of vertices;
        - ``default_vertex_color`` -- integer (default ``None``); the initial
          colors of the vertices of ``G``; if ``None`` a random color will be
          used for each vertex;
        - ``default_edge_color`` -- color (default: ``'black'``);
        - ``show_vertex_labels`` and ``show_edge_labels`` -- boolean
          (default: True); whether to display vertex and edge labels.

        OUTPUT: a graph editor widget

        EXAMPLES:

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph(), width=200)
            sage: type(ed)
            <class 'phitigra.graph_editor.GraphEditor'>

            sage: g = Graph(0)
            sage: g.allow_multiple_edges(True)
            sage: GraphEditor(g)
            Traceback (most recent call last):
            ...
            ValueError: The graph allows loops or multiedges

        """

        if G is None:
            G = Graph(0)

        if G.allows_multiple_edges() or G.allows_loops():
            raise ValueError("The graph allows loops or multiedges")

        self.graph = G

        self._drawing_param = {
            # Sizes of the widget
            'width': int(width),
            'height': int(height),
            # Defaults for drawing vertices
            'default_radius': int(default_radius),
            'default_vertex_color': default_vertex_color,
            'default_edge_color': default_edge_color,
            'show_vertex_labels': show_vertex_labels,
            'show_edge_labels': show_edge_labels
        }

        # The layout (+6 to account for the 3px border on both sides)
        lyt = {'border': '3px solid lightgrey',
               'width': str(self._drawing_param['width'] + 6) + 'px',
               'height': str(self._drawing_param['height'] + 6) + 'px',
               'overflow': 'visible'}
        # The canvas where to draw
        self._multi_canvas = (
            MultiCanvas(4,
                        width=self._drawing_param['width'],
                        height=self._drawing_param['height'],
                        sync_image_data=True,
                        layout=lyt)
        )

        # It consists in 4 layers
        self._e_canvas = self._multi_canvas[0]    # The main layer for edges
        self._v_canvas = self._multi_canvas[2]    # The main layer for vertices

        # Same, but for drawing onjects in interaction (eg dragged vertices
        # without redrawing everything
        self._e_interact_canvas = self._multi_canvas[1]    # For edges
        self._v_interact_canvas = self._multi_canvas[3]    # For vertices

        self._selected_vertices = set()
        self._selected_edges = set()
        self._dragged_vertex = None
        self._dragging_canvas_from = None

        # Registering callbacks for mouse interaction on the canvas
        self._multi_canvas[3].on_mouse_down(self._mouse_down_handler)
        self._multi_canvas[3].on_mouse_move(self._mouse_move_handler)
        self._multi_canvas[3].on_mouse_up(self._mouse_up_handler)
        # When the mouse leaves the canvas, we free the node that
        # was being dragged, if any:
        self._multi_canvas[3].on_mouse_out(self._mouse_up_handler)

        # The widgets of the graph editor (besides the canvas):

        # Where to display messages:
        self._text_output = Label("Graph Editor", layout={'width': '100%'})
        # Data about the graph:
        self._text_graph = Label("", layout={'width': '100%'})

        # The drawing tools
        self._tool_selector = ToggleButtons(
            options=['select / move',
                     'add vertex or edge',
                     'delete vertex or edge'],
#                     'add walk',
#                     'add clique',
#                     'add star'],
            description='',
            disabled=False,
            button_style='',
            tooltips=['Move vertices or the canvas',
                      'Add vertices or edges',
                      'Delete vertices or edges'],
#                      'Add a walk through new or existing vertices',
#                      'Add a clique through new or existing vertices',
#                      'Add a star through new or existing vertices'],
            icons=['']*5,
            layout={'width': '150px', "margin": "0px 2px 0px auto"}
        )
        # We unselect any possibly selected vertex when the current
        # tool is changed, in order to avoid problems with the deletion
        # tool
        self._tool_selector.observe(lambda _: self._tool_selector_clbk())
        self._current_tool = lambda: self._tool_selector.value

        # Selector to change layout
        self._layout_selector = Dropdown(
            options=[('- change layout -', '- change layout -'),
                     ('random', 'random'),
                     ('spring', 'spring'),
                     ('circular', 'circular'),
                     ('planar', 'planar'),
                     ('forest (root up)', 'forest (root up)'),
                     ('forest (root down)', 'forest (root down)'),
                     ('directed acyclic', 'acyclic')],
            value='- change layout -',
            description='',
            layout={'width': '150px', "margin": "1px 2px 1px auto"}
        )
        self._layout_selector.observe(self._layout_selector_clbk)

        # Buttons to rescale:
        self._zoom_in_button = Button(description='',
                                      disabled=False,
                                      button_style='',
                                      tooltip='Zoom in',
                                      icon='search-plus',
                                      layout={'height': '36px',
                                              'width': '36px',
                                              'margin': '0px 1px 0px 0px'})
        self._zoom_in_button.on_click(lambda x: (self._scale_layout(1.5),
                                                 self.refresh()))
        self._zoom_to_fit_button = Button(description='',
                                          disabled=False,
                                          button_style='',
                                          tooltip=('Zoom to fit'),
                                          icon='compress',
                                          layout={'height': '36px',
                                                  'width': '36px',
                                                  'margin': '0px 1px 0px 1px'})
        self._zoom_to_fit_button.on_click(lambda x: (self._normalize_layout(),
                                                     self.refresh()))
        self._zoom_out_button = Button(description='',
                                       disabled=False,
                                       button_style='',
                                       tooltip='Zoom out',
                                       icon='search-minus',
                                       layout={'height': '36px',
                                               'width': '36px',
                                               'margin': '0px 1px 0px 1px'})
        self._zoom_out_button.on_click(lambda x: (self._scale_layout(2/3),
                                                  self.refresh()))

        # To clear the drawing
        self._clear_drawing_button = Button(description="",
                                            disabled=False,
                                            button_style='',
                                            tooltip=('Clear the drawing and '
                                                     'delete the graph'),
                                            icon='trash',
                                            layout={'height': '36px',
                                                    'width': '36px',
                                                    'margin': ('0px 0px '
                                                               '0px 1px')})
        self._clear_drawing_button.on_click(self._clear_drawing_button_clbk)

        # Selector to change the color of the selected vertex
        self._color_selector = ColorPicker(
            concise=False,
            description='',
            value='#437FC0',
            disabled=False,
            layout={'height': '36px',
                    'width': '112px',
                    'margin': '0px 1px 0px 0px'}
        )
        self._color_button = Button(description='',
                                    disabled=False,
                                    button_style='',
                                    tooltip=('Apply color to the '
                                             'selected elements'),
                                    icon='paint-brush',
                                    layout={'height': '36px',
                                            'width': '36px',
                                            'margin': '0px 0px 0px 1px'})
        self._color_button.on_click((lambda x: self._color_button_clbk()))

        self._vertex_radius_box = BoundedIntText(
            value=self._drawing_param['default_radius'],
            min=1,
            max=100,
            step=1,
            description="",
            disabled=False,
            layout={'width': '90px',
                    'margin': 'auto 1px auto 0px'}
        )
        self._radius_button = Button(description='',
                                     disabled=False,
                                     button_style='',
                                     tooltip=('Change the radius of the '
                                              'selected vertices'),
                                     icon='expand',
                                     layout={'height': '36px',
                                             'width': '36px',
                                             'margin': '0px 0px 0px 1px'})
        self._radius_button.on_click((lambda x: self._radius_button_clbk()))

        self._vertex_label_toggle = ToggleButton(
            value=self._drawing_param['show_vertex_labels'],
            description='Show vertex labels',
            disabled=False,
            button_style='',
            tooltip='Should the vertex label be drawn?',
            icon='',
            layout={"width": "150px", "margin": "1px 2px 1px auto"}
        )
        self._vertex_label_toggle.observe(lambda _: self.refresh())

        self._edge_label_toggle = ToggleButton(
            value=self._drawing_param['show_edge_labels'],
            description='Show edge labels',
            disabled=False,
            button_style='',
            tooltip='Should the edge label be drawn?',
            icon='',
            layout={"width": "150px", "margin": "1px 2px 1px auto"}
        )
        self._edge_label_toggle.observe(lambda _: self.refresh())

        self._vertex_label_box = Text(
            value='',
            placeholder='Vertex label',
            description='',
            disabled=False,
            layout={'width': '150px', "margin": "0px 2px 0px auto"}
        )
        self._set_vertex_label_button = Button(
            description='OK',
            disabled=False,
            button_style='',
            tooltip='Set the label of the selected vertex',
            icon='pencil',
            layout={"width": "150px", "margin": "1px 2px 1px auto"}
        )
        self._set_vertex_label_button.on_click(
            lambda x: self._set_vertex_label_button_clbk())

        self._edge_label_box = BoundedIntText(
            value=1,
            min=None,
            max=None,
            step=1,
            description="",
            disabled=False,
            layout={'width': '150px', "margin": "0px 2px 0px auto"}
        )
        self._set_edge_label_button = Button(
            description='OK',
            disabled=False,
            button_style='',
            tooltip='Set the label of the selected edge',
            icon='pencil',
            layout={"width": "150px", "margin": "1px 2px 1px auto"}
        )
        self._set_edge_label_button.on_click(
            lambda x: self._set_edge_label_button_clbk())

        # The final widget, which contains all the parts defined above
        self._widget = HBox([VBox([self._multi_canvas,
                                   HBox([self._text_graph, self._text_output]),
                                   self._output]),
                             VBox([
                                 self._tool_selector,
                                 self._layout_selector,
                                 HBox([self._zoom_in_button,
                                       self._zoom_to_fit_button,
                                       self._zoom_out_button,
                                       self._clear_drawing_button],
                                      layout=Layout(margin="1px 2px "
                                                    + "1px auto")),
                                 HBox([self._color_selector,
                                       self._color_button],
                                      layout=Layout(margin="1px 2px "
                                                    + "1px auto")),
                                 HBox([Label(value='⌀',
                                             layout={'margin': ('auto '
                                                                '2px auto 0px')
                                                     }),
                                       self._vertex_radius_box,
                                       self._radius_button],
                                      layout=Layout(margin=('1px 2px '
                                                            '1px auto'))),
                                 self._vertex_label_toggle,
                                 self._edge_label_toggle,
                                 self._vertex_label_box,
                                 self._set_vertex_label_button,
                                 self._edge_label_box,
                                 self._set_edge_label_button],
                                  layout=Layout(min_width='160px',
                                                width="160px"))
                             ], layout=Layout(width='100%',
                                              height='auto',
                                              overflow='auto hidden'))

        # Prepare the graph data

        # Radii, positions and colors of the vertices or edges on the drawing
        self._vertex_radii = dict()
        self._vertex_colors = dict()

        for v in self.graph.vertex_iterator():
            self.set_vertex_radius(v,
                                   self._drawing_param['default_radius'])
            c = self._drawing_param['default_vertex_color']
            if c is None:
                c = f"#{randrange(0x1000000):06x}"    # Random color
            self.set_vertex_color(v, c)

        self._edge_colors = dict()
        c = self._drawing_param['default_edge_color']
        for e in self.graph.edge_iterator(labels=False):
            self.set_edge_color(e, c)

        if self.graph.get_pos() is None:
            # The graph has no predefined positions: we pick some
            self.graph.layout(layout='spring', save_pos=True)

        # Rescale the coordinates so that the graph fits well in the canvas
        self._normalize_layout()

        self.refresh()

    def show(self):
        """
        Return the editor widget.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: w = ed.show()
            sage: type(w)
            <class 'ipywidgets.widgets.widget_box.HBox'>
        """
        self.refresh()
        return self._widget

    # Getters and setters

    def get_graph(self):
        """
        Return a copy of the drawn graph.

        EXAMPLES:

        The returned graph is different from that of the editor::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph())
            sage: g = ed.get_graph()
            sage: g.delete_vertex(0)
            sage: (len(g), len(ed.graph))
            (9, 10)
        """
        return copy(self.graph)
    @staticmethod
    def get_vertex_label(v):
        """Return the label of a vertex.

        INPUT:

        - `v` -- vertex; the vertex of which we want to know the label.

        OUTPUT:

        A string, that will be printed on ``v``'s shape if
        `self._drawing_param['show_vertex_labels']` is `True`.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph())
            sage: v = ed.graph.random_vertex()
            sage: isinstance(ed.get_vertex_label(v), str)
            True
        """

        return str(v)

    def get_vertex_radius(self, v):
        """
        Return the radius of a vertex.

        If the radius of ``v`` has not been set, return the default radius.

        EXAMPLES:

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph(), default_radius=41)
            sage: ed.get_vertex_radius(0)
            41
            sage: ed.set_vertex_radius(0, 42)
            sage: ed.get_vertex_radius(0)
            42
        """
        return self._vertex_radii.get(v,
                                      self._drawing_param['default_radius'])

    def set_vertex_radius(self, v, radius=None):
        """
        Set the radius of a vertex shape.

        If ``radius`` is ``None``, use the radius in the radius box.

        .. WARNING::

            This function does not redraw the graph.

        EXAMPLES::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph(), default_radius=41)
            sage: ed.get_vertex_radius(0)
            41
            sage: ed.set_vertex_radius(0, 42)
            sage: ed.get_vertex_radius(0)
            42

        TESTS::

            sage: ed.set_vertex_radius(0)
            sage: ed.get_vertex_radius(0) == ed._vertex_radius_box.value
            True
        """
        if radius is None:
            self._vertex_radii[v] = self._vertex_radius_box.value
        else:
            # Casting to int to avoid Sage Integers
            self._vertex_radii[v] = int(radius)

    def get_vertex_color(self, v):
        """
        Get the color of a vertex.

        INPUT:

        - `v` -- vertex; the vertex of which we want to know the color.

        OUTPUT:

        `v`'s color.

        EXAMPLES:

        We color a vertex and ask for its color::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed.set_vertex_color(0, 'blue')
            sage: ed.get_vertex_color(0)
            'blue'

            sage: ed.set_vertex_color(0, '#fff')
            sage: ed.get_vertex_color(0)
            '#fff'

        """
        return self._vertex_colors[v]

    def set_vertex_color(self, v, color=None):
        """
        Set the color of a vertex.

        If ``color`` is ``None``, use the color of the color selector.

        INPUT:

        - ``v`` -- vertex; the vertex to color;
        - ``color`` -- color (default: ``None``); the new color for ``v``.

        OUTPUT:

        No output. Only a side effect: set the color of ``v`` to ``color`` if
        it is not ``None``, or to the color of the color selector otherwise.

        .. WARNING:: This function does not redraw the graph.

        EXAMPLES:

        Colors can be given as named colors or hex values::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed.set_vertex_color(0, 'blue')
            sage: ed.get_vertex_color(0)
            'blue'
            sage: ed.set_vertex_color(0, '#fff')
            sage: ed.get_vertex_color(0)
            '#fff'

        TESTS::

            sage: ed = GraphEditor(Graph(1))
            sage: ed.set_vertex_color(0)
            sage: ed.get_vertex_color(0) == ed._color_selector.value
            True
        """
        if color is None:
            self._vertex_colors[v] = self._color_selector.value
        else:
            self._vertex_colors[v] = color

    def get_edge_color(self, e):
        """
        Return the color of an edge.

        INPUT:

        - ``e`` -- edge; the edge in question;

        OUTPUT:

        The color of ``e``.

        EXAMPLES:

        Edge colors for undirected graphs::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph())
            sage: ed.set_edge_color((1, 6), '#123456')
            sage: ed.get_edge_color((1, 6))
            '#123456'
            sage: ed.get_edge_color((6, 1))
            '#123456'
            sage: ed.get_edge_color((6, 1, 'label'))
            '#123456'
            sage: ed.get_edge_color((5, 9))
            Traceback (most recent call last):
            ...
            KeyError: (5, 9)

        Edge colors for directed graphs::

            sage: ed = GraphEditor(digraphs.Circuit(4))
            sage: ed.set_edge_color((0, 1), '#123456')
            sage: ed.get_edge_color((0, 1))
            '#123456'
            sage: ed.get_edge_color((1, 0))
            Traceback (most recent call last):
            ...
            KeyError: (1, 0)
        """

        u, v, *_ = e

        if self.graph.is_directed():
            return self._edge_colors[(u, v)]

        if (v, u) in self._edge_colors:
            return self._edge_colors[(v, u)]
        else:
            return self._edge_colors[(u, v)]

    def set_edge_color(self, e, color=None):
        """
        Set the color of an edge.

        INPUT:

        - ``e`` -- edge; the edge to color;
        - ``color`` -- color (default: ``None``); the new color for ``e``.

        OUTPUT:

        No output. Only a side effect: set the color of ``e`` to ``color`` if
        it is not ``None``, or to the color of the color selector otherwise.

        Raise an exception if the edge does not belong to the graph.
        See :meth:`get_edge_color` for examples.

        .. WARNING:: this function does not redraw the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: P = graphs.PetersenGraph()
            sage: ed = GraphEditor(P, default_edge_color='pink')
            sage: ed.set_edge_color((1, 6))
            sage: ed.get_edge_color((1,6)) == 'pink'
            True
            sage: ed.set_edge_color((1,5))
            Traceback (most recent call last):
            ...
            ValueError: edge (1, 5) does not belong to the graph
        """

        u, v, *_ = e
        if color is None:
            color = self._drawing_param['default_edge_color']

        if not self.graph.has_edge(e):
            raise ValueError("edge "
                             + str(e)
                             + " does not belong to the graph")

        if self.graph.is_directed():
            self._edge_colors[(u, v)] = color
        elif (u, v) in self._edge_colors.keys():
            self._edge_colors[(u, v)] = color
        else:
            self._edge_colors[(v, u)] = color

    def get_vertex_pos(self, v):
        """
        Return the vertex coordinates.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed.set_vertex_pos(0, 24, 42)
            sage: x, y = ed.get_vertex_pos(0)
            sage: x == 24 and y == 42
            True
        """
        x, y = self.graph.get_pos()[v]
        # -y because the y axis of the canvas goes downwards
        return x, -y

    def get_vertices_pos(self):
        """
        Return the vertices coordinates dictionary.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(10))
            sage: p = ed.get_vertices_pos()
            sage: all(v in p.keys() for v in ed.graph)
            True
        """
        p = self.graph.get_pos()
        # -p[v][1] because the y axis of the canvas goes downwards
        return {v: (p[v][0], -p[v][1])
                for v in self.graph}

    def set_vertex_pos(self, v, x, y):
        """
        Set the position of a vertex.

        INPUT:

        - ``v`` -- vertex; the vertex that needs to have its position set.
        - ``x``, ``y`` -- integers; the coordinates on the canvas for ``v``.

        OUTPUT:

        No output. Only a side effect: the coordinates ``x`` and ``y`` are stored
        in the graph position dictionary.

        .. WARNING::

            This function does not redraw the graph.

        TESTS::

        Same as in :meth:`get_vertex_pos`.

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed.set_vertex_pos(0, 24, 42)
            sage: x, y = ed.get_vertex_pos(0)
            sage: x == 24 and y == 42
            True
        """
        self.set_vertices_pos({v: (int(x), int(y))})

    def set_vertices_pos(self, new_pos):
        """
        Set the position of some vertices.

        INPUT:

        - ``new_pos`` -- dictionary; the dictionary of the new positions,
          indexed by vertices.

        OUTPUT:

        No output. Only a side effect: the coordinates are updated with
        values contained in ``new_pos``.

        .. WARNING::
            This function does not redraw the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PathGraph(3))
            sage: ed.set_vertices_pos({0:(10, 10), 1:(20, 20), 2:(30, 5)})
            sage: ed.graph.get_pos()
            {0: (10, -10), 1: (20, -20), 2: (30, -5)}
        """

        pos = self.graph.get_pos()
        if pos is None:
            pos = dict()
            self.graph.set_pos(pos)

        for v in new_pos.keys():
            # -new_pos[v][1] because the y axis of the canvas goes downwards
            pos[v] = (new_pos[v][0],
                      -new_pos[v][1])

    def _get_vertex_at(self, x, y):
        """
        Return which vertex is drawn at (x,y).

        INPUT:

        - `x`, `y` -- integers; coordinates on the canvas.

        OUTPUT:

        A vertex whose shape contains `(x,y)` and whose center is the
        closest to `(x,y)`. If this does not exists, the returned
        value is ``None``.

        EXAMPLES:

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2), default_radius=20)
            sage: ed.set_vertex_pos(0, 50, 50)
            sage: ed.set_vertex_pos(1, 70, 50)
            sage: ed._get_vertex_at(55, 50)
            0
            sage: ed._get_vertex_at(65, 50)
            1
            sage: ed._get_vertex_at(60, 25) is None
            True
        """

        canvas_pos = self.get_vertices_pos()

        min_dist = self._drawing_param['width']  # aka infinity
        arg_min = None

        for v in self.graph.vertex_iterator():
            v_x, v_y = canvas_pos[v]
            radius = self.get_vertex_radius(v)

            d_x = abs(x - v_x)
            d_y = abs(y - v_y)
            if (d_x < radius and d_y < radius):
                # The user clicked close to vertex v (approximately)!
                d = sqrt(d_x*d_x + d_y*d_y)
                if d <= radius and d < min_dist:
                    min_dist = d
                    arg_min = v

        return arg_min

    def _get_edge_at(self, x, y):
        """
        Return the closest edge near the point with coordinates (x,y).

        Return ``None`` if no edge is close enough to (x,y).

        INPUT:

        - `x`, `y` -- integers; coordinates on the canvas.

        OUTPUT:

        An edge that run close enough from `(x, y)` and minimizes the
        distance to this point. If this does not exists, the returned
        value is ``None``.


        .. WARNING::
            This function assumes that edges are straigh lines between
            their endpoints.

        EXAMPLES:

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PathGraph(3))
            sage: ed.set_vertex_pos(0, 50, 50)
            sage: ed.set_vertex_pos(1, 50, 100)
            sage: ed.set_vertex_pos(2, 100, 100)
            sage: ed.set_vertex_pos(3, 100, 50)
            sage: ed._get_edge_at(50, 75)
            (0, 1)
            sage: ed._get_edge_at(51, 75)
            (0, 1)
            sage: ed._get_edge_at(75, 100)
            (1, 2)
            sage: ed._get_edge_at(60, 98)
            (1, 2)
        """

        def sqnorm(a, b):
            # Square of the norm
            # (to avoid computing square roots)
            d = [a[0] - b[0], a[1] - b[1]]
            return d[0] * d[0] + d[1] * d[1]

        canvas_pos = self.get_vertices_pos()

        min_dist = 10  # We don't want edges too far from the click
        closest_edge = None

        p = vector([x, y])

        for e in self.graph.edge_iterator():
            u, v, *_ = e

            pv = vector(canvas_pos[v])
            pu = vector(canvas_pos[u])

            if (x < min(pv[0], pu[0]) - 10 or
                    x > max(pv[0], pu[0]) + 10 or
                    y < min(pv[1], pu[1]) - 10 or
                    y > max(pv[1], pu[1]) + 10):
                # In the expression above it is important to keep slack
                # (10) in order to deal with horizontal or vertical edges
                continue

            t = (p - pv).dot_product(pu - pv) / sqnorm(pv, pu)
            proj = pv + t * (pu - pv)
            d = sqnorm(proj, p)
            if d < min_dist:
                min_dist = d
                if self.graph.has_edge(u, v):
                    # Case distinction to deal with digraphs
                    closest_edge = (u, v)
                else:
                    closest_edge = (v, u)
        return closest_edge

    ##########
    # Layout #
    ##########

    def _random_layout(self):
        """
        Randomly pick and set positions for the vertices.

        Coordinates are integers chosen between 0 and the square of the
        order of the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PathGraph(3))
            sage: ed._random_layout()
            sage: x, y = ed.get_vertex_pos(1)
            sage: x >= 0 and x <= 9 and y >= 0 and y <= 9
            True
        """
        n = self.graph.order()
        n2 = n*n
        rnd_pos = {v: (randint(0, n2),
                       randint(0, n2))
                   for v in self.graph.vertex_iterator()}
        self.set_vertices_pos(rnd_pos)

    def _normalize_layout(self):
        """
        Shift, rescale and cast the coordinate so that they fill the canvas.

        ``x`` and ``y`` coordinates are scaled by the same factor and
        the graph is centered.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(5), width=501, height=501)
            sage: ed.set_vertex_pos(0, 10, 10)
            sage: ed.set_vertex_pos(1, 5, 10)
            sage: ed.set_vertex_pos(2, 15, 10)
            sage: ed.set_vertex_pos(3, 10, 8)
            sage: ed.set_vertex_pos(4, 10, 12)
            sage: ed._normalize_layout()
            sage: d = ed.get_vertices_pos()
            sage: d[0] == (250, 250)
            True
            sage: d[1][0] <= 25
            True
            sage: d[3][1] >= 150
            True
        """

        if not self.graph:
            # There is nothing to do with the one empty graph
            return

        pos = self.get_vertices_pos()

        # Extrema for vertex centers
        x_min = min(pos[v][0] for v in self.graph)
        x_max = max(pos[v][0] for v in self.graph)
        y_min = min(pos[v][1] for v in self.graph)
        y_max = max(pos[v][1] for v in self.graph)

        x_range = max(x_max - x_min, 0.1)  # max to avoid division by 0
        y_range = max(y_max - y_min, 0.1)

        # Margin to keep on the sides
        margin = max((self.get_vertex_radius(v)
                      for v in self.graph.vertex_iterator())) + 5

        target_width = self._multi_canvas.width - 2 * margin
        target_height = self._multi_canvas.height - 2 * margin
        # Some computations to decide of the scaling factor in order to
        # simultaneously fill the canvas on at least one axis range and
        # keep proportions, and to center the image
        factor_x = target_width / x_range
        factor_y = target_height / y_range

        factor = min(factor_x, factor_y)
        x_shift = margin + (target_width - x_range * factor) / 2
        y_shift = margin + (target_height - y_range * factor) / 2

        new_pos = dict()
        for v in self.graph:
            x, y = pos[v]

            # y-coordinate has a special treatment because on the
            # canvas the y-axis is oriented downwards
            new_pos[v] = (int(x_shift + factor * (x - x_min)),
                          int(y_shift + factor * (y - y_min)))
#            new_pos[v] = (int(x_shift + factor * (x - x_min)),
#                          int(self._multi_canvas.height
#                              - (y_shift + factor * (y - y_min))))

        self.set_vertices_pos(new_pos)

    def _scale_layout(self, ratio):
        """
        Rescale the vertices coordinates around the center of the image
        and with respect to the given ratio.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(5), width=101, height=101)
            sage: ed.set_vertex_pos(0, 50, 50)
            sage: ed.set_vertex_pos(1, 30, 50)
            sage: ed.set_vertex_pos(2, 70, 50)
            sage: ed.set_vertex_pos(3, 50, 30)
            sage: ed.set_vertex_pos(4, 50, 70)
            sage: ed._scale_layout(1.5)
            sage: x, y = ed.get_vertex_pos(0)
            sage: abs(x - 50) <= 1 and abs(y - 50) <= 1
            True
            sage: ed.get_vertex_pos(1)[0] <= 21
            True
            sage: abs(ed.get_vertex_pos(1)[1] - 50) <= 1
            True
        """

        x_shift = self._multi_canvas.width * (1 - ratio) / 2
        y_shift = self._multi_canvas.height * (1 - ratio) / 2

        pos = self.get_vertices_pos()

        new_pos = dict()
        for v in self.graph:
            x, y = pos[v]
            new_pos[v] = (int(x_shift + x * ratio),
                          int(y_shift + y * ratio))

        self.set_vertices_pos(new_pos)

    def _translate_layout(self, vec):
        """
        Translate the vertices coordinates.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed.set_vertex_pos(0, 50, 50)
            sage: ed._translate_layout((25, 25))
            sage: x, y = ed.get_vertex_pos(0)
            sage: abs(x - 75) + abs(y - 75) <= 2
            True
        """

        x_shift, y_shift = vec

        pos = self.get_vertices_pos()

        new_pos = dict()
        for v in self.graph:
            x, y = pos[v]
            new_pos[v] = (int(x + x_shift), int(y + y_shift))

        self.set_vertices_pos(new_pos)

    #########################
    # Text output functions #
    #########################

    def output_text(self, text):
        """
        Write the input string in the textbox of the editor.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed.output_text("Hello world!")
            sage: ed._text_output.value == "Hello world!"
            True
        """

        self._text_output.value = text

    def _text_graph_update(self):
        """Update the caption with data about the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PetersenGraph())
            sage: print(ed._text_graph.value)
            Graph on 10 vertices and 15 edges.
            sage: ed.graph.add_vertex(42)
            sage: ed._text_graph_update()
            sage: print(ed._text_graph.value)
            Graph on 11 vertices and 15 edges.
        """

        self._text_graph.value = ("Graph on " + str(self.graph.order())
                                  + " vertices and "
                                  + str(self.graph.num_edges())
                                  + " edges.")

    ######################
    # Graph modification #
    ######################

    def _add_vertex_at(self, x, y, name=None, color=None):
        """
        Add a vertex to a given position, color it and draw it.

        If ``color`` is ``None``, use the current color of the color
        picker.
        The return value is the same as with
        :meth:`~GenericGraph.add_vertex`. from `~GenericGraph`.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(0))
            sage: ed._add_vertex_at(10, 42, name="vert", color='#112233')
            sage: v=next(ed.graph.vertex_iterator())
            sage: v
            'vert'
            sage: ed.get_vertex_pos(v)
            (10, 42)
            sage: ed.get_vertex_color(v)
            '#112233'
            sage: ed._add_vertex_at(20, 20)
            0
        """

        if name is None:
            name = self.graph.add_vertex()
            return_name = True
        else:
            self.graph.add_vertex(name)
            return_name = False

        self.set_vertex_pos(name, x, y)
        self.set_vertex_color(name, color)
        self.set_vertex_radius(name)

        self._draw_vertex(name)
        self._text_graph_update()

        # Return the vertex name if it was not specified,
        # as the graph add_vertex function:
        if return_name:
            return name

    def _add_edge(self, u, v, label=None, color=None):
        """
        Add an edge between two vertices and draw it

        If ``color`` is ``None``, use the current color of the color
        picker.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed.graph.has_edge(0, 1)
            False
            sage: ed._add_edge(0, 1, color='#112233'); ed.graph.has_edge(0, 1)
            True
            sage: ed.get_edge_color((0, 1))
            '#112233'
        """
        self.graph.add_edge((u, v, label))
        self.set_edge_color((u, v), color)
        self._draw_edge((u, v, label))
        self._text_graph_update()

    #####################
    # Drawing functions #
    #####################

    def _draw_vertex(self, v, canvas=None, color=None, highlight=True):
        """
        Draw the shape of a vertex.

        Also write the vertex name.
        The position is given by
        :meth:`~GraphEditor.get_vertex_pos`.
        If ``canvas`` is ``None``, the default drawing canvas
        (``self._canvas``) is used.
        If ``color`` is ``None`` the color is as given by
        :meth:`~GraphEditor.`get_vertex_color`.
        If ``highlight`` is true, also draw the focus on ``v``.

        TESTS::

        A dummy test, for this drawing function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(1))
            sage: ed._draw_vertex(0)
        """

        if canvas is None:
            canvas = self._v_canvas
        if color is None:
            color = self.get_vertex_color(v)

        x, y = self.get_vertex_pos(v)
        radius = self.get_vertex_radius(v)

        # The inside of the node
        canvas.fill_style = color
        canvas.fill_arc(x, y, radius, 0, 2*pi)

        # The border
        canvas.line_width = 2
        canvas.stroke_style = 'black'
        canvas.stroke_arc(x, y, radius, 0, 2*pi)

        if self._vertex_label_toggle.value:
            # The vertex name
            canvas.font = '20px sans'
            canvas.text_align = 'center'
            canvas.text_baseline = 'middle'
            canvas.fill_style = 'black'
            canvas.fill_text(self.get_vertex_label(v), x, y, max_width=2*radius)

        if highlight and v in self._selected_vertices:
            # Draw the focus
            canvas.stroke_style = 'white'
            canvas.set_line_dash([4, 4])
            canvas.stroke_arc(x, y, radius, 0, 2*pi)
            canvas.set_line_dash([])

    def _draw_incident_edges(self, v, canvas=None):
        """
        Draw the edges incident to a vertex.

        TESTS::

        A dummy test, for this drawing function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.CompleteGraph(2))
            sage: ed._draw_incident_edges(0)
        """
        if canvas is None:
            canvas = self._e_canvas

        # Below We use ignore_direction=True to get all edges incident to a
        # vertex in the case where self.graph is directed
        for e in self.graph.edge_iterator(v, ignore_direction=True):
            self._draw_edge(e, canvas=canvas)

    def _draw_edge(self, e, clear_first=False, canvas=None):
        """
        Draw an edge.

        An arrow is added if the graph is directed.

        INPUT:

        - ``e`` -- edge; of the form (first_end, second_end, label); the
          label is ignored;
        - ``clear_first`` -- Boolean (default: ``False``), whether to
          erase the edge first by drawing a white edge over it;
        - ``canvas`` -- canvas where to draw the edge
          (default: ``None``); with the default value,
          ``self._e_canvas`` is used.

        .. WARNING::

        - The function does not check that ``e`` is an edge of ``self``;

        TESTS::

        A dummy test, for this drawing function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.CompleteGraph(2))
            sage: ed._draw_edge((0,1,'label'))
        """

        u, v, *_ = e
        pos_u = self.get_vertex_pos(u)
        pos_v = self.get_vertex_pos(v)

        if canvas is None:
            canvas = self._e_canvas

        canvas.line_width = 3

        if clear_first:
            canvas.stroke_style = 'white'
            canvas.begin_path()
            canvas.move_to(*pos_u)
            canvas.line_to(*pos_v)
            canvas.stroke()

        canvas.stroke_style = self.get_edge_color((u, v))

        if (u, v) in self._selected_edges or (v, u) in self._selected_edges:
            # If the edge is selected, we draw it dashed
            canvas.set_line_dash([4, 4])

        canvas.begin_path()
        canvas.move_to(*pos_u)
        canvas.line_to(*pos_v)
        canvas.stroke()

        canvas.set_line_dash([])  # Reset dash pattern

        lbl = self.graph.edge_label(u, v)
        if lbl is not None:
            # draw the edge label at the middle of the edge
            pos_uv = [(pos_u[0] + pos_v[0]) / 2, (pos_u[1] + pos_v[1]) / 2]
            canvas.move_to(*pos_uv)
            if self._edge_label_toggle.value:
                # Clear the background
                canvas.fill_style = 'white'
                canvas.fill_arc(*pos_uv, 12, 0, 2*pi)
                # Write the label
                canvas.font = '20px sans'
                canvas.text_align = 'center'
                canvas.text_baseline = 'middle'
                canvas.fill_style = 'black'
                canvas.fill_text(str(lbl), *pos_uv)

        if self.graph.is_directed():
            # If the graph is directed, we also have to draw the arrow
            # tip; We draw it at the end of the edge (as usual)
            radius_v = self.get_vertex_radius(v)
            dist_min = radius_v + self.get_vertex_radius(u)

            # We only do it if the vertex shapes do not overlap.
            if (abs(pos_u[0] - pos_v[0]) > dist_min
                    or abs(pos_u[1] - pos_v[1]) > dist_min):
                canvas.save()
                # Move the canvas so that v lies at (0,0) and
                # rotate it so that v-y is on the x>0 axis:
                canvas.translate(*pos_v)
                canvas.rotate(float(atan2(pos_u[1] - pos_v[1],
                                          pos_u[0] - pos_v[0])))
                # Move to the point where the edge joins v's shape and
                # draw the arrow there:
                canvas.translate(radius_v, 0)
                canvas.fill_style = self.get_edge_color((u, v))
                GraphEditor._draw_arrow(canvas)
                canvas.restore()

    def refresh(self):
        """
        Redraw the whole graph and update the text info.

        Clear the drawing canvasses (``self._e_canvas`` and
        ``self._v_canvas``) and draw the whole graph on it.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: ed.refresh() is None
            True
        """
        self._text_graph_update()
        with hold_canvas():
            self._e_canvas.clear()
            for e in self.graph.edge_iterator():
                self._draw_edge(e)

            self._v_canvas.clear()
            for v in self.graph.vertex_iterator():
                self._draw_vertex(v, highlight=True)

    def _select_vertex(self, vertex=None, redraw=True):
        """
        Add or remove a vertex from the set of selected vertices.

        INPUT:

        - `vertex` -- vertex (default: ``None``); the vertex to be
          (un)selected; if `vertex` is ``None`` then the set of selected
          vertices is emptied;
        - `redraw` -- Boolean (default: `True`); when True, redraw `vertex`,
          otherwise does not change the drawing (useful when the graph is going
          to be fully redrawn afterwards anyway).

        OUTPUT:

        No output. Only side effects:

        - if `vertex` is ``None`` then the set `self._selected_vertices` is
          empied; otherwise `vertex` is added (if not already present) or
          removed (otherwise) in `self._selected_vertices`.
        - if `redraw` is `True`, `vertex` is redrawn, with or without the
          selection focus depending on whether it was selected or unselected.

        .. WARNING::

        No check is done that `vertex` indeed is a vertex of the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: 0 in ed._selected_vertices
            False
            sage: ed._select_vertex(0, redraw=False)
            sage: ed._select_vertex(1, redraw=False)
            sage: 0 in ed._selected_vertices
            True
            sage: ed._select_vertex(0, redraw=False)
            sage: 0 in ed._selected_vertices
            False
            sage: 1 in ed._selected_vertices
            True
            sage: ed._select_vertex(None, redraw=False)
            sage: 1 in ed._selected_vertices
            False
        """

        if vertex is None:
            self._selected_vertices.clear()
            if redraw:
                self.refresh()
            return
        else:
            # Flip selected/unselected state
            try:
                self._selected_vertices.remove(vertex)
                self.output_text("Unselected vertex " +
                                 str(vertex))
            except KeyError:
                self._selected_vertices.add(vertex)
                self.output_text("Selected vertex " +
                                 str(vertex))

            # the radius of the selected vertex becomes the default one
            self._vertex_radius_box.value = (self.get_vertex_radius(vertex))

            if redraw:
                self._draw_vertex(vertex)

    ####################################################
    # Callbacks for mouse action and related functions #
    ####################################################

    def _clean_tools(self):
        """
        Forget that some drawing is taking place.

        This function deletes the `current_clique`, `current_walk_vertex`,
        `current_star_center`, and `current_star_leaf` variables of `self`,
        that store data used when adding a clique, a walk or a star to the
        graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(0))
            sage: attrs = ['_current_clique', '_current_walk_vertex']
            sage: attrs.extend(['_current_star_center', '_current_star_leaf'])
            sage: for attr in attrs: setattr(ed, attr, 42)
            sage: ed._clean_tools()
            sage: any((hasattr(ed, a) for a in attrs))
            False
        """
        attrs = ['_current_clique',
                 '_current_walk_vertex',
                 '_current_star_center',
                 '_current_star_leaf']

        for attr in attrs:
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    def _mouse_action_select_move(self,
                                  on_vertex, closest_edge,
                                  pixel_x, pixel_y):
        """
        Start moving or (un)selecting a vertex or an edge or moving the
        whole graph.

        This function is called after a (down) click when the current
        tool is 'select / move'.

        INPUT:

        - `on_vertex` -- vertex; the clicked vertex if any, can be ``None``
          otherwise;
        - `closest_edge` -- edge; the clicked edge if any, can be ``None``
          otherwise;
        - `pixel_x` -- integer; the x-coordinate on the canvas of the click;
        - `pixel_y` -- integer; the y-coordinate on the canvas of the click.

        OUTPUT:

        No output. Only side effects:

        - if `on_vertex` is not ``None``, draw this vertex and its neighbors
          on the interact canvas (`self._v_interact_canvas`) and the rest of
          the graph on the main canvas (so that we can move `on_vertex` without
          redrawing the whole graph many times;
        - otherwise, if `closest_edge` is not ``None``, (un)select it;
        - otherwise, the click was done on the canvas: record its position
          in order to later move the drawing when the mouse is moved.

        TESTS::

        A dummy test, for this function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: ed._mouse_action_select_move(None, None, int(10), int(-230))
        """

        if on_vertex is not None:
            # Click was on a vertex
            self._dragged_vertex = on_vertex
            self.output_text("Click on vertex " + str(on_vertex))
            with hold_canvas():

                # On the interact canvas we draw the moved vertex and
                # its incident edges
                self._v_interact_canvas.clear()
                self._e_interact_canvas.clear()
                self._draw_incident_edges(on_vertex,
                                          canvas=self._e_interact_canvas)
                self._draw_vertex(on_vertex, canvas=self._v_interact_canvas)

                # Draw everything else on the main canvas
                self._e_canvas.clear()
                for (u1, u2, label) in self.graph.edge_iterator():
                    if (on_vertex != u1 and on_vertex != u2):
                        self._draw_edge((u1, u2, label))
                self._v_canvas.clear()
                for u in self.graph.vertex_iterator():
                    if u != on_vertex:
                        self._draw_vertex(u)

        elif closest_edge is not None:
            # Click was not on a vertex but near an edge
            if closest_edge in self._selected_edges:
                self._selected_edges.remove(closest_edge)
            else:
                self._selected_edges.add(closest_edge)
            self._draw_edge(closest_edge, clear_first=True)
        else:
            # The click was neither on a vertex nor on an edge
            self._dragging_canvas_from = [pixel_x, pixel_y]
            return

    def _mouse_action_add_ve(self, on_vertex, pixel_x, pixel_y):
        """
        Add a vertex or an edge.

        This function is called after a down click is done and the current
        tool is "add vertex or edge".

        INPUT:

        - ``on_vertex`` -- vertex; the clicked vertex, if any;
        - ``pixel_x`` -- integer; the x-coordinate on the canvas of the click;
        - ``pixel_y`` -- integer; the y-coordinate on the canvas of the click.

        OUTPUT:

        No output. Only side effects:

        - if the click is not on a vertex (i.e. ``on_vertex`` is ``None``) and
          there is a selected vertex : empty the set of selected vertices;
        - if the click is not on a vertex and there is no selected vertex: add
          a new vertex at the clicked position;
        - if the click is on a vertex ``v``, that is selected: unselect ``v``;
        - if the click is on an unselected vertex ``v`` and there is a selected
          vertex ``u``: add the edge ``uv``;
        - if the click is on a vertex ``v`` and there is no selected
          vertex: select ``v``.

        In all cases redraw the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._mouse_action_add_ve(0, 0, 0)
            sage: ed._selected_vertices
            {0}
            sage: ed._mouse_action_add_ve(None, 0, 0)
            sage: ed._selected_vertices
            set()

            sage: ed._mouse_action_add_ve(0, 0, 0)
            sage: ed._mouse_action_add_ve(1, 0, 0)
            sage: ed.graph.has_edge(0, 1)
            True
            sage: ed._selected_vertices
            set()

            sage: ed._mouse_action_add_ve(None, 20, 20)
            sage: len(ed.graph)
            3
        """
        if on_vertex is not None:
            # The click is done on an existing vertex

            if len(self._selected_vertices) == 0:
                # No vertex was selected: select the clicked vertex
                self._select_vertex(on_vertex)
            else:
                if on_vertex in self._selected_vertices:
                    # The click is done on the selected vertex
                    self._select_vertex()  # Unselect
                    return

                if len(self._selected_vertices) > 1:
                    raise ValueError

                selected_iterator = (v for v in self._selected_vertices)
                only_selected_vertex = next(selected_iterator)

                # A single vertex was selected and we clicked on a new
                # one: we link it to the previously selected vertex
                self._add_edge(only_selected_vertex, on_vertex)
                self._select_vertex()  # Unselect
                self.output_text("Added edge from " +
                                 str(only_selected_vertex) +
                                 " to " + str(on_vertex))
        else:
            # The click is not done on an existing vertex

            self.output_text("Click was not on a vertex")
            if len(self._selected_vertices):
                # If a vertex is selected and we click on the
                # background, we un-select it:
                self._selected_vertices.clear()
            else:
                # Otherwise, we add a new vertex
                self._add_vertex_at(pixel_x, pixel_y)
        self.refresh()

    def _mouse_action_del_ve(self, on_vertex, on_edge):
        """
        Delete a vertex or an edge.

        This function is called after a down click is done and the current
        tool is "delete vertex or edge".

        INPUT:

        - ``on_vertex`` -- vertex; the clicked vertex, if any;
        - ``on_edge`` -- edge; the clicked edge, if any;

        OUTPUT:

        No output. Only side effects:

        - if ``on_vertex`` is not ``None``, delete this vertex;
        - otherwise, of ``on_edge`` is not ``None``, delete this edge;

        In both cases redraw the graph.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.PathGraph(3))
            sage: ed._mouse_action_del_ve(2, None)
            sage: len(ed.graph)
            2
            sage: ed._mouse_action_del_ve(None, (0, 1))
            sage: ed.graph.num_edges()
            0
        """

        if on_vertex is not None:
            self.graph.delete_vertex(on_vertex)
        elif on_edge is not None:
            self.graph.delete_edge(on_edge)
        else:
            return
        self.refresh()

    def _mouse_action_add_clique(self, clicked_node, pixel_x, pixel_y):
        """
        Add a vertex to the current clique.

        This function is called after a down click is done and the current
        tool is "add clique". It adds a vertex (new or existing) to the clique
        that is being constructed.

        INPUT:

        - ``clicked_node`` -- vertex; the clicked vertex, if any;
        - ``pixel_x``, ``pixel_y`` -- integers; the coordinates of the click,
          relevant only if ``clicked_node`` is ``None`` (new vertex to be
          added).

        OUTPUT:

        No output. Only side effects:

        - if ``clicked_node`` is ``None``, add a new vertex at
          ``(pixel_x, pixel_y)``;
        - if ``clicked_node`` is a vertex of the current clique,
          delete ``self._current_clique``: the construction of this
          clique is done.
        - otherwise, add ``clicked_node`` to ``self._current_clique``
          and add edges to all other vertices of this set.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._mouse_action_add_clique(0, 0, 0) # add 0
            sage: ed._mouse_action_add_clique(1, 0, 0) # add 1
            sage: ed._mouse_action_add_clique(None, 20, 20) # add a new vertex
            sage: G = ed.graph
            sage: u, v, w = G.vertices()
            sage: G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(w, u)
            True
        """

        if clicked_node is None:
            # Click on the canvas: we add a vertex
            clicked_node = self._add_vertex_at(pixel_x, pixel_y)

        if not hasattr(self, '_current_clique'):
            self._current_clique = [clicked_node]
            return
        if clicked_node in self._current_clique:
            self.output_text("Done constructing clique")
            del self._current_clique
            return

        for u in self._current_clique:
            self._add_edge(clicked_node, u)
        self._current_clique.append(clicked_node)

    def _mouse_action_add_walk(self, clicked_node, pixel_x, pixel_y):
        """
        Add a vertex to the current walk.

        This function is called after a down click is done and the current
        tool is "add walk". It adds a vertex (new or existing) to the walk
        that is being constructed.

        INPUT:

        - ``clicked_node`` -- vertex; the clicked vertex, if any;
        - ``pixel_x``, ``pixel_y`` -- integers; the coordinates of the click;

        OUTPUT:

        No output. Only side effects:

        - if ``clicked_node`` is ``None``, add a new vertex at
          ``(pixel_x, pixel_y)`` and call it ``clicked_node``.

        Then:

        - if there is no current walk (i.e. ``self._current_walk_vertex`` does
          not exist), start a new walk with ``clicked_node``;
        - if there is a current walk and ``clicked_node`` is the last
          vertex of it (i.e. it is ``self._current_walk_vertex``), then end
          the construction of the current walk, that is, delete
          ``self._current_walk_vertex``;
        - otherwise add an edge from the last vertex of the walk to
          ``clicked_node`` and set ``self._current_walk_vertex`` to
          ``clicked_node``.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: hasattr(ed, '_current_walk_vertex')
            False
            sage: ed._mouse_action_add_walk(0, 0, 0)
            sage: ed._current_walk_vertex
            0
            sage: ed._mouse_action_add_walk(None, 20, 20)
            sage: ed._mouse_action_add_walk(1, 0, 0)
            sage: ed._current_walk_vertex
            1
            sage: ed._mouse_action_add_walk(1, 0, 0)
            sage: hasattr(ed, '_current_walk_vertex')
            False
            sage: ed.graph.num_edges()
            2
        """

        if clicked_node is None:
            # Click on the canvas: we add a vertex
            clicked_node = self._add_vertex_at(pixel_x, pixel_y)

        if not hasattr(self, '_current_walk_vertex'):
            # The clicked vertex is the first vertex of the walk
            self.output_text("Constructing a walk - "
                             "click on the last vertex when you are done.")
            self._current_walk_vertex = clicked_node
            self._select_vertex(clicked_node)  # Select and redraw
            self._text_graph_update()
            return

        if clicked_node == self._current_walk_vertex:
            self.output_text("Done constructing walk")
            del self._current_walk_vertex
            self._select_vertex(clicked_node, redraw=False)  # Select
            self.refresh()
            return

        self._add_edge(self._current_walk_vertex, clicked_node)
        self._select_vertex(self._current_walk_vertex)  # Unselect&redraw
        self._select_vertex(clicked_node)  # Select & redraw
        self._current_walk_vertex = clicked_node

    def _mouse_action_add_star(self, clicked_node, click_x, click_y):
        """
        Start or continue the drawing of a star.

        If no star is being drawn, start drawing a star with `clicked_node`
        as center. Otherwise, add `clicked_node` as leaf to the star that is
        being drawn.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._mouse_action_add_star(None, 10, 10)
            sage: ed._current_star_center
            2
            sage: ed._mouse_action_add_star(None, 10, 10)
            sage: ed._mouse_action_add_star(0, 10, 10)
            sage: ed._mouse_action_add_star(1, 10, 10)
            sage: ed.graph.has_edge(2, 3) and ed.graph.has_edge(2, 0)
            True
            sage: ed._mouse_action_add_star(2, 10, 10)
            sage: hasattr(ed, '_current_star_center')
            False
        """

        if clicked_node is None:
            # Click on the canvas: we add a vertex
            clicked_node = self._add_vertex_at(click_x, click_y)

        if not hasattr(self, '_current_star_center'):
            # We start drawing a star from the center
            self._current_star_center = clicked_node
            self._current_star_leaf = clicked_node
            self._select_vertex(clicked_node)
            self.output_text('Star with center ' +
                             str(self._current_star_center) +
                             ': click on the leaves')
        elif (clicked_node == self._current_star_center or
                clicked_node == self._current_star_leaf):
            # We are done drawing a star
            self.output_text("Done drawing star")
            del self._current_star_center
            del self._current_star_leaf
            self._select_vertex(redraw=False)
            self.refresh()
        else:
            # We are drawing a star
            self._current_star_leaf = clicked_node
            self._add_edge(self._current_star_center,
                           self._current_star_leaf)
            self.output_text('Star with center ' +
                             str(self._current_star_center) +
                             ': click on the leaves')

    def _mouse_down_handler(self, click_x, click_y):
        """
        Callback for mouse (down) clicks.

        This function is called when a down click is done on the canvas.
        Depending on the current tool in use, call the appropriate function.


        INPUT:
        - ``click_x``, ``click_y`` -- integers;
          the coordinates of the click.

        OUTPUT:

        No output, just a call to the appropriate function.

        TESTS::

        A dummy test, for this function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: ed._mouse_down_handler(10, -230)
        """

        self.initial_click_pos = (click_x, click_y)
        clicked_node = self._get_vertex_at(click_x, click_y)
        closest_edge = None

        if self._current_tool() == 'add vertex or edge':
            return self._mouse_action_add_ve(clicked_node, click_x, click_y)
        if self._current_tool() == 'add walk':
            return self._mouse_action_add_walk(clicked_node, click_x, click_y)
        if self._current_tool() == 'add clique':
            return self._mouse_action_add_clique(clicked_node,
                                                 click_x, click_y)
        if self._current_tool() == 'add star':
            return self._mouse_action_add_star(clicked_node, click_x, click_y)

        if clicked_node is None:
            closest_edge = self._get_edge_at(click_x, click_y)

        if self._current_tool() == 'delete vertex or edge':
            return self._mouse_action_del_ve(clicked_node, closest_edge)
        if self._current_tool() == 'select / move':
            return self._mouse_action_select_move(clicked_node,
                                                  closest_edge,
                                                  click_x,
                                                  click_y)

    def _mouse_move_handler(self, pixel_x, pixel_y):
        """
        Callback for mouse movement.

        This function is called when the mouse is moved.
        Depending on the current tool in use, call the appropriate function.

        INPUT:
        - ``click_x``, ``click_y`` -- integers;
          the coordinates of the mouse.

        OUTPUT:

        No output, just a call to the appropriate function.

        TESTS::

        A dummy test, for this function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: ed._mouse_move_handler(10, -230)
        """
        if self._dragged_vertex is not None:
            # We are dragging a vertex...
            self.output_text("Dragging vertex " + str(self._dragged_vertex))
            v = self._dragged_vertex
            self.set_vertex_pos(v, pixel_x, pixel_y)

            with hold_canvas():
                # We only redraw what changes: the position of the
                # dragged vertex, the edges incident to it and also its
                # neighbors (so that the redrawn edges are not drawn on
                # the neighbors shapes):
                self._e_interact_canvas.clear()
                self._draw_incident_edges(v, canvas=self._e_interact_canvas)
                self._v_interact_canvas.clear()
                self._draw_vertex(v, canvas=self._v_interact_canvas)

        elif self._dragging_canvas_from is not None:
            # We are dragging the canvas
            translation = [pixel_x - self._dragging_canvas_from[0],
                           pixel_y - self._dragging_canvas_from[1]]
            self._translate_layout(translation)
            self._dragging_canvas_from = [pixel_x, pixel_y]
            self.refresh()

    def _mouse_up_handler(self, pixel_x, pixel_y):
        """
        Callback for mouse (up) click.

        This function is called when an up-click is done on the canvas.
        Depending on the current tool in use, call the appropriate function.

        INPUT:
        - ``click_x``, ``click_y`` -- integers;
          the coordinates of the click.

        OUTPUT:

        No output, just a call to the appropriate function.

        TESTS::

        A dummy test, for this function can hardly be tested::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor()
            sage: ed._mouse_up_handler(10, -230)
        """
        if self._dragged_vertex is not None:
            # If we dragged the vertex very close to its initial
            # position, we actually wanted to (un)select it
            if (abs(pixel_x - self.initial_click_pos[0]) < 10
                    and abs(pixel_y - self.initial_click_pos[1]) < 10):
                # (Un)select
                self._select_vertex(self._dragged_vertex, redraw=False)
                with hold_canvas():
                    # We redraw these on the main canvas
                    self._draw_incident_edges(self._dragged_vertex)
                    self._draw_vertex(self._dragged_vertex)
                self._dragged_vertex = None
            else:
                self.output_text("Done dragging vertex.")
                self.refresh()

            self._dragged_vertex = None
            # Should be after _draw_graph to prevent screen flickering:
            self._v_interact_canvas.clear()
            self._e_interact_canvas.clear()

        elif self._dragging_canvas_from is not None:
            # We stop dragging the canvas
            self._dragging_canvas_from = None
            # If we dragged the canvas by very little (or not at all),
            # it was just a click on the canvas to unselect everything
            if (abs(pixel_x - self.initial_click_pos[0]) < 10
                    and abs(pixel_y - self.initial_click_pos[1]) < 10):
                self.output_text("Emptied selection.")
                self._select_vertex(redraw=False)
                self._selected_edges.clear()
                self.refresh()

    ##############################################
    # Callback functions for the widget elements #
    ##############################################

    def _tool_selector_clbk(self):
        """
        Called when changing tools.

        Redraw the graph, unselect selected vertices and clears
        variables used with some tools (when constructing cliques
        for instance).

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._select_vertex(0)
            sage: ed._tool_selector_clbk()
            sage: 0 in ed._selected_vertices
            False
        """
        self._clean_tools()
        self._select_vertex(redraw=False)
        self._selected_edges.clear()
        self.refresh()
        self.output_text('')

    def _layout_selector_clbk(self, change):
        """
        Apply the graph layout given by ``change['new']`` (if any).

        This function is called when the layout selector is used.
        If applying the layout is not possible, an error message is
        written to the text output widget.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(graphs.CompleteGraph(5))
            sage: ed._layout_selector_clbk({'name': 'value', 'new': 'planar'})
            sage: print(ed._text_output.value)
            'planar' layout impossible: the graph is not planar!
        """
        if change['name'] != 'value':
            return
        elif change['new'] == '- change layout -':
            return

        new_layout = change['new']
        self._layout_selector.value = '- change layout -'

        # Interrupt any drawing action that is taking place:
        self._clean_tools()

        self.output_text('Updating layout, please wait...')

        # Handling unreasonable demands
        if new_layout == 'planar' and not self.graph.is_planar():
            self.output_text('\'planar\' layout impossible: '
                             'the graph is not planar!')
            return
        if new_layout == 'acyclic' and not self.graph.is_directed():
            self.output_text('\'directed acyclic\' layout impossible:'
                             ' the graph is not directed!')
            return

        if new_layout == 'random':
            self._random_layout()
        else:
            layout_kw = {'save_pos': True}  # Args for the layout fun

            if (new_layout == 'forest (root up)' or
                    new_layout == 'forest (root down)'):

                # Unreasonable demands again
                if self.graph.is_directed():
                    self.output_text('\'forest\' layout impossible: '
                                     'it is defined only for '
                                     'undirected graphs')
                    return
                if not self.graph.is_forest():
                    self.output_text('\'forest\' layout impossible: '
                                     'the graph is not a forest!')
                    return
                else:
                    # Now we can set the correct parameters
                    # for the forest layout
                    layout_kw['layout'] = 'forest'
                    try:
                        # Pick a selected vertex (if any) as root
                        root = next((v for v in self._selected_vertices))
                        layout_kw['forest_roots'] = [root]
                    except StopIteration:
                        pass
                    if new_layout == 'forest (root up)':
                        layout_kw['tree_orientation'] = 'down'
                    else:
                        layout_kw['tree_orientation'] = 'up'
            else:
                layout_kw['layout'] = new_layout

            # Now parameters are set so we can call the layout function
            self.graph.layout(**layout_kw)

        self._normalize_layout()  # Rescale so that it fits well
        self.refresh()
        self.output_text('Done updating layout.')

    def _color_button_clbk(self):
        """
        Change the color of the selected elements (if any).

        The new color is that of the color wheel:
        ``self._color_selector.value``.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._select_vertex(0)
            sage: ed._color_selector.value = '#420042'
            sage: ed._color_button_clbk()
            sage: ed.get_vertex_color(0)
            '#420042'
        """
        new_color = self._color_selector.value

        for e in self._selected_edges:
            self.set_edge_color(e, new_color)
        for v in self._selected_vertices:
            self.set_vertex_color(v, new_color)
        self.refresh()

    def _radius_button_clbk(self):
        """
        Change the radius of the selected vertices (if any).

        The new radius is that of the radius text box.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: r = ed.get_vertex_radius(0)
            sage: ed._select_vertex(1)
            sage: ed._vertex_radius_box.value = 2*r
            sage: ed._radius_button_clbk()
            sage: ed.get_vertex_radius(1) == 2*r
            True
        """
        r = self._vertex_radius_box.value
        for v in self._selected_vertices:
            self.set_vertex_radius(v, r)
        self.refresh()

    def _clear_drawing_button_clbk(self, _):
        """
        Callback for the ``clear_drawing_button``.

        Replaces the current graph with the empty graph and clears the
        canvas.

        .. WARNING::

            The current drawn graph is lost.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._clear_drawing_button.click()
            sage: len(ed.graph)
            0

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._clear_drawing_button_clbk(42)
            sage: len(ed.graph)
            0
        """
        self.graph = Graph(0)
        self._select_vertex(redraw=None)
        self.refresh()
        self.output_text("Cleared drawing.")

    def _set_vertex_label_button_clbk(self):
        """
        Callback for the ``set_vertex_label_button``.

        Sets the label of the selected vertex to the value of the
        ``vertex_label_box``.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._select_vertex(0)
            sage: ed._vertex_label_box.value = 'a'
            sage: ed._set_vertex_label_button_clbk()
            sage: ed.get_vertex_label(0)
            'a'
        """
        label = self._vertex_label_box.value
        self.dist = {v: self.get_vertex_label(v) for v in self.graph}
        for v in self._selected_vertices:
            self.dist[v] = label
        self.set_vertex_label = lambda v: str(self.dist[v])
        self.refresh()

    def _set_edge_label_button_clbk(self):
        """
        Callback for the ``set_edge_label_button``.

        Sets the label of the selected edge to the value of the
        ``edge_label_box``.

        TESTS::

            sage: from phitigra import GraphEditor
            sage: ed = GraphEditor(Graph(2))
            sage: ed._select_edge((0, 1))
            sage: ed._edge_label_box.value = 'a'
            sage: ed._set_edge_label_button_clbk()
            sage: ed.get_edge_label((0, 1))
            'a'
        """
        label = self._edge_label_box.value
        self.graph.set_edge_label(list(self._selected_vertices)[0], \
            list(self._selected_vertices)[1], label)
        self.refresh()
