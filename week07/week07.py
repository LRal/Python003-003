from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, catagory, body_type, character):
        self.catagory = catagory
        self.body_type = body_type
        self.character = character

    @property
    def is_fierce(self):
        return bool(
            self.catagory == '食肉' and
            self.body_type >= '中等' and
            self.character == '凶猛'
        )


class Cat(Animal):
    def __init__(self, name, catagory, body_type, character):
        super().__init__(catagory, body_type, character)
        self.name = name

    @property
    def sound(self):
        return 'Meow'

    @property
    def fit_for_pet(self):
        return bool(self.character != '凶猛')


class Dog(Animal):
    def __init__(self, name, catagory, body_type, character):
        super().__init__(catagory, body_type, character)
        self.name = name

    @property
    def sound(self):
        return 'Bark'

    @property
    def fit_for_pet(self):
        return bool(self.character != '凶猛')


class Zoo:
    def __init__(self, name):
        self.name = name
        self.__animal_list = []

    def add_animal(self, animal):
        if animal.name not in self.__animal_list:
            setattr(self, animal.__class__.__name__, None)
            self.__animal_list.append(animal.name)
        else:
            raise Exception(f'{animal.name} has already been added.')


if __name__ == '__main__':
    z = Zoo('时间动物园')
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    z.add_animal(cat1)
    have_cat = hasattr(z, 'Cat')
