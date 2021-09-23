import yaml
import argparse


class SMV(object):
    def __init__(self, debug):
        self.debug = debug
        self.data = {}
        self.bmi_m = yaml.load(open('./data/bmi_m.yml', 'r'), Loader=yaml.FullLoader)
        self.bmi_f = yaml.load(open('./data/bmi_f.yml', 'r'), Loader=yaml.FullLoader)
        self.bf_m = yaml.load(open('./data/bodyfat_m.yml', 'r'), Loader=yaml.FullLoader)
        self.bf_f = yaml.load(open('./data/bodyfat_f.yml', 'r'), Loader=yaml.FullLoader)
        self.bf_m_c = yaml.load(open('./data/bodyfat_m_caliper.yml', 'r'), Loader=yaml.FullLoader)
        self.bf_f_c = yaml.load(open('./data/bodyfat_f_caliper.yml', 'r'), Loader=yaml.FullLoader)
        self.height_f = yaml.load(open('./data/height_f.yml', 'r'), Loader=yaml.FullLoader)
        self.height_m = yaml.load(open('./data/height_m.yml', 'r'), Loader=yaml.FullLoader)
        self.income = yaml.load(open('./data/income.yml', 'r'), Loader=yaml.FullLoader)
        self.pop_by_age = yaml.load(open('./data/population_by_age.yml', 'r'), Loader=yaml.FullLoader)
        self.pop_by_state = yaml.load(open('./data/population_by_state_2013.yml', 'r'), Loader=yaml.FullLoader)
        self.smv_m = yaml.load(open('./data/smv_m.yml', 'r'), Loader=yaml.FullLoader)
        self.smv_f = yaml.load(open('./data/smv_f.yml', 'r'), Loader=yaml.FullLoader)

        self.minor = 2
        self.major = 4

        self.fitness = ''
            
        self.fitter_taller_richer_printed = False

    def __call__(self, attrs):
        if attrs['bodyfat'] > 0:
            self.fitness = 'bodyfat'
        elif attrs['bodyfat_c'] > 0:
            self.fitness = 'bodyfat_c'
        else:
            self.fitness = 'bmi'
            attrs['bmi'] = self.bmi(attrs)

        if self.debug:
            print(self.fitness +': ' + str(attrs[self.fitness]))
        if attrs['sex'] == 'male':
            print('Calling Male')
            total = 0
            total += self.total_better(attrs)
            self.percent_male(attrs)
            return 'SMV: ' + str(self.get_smv(total / self.total_pop(attrs), attrs['sex']))
        else:
            print('Calling Female')
            total = 0
            total += self.total_better(attrs)
            self.percent_female(attrs)
            return 'SMV: ' + str(self.get_smv(total / self.total_pop(attrs), attrs['sex']))

    def bmi(self, attrs):
        return round(attrs['weight'] / (attrs['height'] * attrs['height']) * 703)

    def adjust_fit(self, attrs, direction):
        value = 0
        if self.fitness == 'bmi':
            bmi = attrs['bmi']

            if direction == 'up':
                if bmi >= 37:
                    value = 36
                elif bmi >= 36:
                    value = 35
                elif bmi >= 35:
                    value = 34
                elif bmi >= 34:
                    value = 33
                elif bmi >= 33:
                    value = 31
                else:
                    value = bmi - 1
            else:
                if bmi <= 19:
                    value = 22
                elif bmi <= 22:
                    value = 25
                elif bmi <= 25:
                    value = 27
                elif bmi <= 27:
                    value = 29
                elif bmi <= 29:
                    value = 31
                elif bmi <= 31:
                    value = 33
                elif bmi <= 33:
                    value = 35
                elif bmi <= 35:
                    value = 40
                elif bmi <= 40:
                    value = 45
                elif bmi <= 45:
                    value = 50
                else:
                    value = 54
        else:
            if self.fitness == 'bodyfat':
                bf = attrs['bodyfat']
            else:
                bf = attrs['bodyfat_c']
            if direction == 'up':
                if attrs['sex'] == 'male':
                    if bf >= 40:
                        value = 35
                    elif bf >= 35:
                        value = 30
                    elif bf >= 30:
                        value = 25
                    elif bf >= 25:
                        value = 20
                    elif bf >= 20:
                        value = 15
                    elif bf >= 15:
                        value = 10
                    elif bf >= 10:
                        value = 7
                    else:
                        value = 3
                else:
                    if bf >= 50:
                        value = 45
                    elif bf >= 45:
                        value = 40
                    elif bf >= 40:
                        value = 35
                    elif bf >= 35:
                        value = 30
                    elif bf >= 30:
                        value = 25
                    elif bf >= 25:
                        value = 20
                    elif bf >= 20:
                        value = 15
                    else:
                        value = 10
            else:
                if attrs['sex'] == 'male':
                    if bf <= 3:
                        value = 7
                    elif bf <= 7:
                        value = 10
                    elif bf <= 10:
                        value = 15
                    elif bf <= 15:
                        value = 20
                    elif bf <= 20:
                        value = 25
                    elif bf <= 25:
                        value = 30
                    elif bf <= 30:
                        value = 25
                    else:
                        value = 40
                else:
                    if bf <= 10:
                        value = 15
                    elif bf <= 15:
                        value = 20
                    elif bf <= 20:
                        value = 25
                    elif bf <= 25:
                        value = 30
                    elif bf <= 30:
                        value = 35
                    elif bf <= 35:
                        value = 40
                    elif bf <= 40:
                        value = 45
                    else:
                        value = 50
        return value

    def adjust_height(self, attrs, direction):
        height = attrs['height']
        if direction == 'up':
            if height <= 63:
                return 65
            elif height <= 68:
                return 68
            elif height <= 70:
                return 70
            elif height <= 72:
                return 72
            elif height <= 74:
                return 74
            else:
                return 76
        else:
            if height >= 76:
                return 74
            if height >= 74:
                return 72
            elif height >= 72:
                return 70
            elif height >= 70:
                return 68
            elif height >= 68:
                return 65
            else:
                return 60

    def adjust_income(self, attrs, direction):
        income = attrs['income']
        if direction == 'up':
            if income < 50000:
                return 50000
            elif income < 100000:
                return 100000
            elif income < 200000:
                return 200000
            else:
                return 300000
        else:
            if income > 200000:
                return 200000
            elif income > 100000:
                return 100000
            elif income > 50000:
                return 50000
            else:
                return

    def adjust_young(self, attrs, direction):
        age = attrs['age']
        if direction == 'up':
            if age > 50:
                return 40
            elif age >= 45:
                return 35
            elif age >= 35:
                return 29
            elif age >= 29:
                return 25
            elif age >= 25:
                return 20
            else:
                return 18
        else:
            if age <= 20:
                return 25
            elif age <= 25:
                return 29
            elif age <= 29:
                return 35
            elif age <= 35:
                return 45
            else:
                return 50

    def get_smv(self, percent, sex):
        percent *= 100
        if self.debug:
            print("Percent: " + str(round(percent, 2)))
        if sex == 'male':
            for x in self.smv_m:
                if percent < self.smv_m[x]:
                    return x
        else:
            for x in self.smv_f:
                if percent < self.smv_f[x]:
                    return x

    def percent_fit(self, attrs, fit=None):
        if attrs['sex'] == 'male':
            if self.fitness == 'bmi':
                table = self.bmi_m
            elif self.fitness == 'bodyfat':
                table = self.bf_m
            else:
                table = self.bf_m_c
        else:
            if self.fitness == 'bmi':
                table = self.bmi_f
            elif self.fitness == 'bodyfat':
                table = self.bf_f
            else:
                table = self.bf_f_c
        if fit is None:
             fit = attrs[self.fitness]
        if fit not in table:
            return 1
        return table[fit] / 100

    def percent_height(self, attrs, height=None):
        height_percent = 0
        if attrs['sex'] == 'male':
            if height is None:
                height_percent = self.height_m[attrs['height']]
            else:
                height_percent = self.height_m[height]
        else:
            if height is None:
                height_percent = self.height_f[attrs['height']]
            else:
                height_percent = self.height_f[height]
        return (100 - height_percent) / 100

    def percent_income(self, attrs, income=None):
        if income is None:
            income = attrs['income']
        for x in range(0, 100):
            income_target = self.income[x]
            if income_target > income:
                return (100 - x) / 100

    def percent_young(self, attrs, youth=None):
        if youth is None:
            youth = attrs['age']
        younger = 0.0
        total_younger = 0.0
        for x in range(18, 40):
            percent = self.pop_by_age[x]
            if x <= youth:
                younger += percent
            total_younger += percent
        return younger / total_younger

    def percent_female(self, attrs):
        pop = self.total_pop(attrs)
        #base = pop * self.percent_fit(attrs) * self.percent_height(attrs) * self.percent_income(attrs)
        attrs['mod'] = False

        total = 0
        total += self.total_better(attrs)

        print('total: ' + str(total))
        print('SMV: ' + str(self.get_smv(total / self.total_pop(attrs), attrs['sex'])))
    
    def percent_male(self, attrs):
        pop = self.total_pop(attrs)
        #base = pop * self.percent_fit(attrs) * self.percent_youth(attrs)
        attrs['mod'] = False

        total = 0
        total += self.total_better(attrs)

        print('total: ' + str(total))
        print('SMV: ' + str(self.get_smv(total / self.total_pop(attrs), attrs['sex'])))

    def total_pop(self, attrs):
        total_population = 0
        for x in range(1, 85+1):
            if x > attrs['min_a'] and x < attrs['max_a']:
                total_population += self.pop_by_age[x]
        value = round(total_population / 100 * self.pop_by_state[attrs['state']][attrs['sex']])
        if self.debug and False:
            print("Total Pop: " + str(value))
        return value

    def total_base(self, attrs):
        pop = self.total_pop(attrs)
        value = round(
            pop 
            * self.percent_fit(attrs)
            * self.percent_height(attrs)
            * self.percent_income(attrs)
        )
        if self.debug:
            print("Base: " + str(value))
        return value

    def total_better(self, attrs):
        attrs['mod'] = False
        total = 0

        if attrs['sex'] == 'male':
            total += self.total_fitter(attrs)
            total += self.total_taller(attrs)
            total += self.total_richer(attrs)
            total += self.total_fitter_taller(attrs)
            total += self.total_fitter_richer(attrs)
            total += self.total_taller_richer(attrs)
            total += self.total_fitter_taller_richer(attrs)
        else:
            total += self.total_slimmer(attrs)
            total += self.total_younger(attrs)
            total += self.total_younger_fitter(attrs)
        attrs['mod'] = False
        if self.debug:
            print("Better: " + str(total))
        return total

    def total_slimmer(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'up'))
        y = self.percent_young(attrs, self.adjust_young(attrs, 'down')) - self.percent_young(attrs, self.adjust_young(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * y)
        if self.debug:
            print("Fitter: " + str(value))
            print("    Younger: " + str(round(y, 2)))
            print("    Fitter:  " + str(round(f, 2)))
        return value

    def total_younger(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'down')) - self.percent_fit(attrs, self.adjust_fit(attrs, 'up'))
        y = self.percent_young(attrs, self.adjust_young(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * y)
        if self.debug:
            print("Younger: " + str(value))
            print("    Younger: " + str(round(y, 2)))
            print("    Fitter:  " + str(round(f, 2)))
        return value

    def total_younger_fitter(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'up'))
        y = self.percent_young(attrs, self.adjust_young(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * y)
        if self.debug:
            print("Younger Fitter: " + str(value))
            print("    Younger: " + str(round(y, 2)))
            print("    Fitter:  " + str(round(f, 2)))
        return value

    def total_fitter(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'up'))
        h = (self.percent_height(attrs, self.adjust_height(attrs, 'down')) - self.percent_height(attrs, self.adjust_height(attrs, 'up')))
        w = ((self.percent_income(attrs, self.adjust_income(attrs, 'down'))) - self.percent_income(attrs, self.adjust_income(attrs, 'up')))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug:
            print("Fitter: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
        return value

    def total_taller(self, attrs):
        f = (self.percent_fit(attrs, self.adjust_fit(attrs, 'down')) - self.percent_fit(attrs, self.adjust_fit(attrs, 'up')))
        h = self.percent_height(attrs, self.adjust_height(attrs, 'up'))
        w = ((self.percent_income(attrs, self.adjust_income(attrs, 'down'))) - self.percent_income(attrs, self.adjust_income(attrs, 'up')))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug:
            print("Taller: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
        return value

    def total_richer(self, attrs):
        f = (self.percent_fit(attrs, self.adjust_fit(attrs, 'down')) - self.percent_fit(attrs, self.adjust_fit(attrs, 'up')))
        h = (self.percent_height(attrs, self.adjust_height(attrs, 'down')) - self.percent_height(attrs, self.adjust_height(attrs, 'up')))
        w = self.percent_income(attrs, self.adjust_income(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug:
            print("Richer: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
        return value

    def total_fitter_taller(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'up')) 
        h = self.percent_height(attrs, self.adjust_height(attrs, 'up'))
        w = ((self.percent_income(attrs, self.adjust_income(attrs, 'down'))) - self.percent_income(attrs, self.adjust_income(attrs, 'up')))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug:
            print("Fitter Taller: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
        return value

    def total_fitter_richer(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'up'))
        h = (self.percent_height(attrs, self.adjust_height(attrs, 'down')) - self.percent_height(attrs, self.adjust_height(attrs, 'up')))
        w = self.percent_income(attrs, self.adjust_income(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug:
            print("Fitter Richer: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
        return value

    def total_taller_richer(self, attrs):
        f = (self.percent_fit(attrs, self.adjust_fit(attrs, 'down')) - self.percent_fit(attrs, self.adjust_fit(attrs, 'up')))
        h = self.percent_height(attrs, self.adjust_height(attrs, 'up'))
        w = self.percent_income(attrs, self.adjust_income(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug:
            print("Taller Richer: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
        return value

    def total_fitter_taller_richer(self, attrs):
        f = self.percent_fit(attrs, self.adjust_fit(attrs, 'up'))
        h = self.percent_height(attrs, self.adjust_height(attrs, 'up'))
        w = self.percent_income(attrs, self.adjust_income(attrs, 'up'))
        value = round(self.total_pop(attrs) * f * h * w)
        if self.debug and not self.fitter_taller_richer_printed:
            print("Fitter Taller Richer: " + str(value))
            print("    Fitness: " + str(round(f, 2)))
            print("    Height:  " + str(round(h, 2)))
            print("    Wealth:  " + str(round(w, 2)))
            self.fitter_taller_richer_printed = True
        return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            """,
        epilog="""
            """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action='store_true',
        help="Set debugging",
    )
    args = parser.parse_args()

    app = SMV(debug=args.debug)
    attrs_m = {
        'sex': 'male',
        'height': 74,
        'weight': 195,
        'bodyfat': 0,
        'bodyfat_c': 0,
        'income': 135000,
        'age': 40,
        'min_a': 25,
        'max_a': 45,
        'state': 'Minnesota',
    }
    attrs_f = {
        'sex': 'female',
        'height': 67,
        'weight': 165,
        'bodyfat': 0,
        'bodyfat_c': 0,
        'income': 35000,
        'age': 38,
        'min_a': 18,
        'max_a': 45,
        'state': 'Minnesota',
    }
    app(attrs_f)
