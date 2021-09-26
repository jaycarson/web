from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField
from SMV import SMV


SECRET_KEY = 'development'


app = Flask(__name__)
app.config.from_object(__name__)


class SimpleForm(FlaskForm):
    ages = []
    for x in range(18, 100):
        ages.append((x, x))
    
    weights = []
    for x in range(100, 400):
        weights.append((x, x))
    
    heights = []
    for x in range(60, 84):
        heights.append((x, x))

    sex = SelectField(label='Sex', choices=[(1,'Male'), (2,'Female')])
    age = SelectField(label='Age', choices=ages)
    weight = SelectField(label='Weight', choices=weights)
    height = SelectField(label='Height', choices=heights)


@app.route('/',methods=['post','get'])
def index():
    form = SimpleForm()
    if form.validate_on_submit():
        print(form.sex.data)
    else:
        print(form.errors)
    return render_template('base.html')


@app.route('/fertility',methods=['post','get'])
def fertility():
    form = SimpleForm()
    return render_template('fertility.html', form=form)


@app.route('/smv',methods=['post','get'])
def smv():
    height = request.form.get('height') or 60
    weight = request.form.get('weight') or 2000
    sex = request.form.get('sex') or '1'
    age = request.form.get('age') or 30

    attrs = {}

    if sex == '1':
        attrs = {
            'sex': 'male',
            'height': int(height),
            'weight': int(weight),
            'bodyfat': 0,
            'bodyfat_c': 0,
            'income': 135000,
            'age': int(age),
            'min_a': 25,
            'max_a': 45,
            'state': 'Minnesota',
        }
    else:
        attrs = {
            'sex': 'female',
            'height': int(height),
            'weight': int(weight),
            'bodyfat': 0,
            'bodyfat_c': 0,
            'income': 35000,
            'age': int(age),
            'min_a': 18,
            'max_a': 45,
            'state': 'Minnesota',
        }

    app = SMV(debug=True, attrs=attrs)
    calc_smv = app()

    form = SimpleForm()

    return render_template('smv.html', form=form, content=str(calc_smv))


if __name__ == '__main__':
    app.run(debug=True)
