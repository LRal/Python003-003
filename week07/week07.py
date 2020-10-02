from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, catagory, body_type, character):
        self.catagory = catagory
        self.body_type = body_type
        self.character = character
        self.is_fierce = bool(
            self.catagory == '食肉' and
            self.body_type >= '中等' and
            self.character == '凶猛'
        )


class Cat(Animal):
    def __init__(self, name, catagory, body_type, character):
        super().__init__(catagory, body_type, character)
        self.name = name
        self.sound = 'Meow'
        self.fit_for_pet = bool(self.character != '凶猛')


class Dog(Animal):
    def __init__(self, name, catagory, body_type, character):
        super().__init__(catagory, body_type, character)
        self.name = name
        self.sound = 'Bark'
        self.fit_for_pet = bool(self.character != '凶猛')


class Zoo:
    def __init__(self, name):
        self.name = name
        self.__animal_list = []

    def add_animal(self, animal):
        if animal.name not in self.__animal_list:
            self.__animal_list.append(animal.name)
        else:
            raise Exception(f'{animal.name} has already been added.')

        setattr(self, animal.__class__.__name__, None)


if __name__ == '__main__':
    z = Zoo('时间动物园')
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    z.add_animal(cat1)
    have_cat = hasattr(z, 'Cat')
