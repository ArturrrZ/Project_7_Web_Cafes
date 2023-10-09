from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, URLField,SelectField
from wtforms.validators import DataRequired, Email, Length, URL
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] =('sqlite:///cafes.db')
db = SQLAlchemy()
db.init_app(app)
#
class AddForm(FlaskForm):
    name = StringField(label='Name of cafe:', validators=[DataRequired(message='Give me data BRUH')])
    url_map = StringField(label='Address link:', validators=[DataRequired(),URL() ])
    url_img = StringField(label='Picture Link:', validators=[DataRequired(), URL()])
    location=StringField(label='Their Location:',validators=[DataRequired()])
    seats=StringField(label='Amount of seats:',validators=[DataRequired()])
    toilet=SelectField(label='Does it have a restroom?',validators=[DataRequired()],choices=[('True', 'True'), ('False', 'False')])
    wifi=SelectField(label='Is there a WiFi?',validators=[DataRequired()],choices=[('True', 'True'), ('False', 'False')])
    sockets=SelectField(label='Are there any sockets?',validators=[DataRequired()],choices=[('True', 'True'), ('False', 'False')])
    calls=SelectField(label='Can people there take calls?',validators=[DataRequired()],choices=[('True', 'True'), ('False', 'False')])
    price=StringField(label="What's the coffee price $?",validators=[DataRequired()])
    submit=SubmitField(label='Submit')


class cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {old.name: getattr(self, old.name) for old in self.__table__.columns}
with app.app_context():
    db.create_all()


#
# with app.app_context():
#     result = db.session.execute(db.select(cafe).order_by(cafe.name))
#     all_books = result.scalars().all()
# for book in all_books:
#     print(book.has_wifi)
#     # if book.has_wifi:

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/all_cafes")
def all_cafes():
    result = db.session.execute(db.select(cafe).order_by(cafe.name))
    all_cafes = result.scalars().all()
    return render_template('all.html',all_cafes=all_cafes)

@app.route("/add_new", methods=['GET','POST'])
def add_new():
    add_cafe=AddForm()
    if add_cafe.validate_on_submit():
        new_cafe=cafe(
        name = add_cafe.name.data,
        map_url = add_cafe.url_map.data,
        img_url=add_cafe.url_img.data,
        location=add_cafe.location.data,
        seats = add_cafe.seats.data,
        has_toilet =add_cafe.toilet.data == 'True'  ,
        has_wifi = add_cafe.wifi.data== 'True' ,
        has_sockets = add_cafe.sockets.data== 'True' ,
        can_take_calls =add_cafe.calls.data == 'True' ,
        coffee_price = add_cafe.price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        print("submitted")
        return redirect(url_for('all_cafes'))

    return render_template('add.html',form=add_cafe)

@app.route("/show_cafe/<int:cafe_id>")
def show_cafe(cafe_id):
    showed_cafe=db.get_or_404(cafe,cafe_id)
    return render_template('show_cafe.html', cafe=showed_cafe)

if __name__ == "__main__":
    app.run(debug=False)


