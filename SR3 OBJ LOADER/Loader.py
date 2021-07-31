#Universidad del Valle de Guatemala
#Graficas por Computadora
#Laboratorio SR3
#Diego Crespo 19541

class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.verts = []
        self.tcoord = []
        self.normals = []
        self.faces = []

        self.read()


    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v':
                    self.verts.append(list(map(float, value.split(' '))))
                elif prefix == 'vt': 
                    self.tcoord.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append( [ list(map(int, vert.split('/'))) for vert in value.split(' ')] )
