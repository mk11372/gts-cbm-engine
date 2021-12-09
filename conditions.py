BELT_THRESHOLD = 20000

class Condition:

    def __init__(self, name, category="", threshold=0):
        self.name = name
        self.category = category
        self.threshold = threshold

    def check_against_threshold(self, real_value):
        return real_value >= self.threshold

class BeltCondition(Condition):
    def __init__(self, name, category="belt", threshold=BELT_THRESHOLD):
        super().__init__(name)
        self.category = category
        self.threshold = threshold

station_belt_condition = BeltCondition("station_belt_condition")