import mymath

def main():
    print("삼각형의 넓이 계산:")
    base = float(input("밑변의 길이를 입력하세요: "))
    height = float(input("높이의 길이를 입력하세요: "))
    print(f"삼각형의 넓이: {mymath.triangle_area(base, height)}")

    print("\n원의 넓이 계산:")
    radius = float(input("원의 반지름을 입력하세요: "))
    print(f"원의 넓이: {mymath.circle_area(radius)}")

    print("\n직사각형의 넓이 계산:")
    length = float(input("길이를 입력하세요: "))
    width = float(input("너비를 입력하세요: "))
    print(f"직사각형의 넓이: {mymath.rectangle_area(length, width)}")

    print("\n직육면체의 표면적 계산:")
    length = float(input("길이를 입력하세요: "))
    width = float(input("너비를 입력하세요: "))
    height = float(input("높이를 입력하세요: "))
    print(f"직육면체의 표면적: {mymath.cuboid_surface_area(length, width, height)}")

if __name__ == "__main__":
    main()