import math

def triangle_area(base, height):
    """삼각형의 넓이를 계산합니다."""
    return 0.5 * base * height

def circle_area(radius):
    """원의 넓이를 계산합니다."""
    return math.pi * (radius ** 2)

def rectangle_area(length, width):
    """직사각형의 넓이를 계산합니다."""
    return length * width

def cuboid_surface_area(length, width, height):
    """직육면체의 표면적을 계산합니다."""
    return 2 * (length * width + width * height + height * length)