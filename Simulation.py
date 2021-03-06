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

        try:
            chance_to_conceive = yaml.load(open('./web/data/fertility.yml', 'r'), Loader=yaml.FullLoader)
            chance_to_miscarry = yaml.load(open('./web/data/miscarriage.yml', 'r'), Loader=yaml.FullLoader)
            chance_on_ivf = yaml.load(open('./web/data/ivf.yml', 'r'), Loader=yaml.FullLoader)
        except:
            chance_to_conceive = yaml.load(open('./web/data/fertility.yml', 'r'))
            chance_to_miscarry = yaml.load(open('./web/data/miscarriage.yml', 'r'))
            chance_on_ivf = yaml.load(open('./web/data/ivf.yml', 'r'))

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
        }
        self.results = {
            'sample size': self.sample_size,
            'total children': 0,
            'total miscarriages': 0,
            'total still births': 0,
            'total children with down syndrome': 0,
            0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
            6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
        }

    def __call__(self):
        for period in range(0, self.duration + 1):
            for woman in self.population:
                woman()
            
        for woman in self.population:
            self.results['total children'] += woman.children
            self.results['total children with down syndrome'] += woman.children_with_down_syndrome
            self.results['total miscarriages'] += woman.miscarriages
            self.results['total still births'] += woman.still_births
            
            if woman.children > 10:
                self.results[10] += 1
            else:
                self.results[woman.children] += 1


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
        default=70,
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
        default=100,
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
    
    print(app.results['total children'] / app.results['sample size'])

    #if bmi >= 25.0:
    #    app = Simulation(
    #        years = int(args.years),
    #        months = int(args.months),
    #        weight = 24.0 * int(args.height) * int(args.height) / 703.0,
    #        height = int(args.height),
    #        carnivore = args.carnivore,
    #        twins = args.twins,
    #        casual_smoker = args.casual,
    #        regular_smoker = args.regular,
    #        end_year = int(args.end),
    #        ivf_allowed = args.ivf,
    #        size = int(args.size),
    #    )
    #    app()
