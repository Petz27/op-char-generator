class Feat:
    def __init__(self, name, feat_type, prerequisite, benefit, effect, class_name):
        self.name = name
        self.type = feat_type
        self.prerequisite = prerequisite
        self.benefit = benefit
        self.effect = effect
        self.class_name = class_name

    def display(self):
        print(f"Name: {self.name}")
        print(f"Type: {self.type}")
        print(f"Prerequisite: {self.prerequisite}")
        print(f"Benefit: {self.benefit}")
        print(f"Effect: {self.effect}")
        print(f"Class: {self.class_name}")