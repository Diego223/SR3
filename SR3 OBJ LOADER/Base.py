#Universidad del Valle de Guatemala
#Graficas por Computadora
#Laboratorio SR3
#Diego Crespo 19541
import struct
from collections import namedtuple
from Loader import Obj

LineV2 = namedtuple('Point2', ['x', 'y'])

def bytec(c):
    return struct.pack('=c', c.encode('ascii'))

def duo(w):
    return struct.pack('=h', w)

def dduo(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


black = color(0, 0, 0)
white = color(1, 1, 1)


class Engine(object):
    def __init__(self, width, height):
        self.pointsColor = white
        self.bgColor = black
        self.newWindow(width, height)

    def Viewport(self, x, y, width, height):
        self.viewX = x
        self.viewY = y
        self.portWidth = width
        self.portHeight = height

    def Clear(self):
        self.pixels = [[ self.bgColor for y in range(self.height)] for x in range(self.width)]

    def newWindow(self, width, height):
        self.width = width
        self.height = height
        self.Clear()
        self.Viewport(0, 0, width, height)
    
    def changeColor(self, r, g, b):
        self.pointsColor = color(r, g, b)

    def bgColor(self, r, g, b):
        self.bgColor = color(r, g, b)

    def Vertex(self, x, y, color = None):
        if x < self.viewX or x >= self.viewX + self.portWidth or y < self.viewY or y >= self.viewY + self.portHeight:
            return

        if (0 < x < self.width) and (0 < y < self.height):
            self.pixels[int(x)][int(y)] = color or self.pointsColor

    def nVertex(self, x, y, color = None):
        x = int( (x + 1) * (self.portWidth / 2) + self.viewX )
        y = int( (y + 1) * (self.portHeight / 2) + self.viewY)
    
        if x < self.viewX or x >= self.viewX + self.portWidth or y < self.viewY or y >= self.viewY + self.portHeight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.pointsColor

    def Line(self, v0, v1, color=None):
        xi = v0.x
        xf = v1.x
        yi = v0.y
        yf = v1.y

        if xi == xf and yi == yf:
            self.Vertex(xi,yf,color)
            return

        dx = abs(xf - xi)
        dy = abs(yf - yi)

        step = dy > dx

        if step:
            xi, yi = yi, xi
            xf, yf = yf, xf

        if xi > xf:
            xi, xf = xf, xi
            yi, yf = yf, yi

        dx = abs(xf - xi)
        dy = abs(yf - yi)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = yi

        for x in range(xi, xf + 1):
            if step:
                self.Vertex(y, x, color)
            else:
                self.Vertex(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if yi < yf else -1
                limit += 1

    def nLine(self, v0, v1, color = None):
        xi = int( (v0.x + 1) * (self.portWidth / 2) + self.viewX)
        xf = int( (v1.x + 1) * (self.portWidth / 2) + self.viewX)
        yi = int( (v0.y + 1) * (self.portHeight / 2) + self.viewY)
        yf = int( (v1.y + 1) * (self.portHeight / 2) + self.viewY)

        dx = abs(xf - xi)
        dy = abs(yf - yi)

        step = dy > dx

        if step:
            xi, yi = yi, xi
            xf, yf = yf, xf

        if xi > xf:
            xi, xf = xf, xi
            yi, yf = yf, yi

        dx = abs(xf - xi)
        dy = abs(yf - yi)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = yi

        for x in range(xi, xf + 1):
            if step:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)
            offset += m
            if offset >= limit:
                y += 1 if yi < yf else -1
                limit += 1

    def loadOBJ(self, filename, translate = LineV2(0.0,0.0), scale = LineV2(1.0,1.0)):

        model = Obj(filename)

        for face in model.faces:
            vertsCount = len(face)

            for v in range(vertsCount):

                indexi = face[v][0] - 1
                indexf = face[(v + 1) % vertsCount][0] - 1

                verti = model.verts[indexi]
                vertf = model.verts[indexf]

                xi = round(verti[0] * scale.x + translate.x)
                yi = round(verti[1] * scale.y + translate.y)
                xf = round(vertf[0] * scale.x + translate.x)
                yf = round(vertf[1] * scale.y + translate.y)

                self.Line(LineV2(xi,yi), LineV2(xf, yf))

    #crea archivo bmp
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dduo(14 + 40 + (self.width * self.height * 3)))
            file.write(dduo(0))
            file.write(dduo(14 + 40))

            file.write(dduo(40))
            file.write(dduo(self.width))
            file.write(dduo(self.height))
            file.write(duo(1))
            file.write(duo(24))
            file.write(dduo(0))
            file.write(dduo(self.width * self.height * 3))
            file.write(dduo(0))
            file.write(dduo(0))
            file.write(dduo(0))
            file.write(dduo(0))

            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
