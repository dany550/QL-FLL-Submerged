from umath import*



class Vec:
    def __init__(self,x,y):
        self.x = y
        self.y = y
    
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    # skalární součin a násobení skalárem (scalar mult and dot product)
    def __mul__(self, other):
        if isinstance(other, Vec):
            # Skalární součin
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            # Násobení vektoru skalárem
            return Vec(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __add__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x - other.x, self.y - other.y)
    
    # délka vektoru
    def lenght(self):
        return sqrt(self.x**2 + self.y**2)
    
    # sestrojení jednotkového vektoru podle osy x/y
    def xAxis():
        return Vec(1,0)
    def yAxis():
        return Vec(0,1)
    
class Matrix:
    def __init__(self, matrix = [[1,0],[0,1]]):
        if isinstance(matrix, list) and len(matrix) == 2 and all(len(row) == 2 for row in matrix):
            self.val = matrix  # Uložení matice do 2D seznamu
        else:
            raise ValueError("Matrix must be 2 by 2")

    def __repr__(self):
        # Reprezentace matice pro print
        return f"[{self.val[0][0]}, {self.val[0][1]}]\n[{self.val[1][0]}, {self.val[1][1]}]"

    # Přístup k prvkům matice přes indexaci
    def __getitem__(self, indices):
        x, y = indices
        return self.val[x][y]

    # Sčítání matic
    def __add__(self, other):
        if isinstance(other, Matrix):
            result = [
                [self.val[0][0] + other.val[0][0], self.val[0][1] + other.val[0][1]],
                [self.val[1][0] + other.val[1][0], self.val[1][1] + other.val[1][1]],
            ]
            return Matrix(result)

    # Násobení matic
    def __mul__(self, other):
        if isinstance(other, Matrix):
            result = [
                [
                    self.val[0][0] * other.val[0][0] + self.val[0][1] * other.val[1][0],
                    self.val[0][0] * other.val[0][1] + self.val[0][1] * other.val[1][1],
                ],
                [
                    self.val[1][0] * other.val[0][0] + self.val[1][1] * other.val[1][0],
                    self.val[1][0] * other.val[0][1] + self.val[1][1] * other.val[1][1],
                ],
            ]
            return Matrix(result)
    # sestrojení rotační matice
    def rot(radians):
        return Matrix([[cos(radians),-sin(radians)],[sin(radians),cos(radians)]])