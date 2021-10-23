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

    commentary_m = ""
    commentary_f = ""

    if calc_smv_m < calc_smv_f:
        commentary_m += 'You are lower SMV than her. If she does get interested in you, then do not get attached. This relationship will probably not last.'
        commentary_f += 'You are higher SMV than him. You may like him in this moment, but it will not last.'
    elif difference < 1 and difference > -1:
        commentary_m += 'You are about the same SMV as her. Do not get attached. Her tastes and opinions will eventually change. You will not measure up. Then she will drop you.'
        commentary_f += 'You are about the same SMV as him. You may like him in this moment, but it will not last.'
    elif difference >= 1 and difference < 2:
        commentary_m += 'You have a little higher SMV than her. This is probably an appropriate match.'
        commentary_f += 'You have a little lower SMV than him. You will probably feel satisfied in this relationship.'
    else:
        commentary_m += 'You have a higher SMV than her. You are out of her league and can do better.'
        commentary_f += 'You have a lower SMV than him. If he does not recognize his value, then you should consider yourself lucky and try to lock him down.'

    if calc_smv_f >= 8.5:
        commentary_m += 'She belongs to the streets. Bang and pass.'

    if calc_smv_m >= calc_smv_f:
        commentary_m += '\nYour SMV is greater than or equal to her SMV. First, you are not entitled to her. '
        commentary_m += 'She is a human being with needs/wants/desires of her own. You are well situated to '
        commentary_m += 'attract this woman, but it will not matter if you have poor Game. Game indicates that '
        commentary_m += 'you have options and that she is one of many. Next, she has to believe that you can do better '
        commentary_m += 'but that you are choosing her. If she believes that she can better, then your days are '
        commentary_m += 'numbered.'

    if round(app_m_actual.percent, 1) < 1.0 and round(percent_f_0, 1) > 1.0:
        commentary_f += '\nYou should recognize that you are dealing with a man in the top 1%. These men are very rare. '
        if calc_smv_m < smv_f_0:
            commentary_f += ' You may have a higher SMV than him today, but that will not last. You may feel that you are out of his league. You are not. He is probably out of your league and it will probably be difficult to actually lock down a man with as many options as he has.'
        else:
            commentary_f += ' This man is a rarety. If he is considering you for a long term relationship, then you should attempt to lock him down at any cost. You probably will not get another chance with another man of his caliber.'
    if round(app_m_actual.percent, 1) < 1.0:
        commentary_m += '\nYou are in the top one percent. This model does not take Game into account. '
        commentary_m += 'You apparently have everything.\nIf you are still having problems with women, '
        commentary_m += 'then it is because your Game sucks. Women will be attracted to you at first '
        commentary_m += 'because you "Check off all the boxes", but they will lose attraction to you. It '
        commentary_m += 'will confuse them because they will not know why they just don\'t "vibe" with you '
        commentary_m += '(Even though they want to). The reason why this is confusing is because it is '
        commentary_m += 'incongruent. A man who has "everything" should have game. He should have abundance. '
        commentary_m += 'He shouldn\'t care about her because he has many options. Work on your Game. Dammit.'

    commentary_m += app_m.results_weight + "\n"
    commentary_f += app_f.results_weight + "\n"

    commentary_m += app_m.results_income
    
    if app_f.income > app_m.income:
        commentary_m += " She makes more money than you. Women want you to make at least 125% of what they make."
        commentary_f += " You make more money than him. You may be fine with that for the moment. However, you are going grow resentful of his 'lack of ambition', laziness, etc."
    elif (app_f.income * 1.25) > app_m.income:
        commentary_m += " You do not make enough money. Women want you to make at least 125% of what they make."
        commentary_f += " He does not make enough money. You may be fine with it for now and he does make the same or more money than you. However, you are going to grow resentful of his 'lack of ambition', laziness, etc."

    commentary_m += "\n"
    commentary_f += "\n"

    if app_m.height < 69:
        commentary_m += "You have below average height. There's nothing that you can do about that. What you can do is get out and work on yourself. Improve your career, make more money, and hit the gym.\n"
    elif app_m.height == 69:
        commentary_m += "You have average height. There's nothing that you can do about that. What you can do is get out and work on yourself. Improve your career, make more money, and hit the gym.\n"
    elif app_m.height < 72:
        commentary_m += "Your height is below six feet tall. There's nothing that you can do about that. What you can do is get out and work on yourself. Improve your career, make more money, and hit the gym.\n"

    if app_f.age >= 36:
        commentary_m += "She is in the Alpha-Reinterest phase of her life. During this time, she will prioritise physical and other traits that allow her to 'flex' over her girlfriends. She does still desire Beta long term traits, but Alpha traits have regained priority. If you are looking for a woman in this stage of life, then you should focus on your health. If you haven't accomplished anything, then focus on your life and make something of yourself.\n"
    elif app_f.age >= 26:
        commentary_m += "She is in the Beta-Long Term phase of her life. She has started to consider consider your income and look for a man that may better provide security. Alpha traits are still important, but she is starting to get baby rabbies. Be careful not to be the guy that is good enough for now. She should want to have YOUR child, not just have a child. If you are looking for a woman in this stage of life, then focus on your purpose and become successful.\n"
    else:
        commentary_m += "She is in the Alpha-Short Term phase of her life. She pretty much only cares about physical traits. Do you have a six pack? Are you over six feet tall. At this age she has little to no concept of money and how one earns it. She may want a guy who makes six figures, but she probably doesn't know that that takes. If you are looking for women in this stage of life, then work out and get in the best shape of your life.\n"

    return render_template(
        'smv.html',
        form=form,
        smv_m=str(calc_smv_m),
        percent_m=str(round(app_m.percent, 1)),
        smv_m_actual=str(calc_smv_m_actual),
        percent_m_actual=str(round(app_m_actual.percent, 1)),
        smv_f= str(smv_f_0),
        smv_f_5= str(smv_f_5),
        smv_f_10= str(smv_f_10),
        percent_f=str(round(percent_f_0, 1)),
        percent_f_5=str(round(percent_f_5, 1)),
        percent_f_10=str(round(percent_f_10, 1)),
        commentary_m=commentary_m.split('\n'),
        commentary_f=commentary_f.split('\n'),
    )


if __name__ == '__main__':
    app.run(debug=True)
