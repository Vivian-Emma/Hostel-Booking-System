from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField, DateField, FileField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class Booking(FlaskForm):
    name = StringField('Enter Your Full Name', validators=[DataRequired()])
    phone = StringField('Enter a valid Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    course = StringField('Course of Study', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    studentId = StringField('Student Id', validators=[DataRequired()])
    relation = StringField('Relationship to emergency contact', validators=[DataRequired()])
    nameOfEmergencyContact = StringField('Name Of Emergency Contact', validators=[DataRequired()])
    emergencyContact = StringField('Emergency Contact', validators=[DataRequired(), Length(min=10, max=10)])
    level = SelectField('Level', choices=[("-Select-", "-Select-"),("100", "100"), ("200", "200"), ("300", "300"),("400", "400"),("500", "500"),("Diploma", "Diploma"),("N/A", "N/A")], validators=[DataRequired()])
    # bookingtype = SelectField('Booking Type', choices=[("-Select-", "-Select-"),("Single-Booking", "Single-Booking"), ("Multiple-Booking", "Multiple-Booking")], validators=[DataRequired()])
    # bookingnumber = IntegerField('Number of Bookings', validators=[DataRequired()])
    # room = SelectField('Select Room', choices=[("-Select-", "-Select-"),("One in a Room", "One in a Room"), ("Two in a Room", "Two in a Room"), ("Four in a room", "Four in a room")], validators=[DataRequired()])
    checkin = DateField('Check in Date', format='%Y-%m-%d')
    # special = SelectField('Special Request or Need', choices=[("-Select-", "-Select-"),("Top Bed", "Top Bed"), ("Down Bed", "Down Bed")])

    submit = SubmitField('Make Payment')

class NewRegistration(FlaskForm):
    firstname = StringField('Enter First Name', validators=[DataRequired()])
    lastname = StringField('Enter Last Name', validators=[DataRequired()])
    email = StringField('Enter E-mail', validators=[DataRequired()])
    phone = IntegerField('Enter a valid Phone Number', validators=[DataRequired()])
    studentid = StringField('Enter Student ID')
    course = StringField('Course of Study', validators=[DataRequired()])
    level = IntegerField('Level', validators=[DataRequired()])
    room = SelectField('Select Room', choices=[("-Select-", "-Select-"),("One in a Room", "One in a Room"), ("Two in a Room", "Two in a Room"), ("Four in a room", "Four in a room")], validators=[DataRequired()])
    checkin = DateField('Arrival Date', format='%Y-%m-%d')
    # special = SelectField('Special Request or Need', choices=[("-Select-", "-Select-"),("Top Floor", "Top Floor"), ("Down Bed", "Down Bed"), ("Ground Floor", "Ground Floor")])
    emergencyname = StringField('Kindly provide an Emergency Contact Name', validators=[DataRequired()])
    emergencyrelationship = StringField('Emergency Relationship', validators=[DataRequired()])
    emergencycontact = IntegerField('Enter Emergency Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    name = StringField('Enter your Full Name', validators=[DataRequired()])
    id = IntegerField('Enter Student ID', validators=[DataRequired()])
    network = SelectField('Select your Network', choices=[("MTN","MTN"), ("VODAFONE","VODAFONE"), ("AIRTELTIGO","AIRTELTIGO")], validators=[DataRequired()])
    amount = IntegerField('Enter Amount', validators=[DataRequired()])
    roomNumber = StringField('Room Number', validators=[DataRequired()])
    phone = StringField('Enter Phone Number', validators=[DataRequired()])
    submit = SubmitField('Pay Now')

class DetailsForm(FlaskForm):
    checkin = DateField('Arrival Date', format='%Y-%m-%d')
    location = SelectField('Room Location', choices=[("-Select-", "-Select-"),("First Floor", "First Floor"), ("Second Floor", "Second Floor"), ("Ground Floor", "Ground Floor")])
    submit = SubmitField('Book Now')
