from socket import socket as TempLib;NetworkHandeler = TempLib();del TempLib
import math

class Vec3:
    def __init__(self,x:float=0,y:float=0,z:float=0,color:tuple = (0,0,0)):
        """
        Vec3: class storing position and color


        x = pos.x


        y = pos.y


        z = pos.z


        color: tuple with red green and blue values

        """

        self.x = x
        self.y = y
        self.z = z
        self.color = color
    
    def screen_space(self,ScreenSize):
        """
        
        Converts x and y to screenspace for drawing on canvas
        
        """

        Width = ScreenSize[0]
        Height = ScreenSize[1]

        x = self.x+Width/2
        y = -self.y
        y = y+Height/2
        
        return Vec3(x,y,self.z,self.color)
    def ToMatrix(self):
        """

        Converts X, Y and Z into a list for matrix transformations.

        """
        return [[self.x],[self.y],[self.z]]
    def FromMatrix(self,Matrix):
        """

        Converts a 1x3 matrix to a vec3

        """
        self.x = Matrix[0][0]
        self.y = Matrix[1][0]
        self.z = Matrix[2][0]

class Matrices:
    def Projection(FOV:float=math.radians(60)):
        return [
            [1,0,0],
            [0,1,0],
            [0,0,1],
            [0,0,math.tan(FOV)]
        ]
    def RotX(angle:float):
        angle = math.radians(angle)
        return [
            [1,0,0],
            [0,math.cos(angle),-math.sin(angle)],
            [0,math.sin(angle),math.cos(angle)]
        ]
    def RotY(angle:float):
        angle = math.radians(angle)
        return [
            [math.cos(angle),0,math.sin(angle)],
            [0,1,0],
            [-math.sin(angle),0,math.cos(angle)]
        ]
    def RotZ(angle:float):
        angle = math.radians(angle)
        return[
            [math.cos(angle),-math.sin(angle),0],
            [math.sin(angle),math.cos(angle),0],
            [0,0,1]
        ]

    def matrix_multiplacation(A,B):
        return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*A)] for X_row in B]
