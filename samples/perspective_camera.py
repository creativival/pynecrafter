from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

box_vertices = [Point3(1, 0, 1), Point3(-1, 0, 1), Point3(-1, 0, -1), Point3(1, 0, -1)]
box_color = Vec4(1, 1, 1, 0.1)

# line_points = [
#     [Point3(0, 0, 0), Point3(8, 40, 6)],
#     [Point3(0, 0, 0), Point3(8, 40, -6)],
#     [Point3(0, 0, 0), Point3(-8, 40, -6)],
#     [Point3(0, 0, 0), Point3(-8, 40, 6)]
# ]
line_points = [
    [Point3(4, 0, 3), Point3(4, 40, 3)],
    [Point3(4, 0, -3), Point3(4, 40, -3)],
    [Point3(-4, 0, -3), Point3(-4, 40, -3)],
    [Point3(-4, 0, 3), Point3(-4, 40, 3)],
]
line_color = Vec4(1, 1, 1, 1)

axis_points = [
    [Point3(0, 0, 0), Point3(100, 0, 0)],
    [Point3(0, 0, 0), Point3(0, 100, 0)],
    [Point3(0, 0, 0), Point3(0, 0, 100)],
]
axis_colors = [
    Vec4(1, 0, 0, 0.5),
    Vec4(0, 1, 0, 0.5),
    Vec4(0, 0, 1, 0.5),
]


class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        geom_format = GeomVertexFormat.getV3c4()

        # box
        box_geom_data = GeomVertexData("box", geom_format, Geom.UHStatic)
        box_vertex_writer = GeomVertexWriter(box_geom_data, "vertex")
        box_color_writer = GeomVertexWriter(box_geom_data, 'color')

        for pos in box_vertices:
            box_vertex_writer.addData3f(pos)
            box_color_writer.addData4f(box_color)

        geom_triangles = GeomTriangles(Geom.UHStatic)
        geom_triangles.addVertices(0, 1, 2)
        geom_triangles.closePrimitive()
        geom_triangles.addVertices(2, 3, 0)
        geom_triangles.closePrimitive()

        box_geom = Geom(box_geom_data)
        box_geom.addPrimitive(geom_triangles)
        box_node1 = GeomNode("box1")
        box_node1.addGeom(box_geom)
        box_node2 = GeomNode("box2")
        box_node2.addGeom(box_geom)
        box_node3 = GeomNode("box3")
        box_node3.addGeom(box_geom)

        self.near_surface = self.render.attachNewNode(box_node1)
        # self.near_surface.setScale(2, 1, 1.5)
        self.near_surface.setScale(4, 1, 3)
        self.near_surface.setPos(0, 10, 0)
        self.near_surface.setTransparency(TransparencyAttrib.MAlpha)
        self.far_surface = self.render.attachNewNode(box_node2)
        self.far_surface.setScale(4, 1, 3)
        self.far_surface.setPos(0, 20, 0)
        self.far_surface.setTransparency(TransparencyAttrib.MAlpha)
        self.film_surface = self.render.attachNewNode(box_node3)
        self.film_surface.setScale(4, 1, 3)
        self.film_surface.setPos(0, 0, 0)
        self.film_surface.setTransparency(TransparencyAttrib.MAlpha)

        # line
        line_geom_data = GeomVertexData('line', geom_format, Geom.UHDynamic)
        line_vertex_writer = GeomVertexWriter(line_geom_data, 'vertex')
        line_color_writer = GeomVertexWriter(line_geom_data, 'color')
        indies = []

        for i, points in enumerate(line_points):
            line_vertex_writer.addData3f(points[0])
            line_color_writer.addData4f(line_color)
            line_vertex_writer.addData3f(points[1])
            line_color_writer.addData4f(line_color)
            indies.append((i * 2, i * 2 + 1))

        geom_lines = GeomLines(Geom.UHDynamic)
        for index in indies:
            geom_lines.addVertices(*index)
        line_geom = Geom(line_geom_data)
        line_geom.addPrimitive(geom_lines)

        line_geom_node = GeomNode('line')
        line_geom_node.addGeom(line_geom)
        self.four_lines = self.render.attachNewNode(line_geom_node)

        # axis
        axis_geom_data = GeomVertexData('axis', geom_format, Geom.UHDynamic)
        axis_vertex_writer = GeomVertexWriter(axis_geom_data, 'vertex')
        axis_color_writer = GeomVertexWriter(axis_geom_data, 'color')
        indies = []

        for i, points in enumerate(axis_points):
            axis_vertex_writer.addData3f(points[0])
            axis_color_writer.addData4f(axis_colors[i])
            axis_vertex_writer.addData3f(points[1])
            axis_color_writer.addData4f(axis_colors[i])
            indies.append((i * 2, i * 2 + 1))

        geom_lines = GeomLines(Geom.UHDynamic)
        for index in indies:
            geom_lines.addVertices(*index)
        axis_geom = Geom(axis_geom_data)
        axis_geom.addPrimitive(geom_lines)

        axis_geom_node = GeomNode('axis')
        axis_geom_node.addGeom(axis_geom)
        self.axis = self.render.attachNewNode(axis_geom_node)
        self.axis.setTransparency(TransparencyAttrib.MAlpha)

        # camera
        self.camera_model = self.loader.loadModel('models/camera')
        self.camera_model.reparentTo(self.render)

        self.cam.setPos(10, -30, 10)
        self.cam.lookAt(0, 0, 0)


app = Application()
app.run()
