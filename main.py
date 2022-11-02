from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
# Secret key used in our flask application
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# Our FlaskForm object declaration. Specifies that our form has a name, location, opening time,
# closing time, coffee rating, etc. Also has appropriate Field types and validators.
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                              validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


# add.html page that handles form submission for adding a new cafe into our table
@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    # Checks if valid form submission received from "POST", then writes new entry into
    # cafe-data.csv file and redirects to our cafes.html page
    if form.validate_on_submit():
        newdata = [form.cafe.data, form.location.data, form.open_time.data, form.closing_time.data,
                   form.coffee_rating.data, form.wifi_rating.data, form.power_rating.data]

        with open('cafe-data.csv', 'a', newline='', encoding="utf-8") as csvfile:
            cafewriter = csv.writer(csvfile, delimiter=",")
            cafewriter.writerow(newdata)
        # Obsolete code that redirect + url_for cafes replaced.
        # with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        #     csv_data = csv.reader(csv_file, delimiter=',')
        #     list_of_rows = []
        #     for row in csv_data:
        #         list_of_rows.append(row)
        # return render_template('cafes.html', cafes=list_of_rows)
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


# Our cafes.html page showing a table that pulls data entries from cafe-data.csv file
# "utf-8" encoding needed otherwise an error for improper file type
@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
