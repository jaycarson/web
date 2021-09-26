from Woman import Woman
import yaml
import argparse
import os


class Simulation(object):
    def __init__(self, years, months, weight, height, carnivore, twins, casual_smoker, regular_smoker, end_year, ivf_allowed, size):
        self.years = int(years)
        self.months = int(months)
        end_year = int(end_year)
        self.duration = end_year * 12 - self.years * 12 - self.months
        self.sample_size = size
        self.weight = weight
        self.height = height
        self.simulation_length_years = end_year - years

        keys = []

        if weight > 25 * height * height / 703:
            keys.append('Over Weight')
        elif weight < 18 * height * height / 703:
            keys.append('Under Weight')
        else:
            keys.append('Healthy Weight')

        if regular_smoker:
            keys.append('Regular Smoker')
        elif casual_smoker:
            keys.append('Casual Smoker')
        else:
            keys.append('Nonsmoker')
        
        if ivf_allowed:
            keys.append('IVF Allowed')
        else:
            keys.append('IVF Not Allowed')

        self.key = '-'.join(keys)

        chance_to_conceive = yaml.load(open('fertility.yml', 'r'), Loader=yaml.FullLoader)
        chance_to_miscarry = yaml.load(open('miscarriage.yml', 'r'), Loader=yaml.FullLoader)
        chance_on_ivf = yaml.load(open('ivf.yml', 'r'), Loader=yaml.FullLoader)

        self.population = []
        seed = 0
        for woman_id in range(0, self.sample_size):
            self.population.append(
                Woman(
                    self.years,
                    self.months,
                    weight,
                    height,
                    carnivore,
                    twins,
                    casual_smoker,
                    regular_smoker,
                    conceive = chance_to_conceive,
                    miscarry = chance_to_miscarry,
                    ivf = chance_on_ivf,
                    ivf_allowed = ivf_allowed,
                    seed = seed,
                )
            )
            seed += 1
        print('Age:          ' + str(self.years))
        print('Age End:      ' + str(end_year))
        print('Weight:       ' + str(weight))
        print('Height:       ' + str(height))
        print('BMI:          ' + str(self.population[0].bmi)[0:5])
        print('Carnivore:    ' + str(carnivore))
        print('Twins:        ' + str(twins))
        print('IVF Allowed:  ' + str(ivf_allowed))
        print('')
        
        if os.path.exists('details.yml'):
            self.records = yaml.load(open('details.yml', 'r'), Loader=yaml.FullLoader)
        else:
            self.records = {
                'summary': {
                    'Age': self.years,
                    'Age_End': end_year,
                    'Weight': weight,
                    'Height': height,
                    'BMI': self.population[0].bmi,
                    'Carnivore': carnivore,
                    'Twins': twins,
                    'IVF_Allowed': ivf_allowed,
                    'Duration': self.duration,
                },
                'details': {}}

    def __call__(self):
        for period in range(0, self.duration + 1):
            for woman in self.population:
                woman()
            total_children = 0
            total_miscarriages = 0
            total_still_births = 0
            total_children_with_down_syndrom = 0
            max_children = min(int(self.simulation_length_years / (40 / 52)) + 1, 40)
            
            if period not in self.records['details']:
                self.records['details'][period] = {}

            for i in range(0, max_children):
                self.add_distribution(period, i, 'Children')
                self.add_distribution(period, i, 'Miscarriages')

            for woman in self.population:
                total_children += woman.children
                total_children_with_down_syndrom += woman.children_with_down_syndrom
                total_miscarriages += woman.miscarriages
                total_still_births += woman.still_births

                self.records['details'][period]['Children_Dist'][woman.children][self.key] += 1
                if woman.miscarriages not in self.records['details'][period]['Miscarriages_Dist']:
                    self.records['details'][period]['Miscarriages_Dist'][woman.miscarriages] = {}
                if self.key not in self.records['details'][period]['Miscarriages_Dist'][woman.miscarriages]:
                    self.records['details'][period]['Miscarriages_Dist'][woman.miscarriages][self.key] = 0
                self.records['details'][period]['Miscarriages_Dist'][woman.miscarriages][self.key] += 1

            for i in range(0, max_children):
                self.records['details'][period]['Children_Dist_Percent'][i][self.key] = round(self.records['details'][period]['Children_Dist'][i][self.key] / self.sample_size * 100, 2)
                self.records['details'][period]['Miscarriages_Dist_Percent'][i][self.key] = round(self.records['details'][period]['Miscarriages_Dist'][i][self.key] / self.sample_size * 100, 2)

            if self.months + period % 12 > 12:
                age = self.years + period // 12 + 1
            else:
                age = self.years + period // 12
            self.add_detail(period, 'Age', 'Age', age)
            self.add_detail(period, 'Year', 'Year', period // 12)
            self.add_detail(period, 'Month', 'Month', period % 12)
            self.add_detail(period, 'Weight', 'Weight', self.weight)
            self.add_detail(period, 'Height', 'Height', self.height)
            self.add_detail(period, 'Total_Children', 'Total_Children', total_children)
            self.add_detail(period, 'Total_Children_Percent', 'Average_Number_Of_Children', total_children / self.sample_size)
            self.add_detail(period, 'Total_Children_With_Down_Syndrom', 'Total_Children_With_Down_Syndrom', total_children_with_down_syndrom)
            self.add_detail(period, 'Total_Children_With_Down_Syndrom_Percent', 'Total_Children_With_Down_Syndrom', total_children_with_down_syndrom / self.sample_size)
            self.add_detail(period, 'Total_Miscarriages', 'Total_Miscarriages', total_miscarriages)
            self.add_detail(period, 'Total_Miscarriages_Percent', 'Average_Number_Of_Miscarriages', total_miscarriages / self.sample_size)
            self.add_detail(period, 'Total_Still_Births', 'Total_Still_Births', total_still_births)
            self.add_detail(period, 'Total_Still_Births_Percent', 'Average_Number_Of_Still_Births', total_still_births / self.sample_size)

        with open('details.yml', 'w') as fh:
            yaml.dump(self.records, fh)

    def add_detail(self, period, record_name, field, value):
        if period not in self.records['details']:
            self.records['details'][period] = {}
        if record_name not in self.records['details'][period]:
            self.records['details'][period][record_name] = {}
        if field not in self.records['details'][period][record_name]:
            self.records['details'][period][record_name][field] = {}
        self.records['details'][period][record_name][field][self.key] = value

    def add_distribution(self, period, i, distribution):
        if distribution + '_Dist' not in self.records['details'][period]:
            self.records['details'][period][distribution + '_Dist'] = {}
        if distribution + '_Dist_Percent' not in self.records['details'][period]:
            self.records['details'][period][distribution + '_Dist_Percent'] = {}

        if i not in self.records['details'][period][distribution + '_Dist']:
            self.records['details'][period][distribution + '_Dist'][i] = {}
        if i not in self.records['details'][period][distribution + '_Dist_Percent']:
            self.records['details'][period][distribution + '_Dist_Percent'][i] = {}

        self.records['details'][period][distribution + '_Dist'][i][self.key] = 0
        self.records['details'][period][distribution + '_Dist_Percent'][i][self.key] = 0.0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            """,
        epilog="""
            """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--years",
        default=35,
        help="Set starting age in years",
    )
    parser.add_argument(
        "--months",
        default=0,
        help="Set starting age in months",
    )
    parser.add_argument(
        "--weight",
        default=170,
        help="Set the weight of the subjects",
    )
    parser.add_argument(
        "--height",
        default=64,
        help="Set the height of the subjects.",
    )
    parser.add_argument(
        "--carnivore",
        action='store_true',
        help="Set whether the subjects primarily eat meat or not.",
    )
    parser.add_argument(
        "--twins",
        action='store_true',
        help="Set whether the subjects have twins running in the family.",
    )
    parser.add_argument(
        "--casual",
        action='store_true',
        help="Set whether the subjects are casual smokers or not.",
    )
    parser.add_argument(
        "--regular",
        action='store_true',
        help="Set whether the subjects are regular smokers or not.",
    )
    parser.add_argument(
        "--end",
        default=40,
        help="Set end year.",
    )
    parser.add_argument(
        "--ivf",
        action='store_false',
        help="Set whether IVF is allowed or not.",
    )
    parser.add_argument(
        "--size",
        default=1000,
        help="Set sample size.",
    )
    parser.add_argument(
        "--tall",
        action='store_true',
        help="Set subjects to be tall (5'4''+).",
    )
    parser.add_argument(
        "--healthy",
        action='store_true',
        help="Set subjects to be have a healthy weight.",
    )
    parser.add_argument(
        "--morbid",
        action='store_true',
        help="Set subjects to be have a healthy weight.",
    )

    args = parser.parse_args()

    if args.tall:
        args.height = 65
    if args.healthy:
        args.weight = 130
    elif args.morbid:
        args.weight = 234

    bmi = (int(args.weight) * 703) / (int(args.height) * int(args.height))

    app = Simulation(
        years = int(args.years),
        months = int(args.months),
        weight = int(args.weight),
        height = int(args.height),
        carnivore = args.carnivore,
        twins = args.twins,
        casual_smoker = args.casual,
        regular_smoker = args.regular,
        end_year = int(args.end),
        ivf_allowed = args.ivf,
        size = int(args.size),
    )
    app()

    if bmi >= 25.0:
        app = Simulation(
            years = int(args.years),
            months = int(args.months),
            weight = 24.0 * int(args.height) * int(args.height) / 703.0,
            height = int(args.height),
            carnivore = args.carnivore,
            twins = args.twins,
            casual_smoker = args.casual,
            regular_smoker = args.regular,
            end_year = int(args.end),
            ivf_allowed = args.ivf,
            size = int(args.size),
        )
        app()
