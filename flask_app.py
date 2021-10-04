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

    return render_template(
        'fertility.html',
        form=form,
        total_children=sim.total_children_percent,
        total_children_down_syndrome=sim.total_children_with_down_syndrome_percent,
        total_miscarriages=sim.total_miscarriages_percent,
        total_still_births=sim.total_still_births_percent,
    )


@app.route('/smv',methods=['post','get'])
def smv():
    height_m = request.form.get('height_m') or 60
    weight_m = request.form.get('weight_m') or 200
    age_m = request.form.get('age_m') or 30
    income_m = request.form.get('income_m') or 40000
    bf_m = request.form.get('bf_m') or 0
    bf_c_m = request.form.get('bf_m_c') or 0
    
    height_f = request.form.get('height_f') or 60
    weight_f = request.form.get('weight_f') or 200
    age_f = request.form.get('age_f') or 30
    income_f = request.form.get('income_f') or 40000
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
        'bodyfat': int(bf_f),
        'bodyfat_c': int(bf_c_f),
        'income': int(income_f),
        'age': int(age_f),
        'state': 'Minnesota',
    }

    app_m = SMV(debug=True, attrs=attrs_m)
    app_m.age_female = int(age_f)
    calc_smv_m = app_m()

    app_f = SMV(debug=True, attrs=attrs_f)
    calc_smv_f = app_f()

    form = SimpleForm()

    return render_template(
        'smv.html',
        form=form,
        smv_m=str(calc_smv_m),
        percent_m=str(round(app_m.percent, 1)),
        smv_f=str(calc_smv_f),
        percent_f=str(round(app_f.percent, 1)),
    )


if __name__ == '__main__':
    app.run(debug=True)
