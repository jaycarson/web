from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField
from SMV import SMV
from Simulation import Simulation


SECRET_KEY = 'development'


app = Flask(__name__)
app.config.from_object(__name__)


class SimpleForm(FlaskForm):
    ages = []
    for x in range(18, 101):
        ages.append((x, x))
    
    end_years = []
    for x in range(18, 101):
        end_years.append((x, x))

    weights = []
    for x in range(100, 401):
        weights.append((x, x))
    
    heights = []
    for x in range(60, 84):
        heights.append((x, x))

    months = []
    for x in range(1, 13):
        months.append((x, x))

    incomes = []
    for x in range(10, 501):
        incomes.append((x * 1000, x * 1000))

    bfs = []
    for x in range(0, 51):
        bfs.append((x, x))

    age_f = SelectField(label='Age', choices=ages)
    age_m = SelectField(label='Age', choices=ages)
    weight_f = SelectField(label='Weight', choices=weights)
    weight_m = SelectField(label='Weight', choices=weights)
    height_f = SelectField(label='Height', choices=heights)
    height_m = SelectField(label='Height', choices=heights)
    end_year = SelectField(label='End Year', choices=end_years)
    month = SelectField(label='Month', choices=months)
    income_f = SelectField(label='Income', choices=incomes)
    income_m = SelectField(label='Income', choices=incomes)
    bf_m = SelectField(label='Body Fat', choices=bfs)
    bf_c_m = SelectField(label='Body Fat Caliper', choices=bfs)
    bf_f = SelectField(label='Body Fat', choices=bfs)
    bf_c_f = SelectField(label='Body Fat Caliper', choices=bfs)


@app.route('/',methods=['post','get'])
def index():
    form = SimpleForm()
    if form.validate_on_submit():
        print(form.sex.data)
    else:
        print(form.errors)
    return render_template('home.html')


@app.route('/fertility',methods=['post','get'])
def fertility():
    height = request.form.get('height_f') or 60
    weight = request.form.get('weight_f') or 200
    years = request.form.get('age_f') or 18
    months = request.form.get('month') or 0
    end_year = request.form.get('end_year') or 50
    
    form = SimpleForm()
    sim = Simulation(
        years = int(years),
        months = int(months),
        weight = int(weight),
        height = int(height),
        carnivore = True,
        twins = True,
        casual_smoker = False,
        regular_smoker = False,
        end_year = int(end_year),
        ivf_allowed = True,
        size = int(1000),
    )
    sim()

    sample_size = sim.results['sample size']

    return render_template(
        'fertility.html',
        form=form,
        total_children=sim.results['total children'] / sample_size,
        total_children_down_syndrome=sim.results['total children with down syndrome'] / sample_size,
        total_miscarriages=sim.results['total miscarriages'] / sample_size,
        total_still_births=sim.results['total still births'] / sample_size,
        r_0=round(sim.results[0] / sample_size * 100, 2),
        r_1=round(sim.results[1] / sample_size * 100, 2),
        r_2=round(sim.results[2] / sample_size * 100, 2),
        r_3=round(sim.results[3] / sample_size * 100, 2),
        r_4=round(sim.results[4] / sample_size * 100, 2),
        r_5=round(sim.results[5] / sample_size * 100, 2),
        r_6=round(sim.results[6] / sample_size * 100, 2),
        r_7=round(sim.results[7] / sample_size * 100, 2),
        r_8=round(sim.results[8] / sample_size * 100, 2),
        r_9=round(sim.results[9] / sample_size * 100, 2),
        r_10=round(sim.results[10] / sample_size * 100, 2),
    )


@app.route('/smv',methods=['post','get'])
def smv():
    height_m = request.form.get('height_m') or 60
    weight_m = request.form.get('weight_m') or 100
    age_m = request.form.get('age_m') or 18
    income_m = request.form.get('income_m') or 10000
    bf_m = request.form.get('bf_m') or 0
    bf_c_m = request.form.get('bf_m_c') or 0
    
    height_f = request.form.get('height_f') or 60
    weight_f = request.form.get('weight_f') or 100
    age_f = request.form.get('age_f') or 19
    income_f = request.form.get('income_f') or 10000
    bf_f = request.form.get('bf_f') or 0
    bf_c_f = request.form.get('bf_c_f') or 0

    attrs = {}

    attrs_m = {
        'sex': 'male',
        'height': int(height_m),
        'weight': int(weight_m),
        'bodyfat': int(bf_m),
        'bodyfat_c': int(bf_c_m),
        'income': int(income_m),
        'age': int(age_m),
        'state': 'Minnesota',
    }
    attrs_f = {
        'sex': 'female',
        'height': int(height_f),
        'weight': int(weight_f),
        'bodyfat': 0,
        #'bodyfat': int(bf_f),
        'bodyfat_c': 0,
        #'bodyfat_c': int(bf_c_f),
        'income': int(income_f),
        'age': int(age_f),
        'state': 'Minnesota',
    }

    app_m = SMV(debug=True, attrs=attrs_m)
    app_m.age_female = int(age_f)
    calc_smv_m = app_m()
    
    app_m_actual = SMV(debug=True, attrs=attrs_m)
    app_m_actual.age_female = int(age_f)
    app_m_actual.male_actual = True
    calc_smv_m_actual = app_m_actual()

    app_f = SMV(debug=True, attrs=attrs_f)
    calc_smv_f = app_f()

    form = SimpleForm()

    app_f.age = int(age_f) + 5
    app_f.weight = int(weight_f) + 10
    smv_f_5 = app_f()
    percent_f_5 = app_f.percent
    
    app_f.age = int(age_f) + 10
    app_f.weight = int(weight_f) + 20
    smv_f_10 = app_f()
    percent_f_10 = app_f.percent
    
    app_f.age = int(age_f)
    app_f.weight = int(weight_f)
    smv_f_0 = app_f()
    percent_f_0 = app_f.percent

    difference = calc_smv_m - calc_smv_f
    if calc_smv_m < calc_smv_f:
        results_m = 'You are lower SMV than her. If she does get interested in you, then do not get attached. This relationship will probably not last.'
        results_f = 'You are higher SMV than him. You may like him in this moment, but it will not last.'
    elif difference < 1 and difference > -1:
        results_m = 'You are about the same SMV as her. Do not get attached. Her tastes and opinions will eventually change. You will not measure up. Then she will drop you.'
        results_f = 'You are about the same SMV as him. You may like him in this moment, but it will not last.'
    elif difference >= 1 and difference < 2:
        results_m = 'You have a little higher SMV than her. This is probably an appropriate match.'
        results_f = 'You have a little lower SMV than him. You will probably feel satisfied in this relationship.'
    else:
        results_m = 'You have a higher SMV than her. You are out of her league and can do better.'
        results_f = 'You have a lower SMV than him. If he does not recognize his value, then you should consider yourself lucky and try to lock him down.'

    if calc_smv_f >= 8.5:
        results_m = 'She belongs to the streets. Bang and pass.'

    if round(app_m_actual.percent, 1) < 1.0 and round(percent_f_0, 1) > 1.0:
        results_f += '\nYou should recognize that you are dealing with a man in the top 1%. These men are very rare. '
        if calc_smv_m < smv_f_0:
            results_f += ' You may have a higher SMV than him today, but that will not last. You may feel that you are out of his league. You are not. He is probably out of your league and it will probably be difficult to actually lock down a man with as many options as he has.'
        else:
            results_f += ' This man is a rarety. If he is considering you for a long term relationship, then you should attempt to lock him down at any cost. You probably will not get another chance with another man of his caliber.'

    return render_template(
        'smv.html',
        form=form,
        smv_m='SMV: ' + str(calc_smv_m),
        percent_m=str(round(app_m.percent, 1)),
        smv_m_actual='SMV: ' + str(calc_smv_m_actual),
        percent_m_actual=str(round(app_m_actual.percent, 1)),
        smv_f= str(smv_f_0),
        smv_f_5= str(smv_f_5),
        smv_f_10= str(smv_f_10),
        percent_f=str(round(percent_f_0, 1)),
        percent_f_5=str(round(percent_f_5, 1)),
        percent_f_10=str(round(percent_f_10, 1)),
        results_weight_m=app_m.results_weight,
        results_weight_f=app_f.results_weight,
        results_income_m=app_m.results_income,
        results_m=results_m,
        results_f=results_f.split('\n'),
    )


if __name__ == '__main__':
    app.run(debug=True)
