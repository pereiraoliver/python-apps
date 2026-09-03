"""Notes and a basic example for Python abstract classes."""

from abc import ABC, abstractmethod


# Abstract classes enforces methods in their child classes
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        """Every animal must define its own sound."""
        pass


# Dog() must implement make_sound method as it is a child of the abstract Animal class
class Dog(Animal):
    def make_sound(self):
        print("Woof!")


# Dog() now can be instantiated.
my_dog = Dog()
my_dog.make_sound()

# animal = Animal() ---> would raise TypeError because it cannot be instantiated.
