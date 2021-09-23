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
    return render_template('smv.html',form=form)


@app.route('/smv',methods=['post','get'])
def smv():
    height = request.form.get('height')
    weight = request.form.get('weight')
    sex = request.form.get('sex')
    age = request.form.get('age')

    app = SMV(debug=True)

    if sex == '1':
        attrs_m = {
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
        calc_smv = app(attrs_m)
    else:
        attrs_f = {
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
        calc_smv = app(attrs_f)

    return calc_smv


if __name__ == '__main__':
    app.run(debug=True)
