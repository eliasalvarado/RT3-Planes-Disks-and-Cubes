from math import tan, pi, atan2, acos
from npPirata import subtractVectors, vectorMagnitude, normVector, dot, multVectorScalar, multVectors, addVectors, addVectorScalar, subtractVectorScalar


class Intercept(object):
    def __init__(self, distance, point, normal, texCoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj
        self.texCoords = texCoords


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        L = subtractVectors(self.position, orig)
        magnitudL = vectorMagnitude(L)
        tca = dot(L, dir)
        d = (magnitudL ** 2 - tca ** 2) ** 0.5

        if type(d) is complex:
            d = float(d.real)

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        dir = multVectorScalar(dir, t0)
        point = [orig[i] + dir[i] for i in range(3)]
        normal = subtractVectors(point, self.position)
        normal = normVector(normal)

        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = acos(normal[1]) / pi


        return Intercept(t0, point, normal, (u, v), self)


class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = normVector(normal)
        super().__init__(position=position, material=material)

    def ray_intersect(self, orig, dir):
        denom = dot(dir, self.normal)

        if (abs(denom) <= 0.0001):
            return None
            
        num = dot((subtractVectors(self.position, orig)), self.normal)
        t = num / denom

        if (t < 0):
            return None

        point = addVectors(orig, multVectorScalar(dir, t))
        
        return Intercept(t, point, self.normal, None, self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position=position, normal=normal, material=material)

    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)

        if planeIntersect is None:
            return None
        
        contactDistance = subtractVectors(planeIntersect.point, self.position)

        contactDistance = vectorMagnitude(contactDistance)

        if (contactDistance > self.radius):
            return None
        
        return Intercept(planeIntersect.distance, planeIntersect.point, self.normal, None, self)


class AABB(Shape):
    def __init__(self, position, size, material):
        super().__init__(position=position, material=material)

        self.size = size
        self.planes = []

        leftPlane = Plane(position=addVectors(position, [-size[0] / 2, 0, 0]), normal=(-1, 0, 0), material=material)
        rightPlane = Plane(position=addVectors(position, [size[0] / 2, 0, 0]), normal=(1, 0, 0), material=material)

        bottomPlane = Plane(position=addVectors(position, [0, -size[1] / 2, 0]), normal=(0, -1, 0), material=material)
        topPlane = Plane(position=addVectors(position, [0, size[1] / 2, 0]), normal=(0, 1, 0), material=material)

        frontPlane = Plane(position=addVectors(position, [0, 0, -size[2] / 2]), normal=(0, 0, -1), material=material)
        backPlane = Plane(position=addVectors(position, [0, 0, size[2] / 2]), normal=(0, 0, 1), material=material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        self.boundsMin = [0, 0, 0]
        self.boundsMax = [0, 0, 0]

        self.bias = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (self.bias + size[i] / 2)
            self.boundsMax[i] = self.position[i] + (self.bias + size[i] / 2)

    def ray_intersect(self, orig, dir):
        intercept = None

        t = float('inf')
        u = v = 0

        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig=orig, dir=dir)

            if planeIntersect is not None:
                planePoint = planeIntersect.point

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intercept = planeIntersect

                                if abs(plane.normal[0]) > 0:
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2)
                                elif abs(plane.normal[1]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + self.bias * 2)
                                elif abs(plane.normal[2]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + self.bias * 2)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + self.bias * 2)

        if intercept is None:
            return None
        
        return Intercept(t, intercept.point, intercept.normal, (u, v), self)




