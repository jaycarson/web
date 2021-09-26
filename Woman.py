from random import Random


class Woman(object):
    def __init__(self, years, months, weight, height, carnivore, twins, casual_smoker, regular_smoker, conceive, miscarry, ivf, ivf_allowed, seed):
        self.carnivore = carnivore
        self.casual_smoker = casual_smoker
        self.regular_smoker = regular_smoker
        self.height = height
        self.weight = weight
        self.years = years
        self.months = months
        self.twins_run_in_family = twins
        self.age = years + months / 12.0
        self.children = 0
        self.children_with_down_syndrom = 0
        self.miscarriages = 0
        self.still_births = 0
        self.months_trying = 0
        self.chance_to_conceive = conceive
        self.chance_to_miscarry_early = miscarry
        self.chance_on_ivf = ivf
        self.chance_to_miscarry_late = 0.015
        self.has_had_still_birth = False
        self.on_ivf = False
        self.ivf_allowed = ivf_allowed
        self.random_obj = Random()
        self.random_obj.seed(seed)

        self.bmi = 703 * self.weight / (self.height * self.height)
        self.miscarriage_risk = 0.0

        self.is_pregnant = False
        self.preg_month = 0

    def __call__(self):
        self.update()
        if self.is_pregnant:
            if self.preg_month == 2:
                if self.random_obj.random() < self.get_miscarriage_early_chance():
                    self.is_pregnant = False
                    self.miscarriages += 1
                else:
                    self.preg_month += 1
            elif self.preg_month == 6:
                if self.random_obj.random() < self.chance_to_miscarry_late:
                    self.is_pregnant = False
                    self.miscarriages += 1
                else:
                    self.preg_month += 1
            elif self.preg_month == 9:
                self.is_pregnant = False
                self.weight += 5
                self.children += self.birth()
                self.on_ivf = False
            else:
                self.preg_month += 1
        else:
            if self.on_ivf:
                if self.random_obj.random() < self.chance_on_ivf[self.years]:
                    self.is_pregnant = True
                    self.preg_month = 0
                    self.months_trying = 0
                else:
                    self.months_trying += 1
            else:
                if self.random_obj.random() < self.chance_to_conceive[self.years]:
                    self.is_pregnant = True
                    self.preg_month = 0
                    self.months_trying = 0
                else:
                    self.months_trying += 1
                    if self.months_trying >= 6 and self.ivf_allowed:
                        self.on_ivf = True

        if self.months == 12:
            self.years += 1
            self.months = 1
        else:
            self.months += 1

    def birth(self):
        children = 1

        fraternal_twin_chance = 1.0 / 250.0
        identical_twin_chance = 3.5 / 1000.0

        if self.on_ivf:
            if self.years <= 35:
                fraternal_twin_chance = 0.121
            elif self.years <= 37:
                fraternal_twin_chance = 0.091
            elif self.years <= 40:
                fraternal_twin_chance = 0.053
        else:
            if self.height > 64.0:
                fraternal_twin_chance *= 2.0
            if self.years > 35:
                fraternal_twin_chance *= 4.0
            if self.bmi > 30.0:
                fraternal_twin_chance *= 1.25
            if self.bmi < 18.5:
                fraternal_twin_chance *= 0.75
            if self.carnivore:
                fraternal_twin_chance *= 5.0
            if self.twins_run_in_family:
                fraternal_twin_chance *= 2.5

        if self.random_obj.random() < fraternal_twin_chance:
            children += 1

        count = children

        for twin in range(0, count):
            if self.random_obj.random() < identical_twin_chance:
                children += 1

        count = children

        for child in range(0, count):
            if self.random_obj.random() < self.get_down_syndrom_chance():
                self.children_with_down_syndrom += 1
            if self.random_obj.random() < self.get_still_birth_chance():
                children -= 1
                self.still_births += 1
                self.has_had_still_birth = True

        return children

    def get_down_syndrom_chance(self):
        if self.years < 25:
            return 1.0 / 1200.0
        elif self.years < 35:
            return 1.0 / 350.0
        elif self.years < 40:
            return 1.0 / 100.0
        elif self.years < 45:
            return 1.0 / 30.0
        else:
            return 1.0 / 30.0

    def get_miscarriage_early_chance(self):
        success = 1 - self.chance_to_miscarry_early[self.years]
        mod = -self.miscarriage_risk + 2
        return 1 - success * mod

    def get_miscarriage_late_chance(self):
        return self.chance_to_miscarry_late

    def get_still_birth_chance(self):
        if self.has_had_still_birth:
            chance = 0.025
        else:
            chance = 0.01

        # Note chances increased by 20% per 5 BMI points starting at 26
        if self.bmi > 26.0:
            chance *= 1.2
        if self.bmi > 31.0:
            chance *= 1.2
        if self.bmi > 36.0:
            chance *= 1.2
        if self.bmi > 41.0:
            chance *= 1.2
        if self.bmi > 46.0:
            chance *= 1.2

        # Note smoking 1-9 cigarettes per day increases chance 9%
        if self.casual_smoker:
            chance *= 1.09

        # Note smoking 10+ cigarettes per day increases chance 52%
        if self.regular_smoker:
            chance *= 1.52

        return chance

    def update(self):
        self.bmi = 703 * self.weight / (self.height * self.height)

        if self.bmi < 18.5:
            self.miscarriage_risk = 1.08
        elif self.bmi < 25.0:
            self.miscarriage_risk = 1.0
        elif self.bmi < 30.0:
            self.miscarriage_risk = 1.09
        elif self.bmi < 35.0:
            self.miscarriage_risk = 1.15
        else:
            self.miscarriage_risk = 1.27
