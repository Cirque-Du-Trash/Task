from animals.mammals import Dog
from animals.birds import Eagle

def main():
    dog = Dog(name="Buddy", breed="Golden Retriever")
    print(dog)
    print(dog.speak())

    eagle = Eagle(name="Baldy", wingspan=2.3)
    print(eagle)
    print(eagle.fly())

if __name__ == "__main__":
    main()