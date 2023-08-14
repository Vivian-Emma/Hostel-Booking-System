from flask import Flask,redirect,url_for,render_template,request, session
import urllib3
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import httpx
import csv
import requests
import urllib.request, urllib.parse
from datetime import datetime
from forms import DetailsForm 


app=Flask(__name__)
app.config['SECRET_KEY'] = '5791628basdfsabca32242sdfsfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.String(), nullable=True)
    number = db.Column(db.Integer(), nullable=True)
    maxOccupancy = db.Column(db.Integer(), nullable = True)
    occupancyStatus = db.Column(db.String(), nullable = True)
    occupants = db.Column(db.Integer(), nullable = True)
    bedsAvailable = db.Column(db.Integer(), nullable = True)
    floor = db.Column(db.String(), nullable = True)
    tier = db.Column(db.String(), nullable = True)
    price = db.Column(db.Float(), nullable = True)
    roomtype = db.Column(db.String(), nullable = True)
    slots = db.Column(db.Integer(), nullable = True)
    space = db.Column(db.Boolean(), default=False)

    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Block('{self.number}', Room('{self.number}', Occupancy- '{self.occupancyStatus}', )"


class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    range = db.Column(db.String(), nullable=True)
    basic = db.Column(db.Float(), nullable=True)
    premium = db.Column(db.Float(), nullable=True)
    space = db.Column(db.Boolean(), default=True)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Room Type('{self.name}', Space('{self.space}', )"

class Blocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=True)
    paid = db.Column(db.Float(), nullable=True, default=0)
    outstanding = db.Column(db.Float(), nullable=True, default=0)
    due = db.Column(db.Float(), nullable=True, default=0)

    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Blocks ('{self.name}', Space('{self.space}', )"


class RoomLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(), nullable=True)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Room Type('{self.name}', Space('{self.space}', )"

class Occupant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    studentId = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    course = db.Column(db.String(), nullable=True)
    level = db.Column(db.String(), nullable=True)
    room = db.Column(db.String(), nullable=True)
    block = db.Column(db.String(), nullable=True)
    roomnumber = db.Column(db.String(), nullable=True)
    roomid = db.Column(db.String(), nullable=True)
    roomCost = db.Column(db.Float(), nullable=True, default=0)
    amountPaid = db.Column(db.Float(), nullable=True, default=0)
    due = db.Column(db.Float(), nullable=True)
    paid = db.Column(db.Boolean(), default=False)

def __repr__(self): 
    return f"Occupant('{self.name}', Room('{self.roomnumber}', Paid- '{self.occupancyStatus}', )"

@app.route('/roomtype', methods=['GET', 'POST'])
def roomtype():
    roomtype = RoomType.query.all()
    return render_template('roomtype.html', roomtype=roomtype)

# @app.route('/blocks/<string:roomtype>', methods=['GET', 'POST'])
# def blocks(roomtype):
#     print(roomtype)
#     roomtype = RoomLocation.query.all()
#     return render_template('location.html', roomtype=roomtype)

@app.route('/location/<string:roomtype>/<string:tier>', methods=['GET', 'POST'])
def location(roomtype, tier):
    print(roomtype)
    session["roomtype"] = roomtype
    session["roomtier"] = tier
    roomtype = RoomLocation.query.all()
    return render_template('location.html', roomtype=roomtype)

@app.route('/rooms/<string:id>', methods=['GET', 'POST'])
def rooms(id):
    block = id

    session["roomlocation"] = id

    floor = RoomLocation.query.get_or_404(id)

    print("floor")
    floor = floor.location

    roomtype = session['roomtype']
    print(roomtype)

    # allrooms = Room.query.filter_by(block=block).order_by(Room.number.asc()).all()
    allrooms = Room.query.filter_by(maxOccupancy = roomtype, floor= floor, price=session["roomtier"], space=True).all()
    # allrooms = Room.query.all()
    print(allrooms)
    return render_template('rooms.html', rooms=allrooms, block=block)


@app.route('/allrooms/<string:id>', methods=['GET', 'POST'])
def allrooms(id):
    block = id
    session["roomlocation"] = id
    allrooms = Room.query.filter_by(block=block).all()
    print(allrooms)
    return render_template('allrooms.html', rooms=allrooms, block=block)

@app.route('/blocks', methods=['GET', 'POST'])
def block():
    allbocks = Blocks.query.all()
    return render_template('blocks.html', blocks = allbocks)

@app.route('/occupants', methods=['GET', 'POST'])
def occupants():
    alloccupants = Occupant.query.order_by(Occupant.id.desc()).all()
    return render_template("occupants.html", alloccupants = alloccupants)


def sendRancardMessage(phone,message):
    url = "https://unify-base.rancard.com/api/v2/sms/public/sendMessage"
    message = {
        "apiKey": "dGFsYW5rdTpUYWxhbmt1Q3U6MTY1OkFQSWtkczAxNDI0Nzg1NDU=",
        "contacts": [phone],
        "message": message,
        "scheduled": False,
        "hasPlaceholders": False,
        "senderId": "Pronto"
    }
    r = requests.post(url, json=message)
    print(r.text)
    return r.text


@app.route('/form',methods=['GET','POST'])
def pronto():
    form=Booking()

    if request.method=='POST':
        if form.validate_on_submit():
            newOccupant = Occupant(
                name = form.name.data,
                phone = form.phone.data,
                # studentId = form.studentid.data,
                course = form.course.data,
                level = form.level.data,
            )

            db.session.add(newOccupant)
            db.session.commit()
            session['occupantId'] = newOccupant.id

        
            return redirect(('https://sandbox.prestoghana.com/pay/myhostel' ))
            # return redirect(url_for('roomtype' ))
        
        else:
            print(form.errors)
        return render_template('pronto.html', form=form)
    return render_template('pronto.html', form=form)


@app.route('/extractDatacsv', methods=['GET', 'POST'])
def extractDatacsv():
    with open('Documents/ROOMS.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csvData = []

        for r in Room.query.all():
            db.session.delete(r)
            db.session.commit()


        for row in csv_reader:
            print(row)
            csvData.append(row)
            newRoom = Room(block=row["BLOCK"], floor=row["FLOOR"], number=row["ROOM_NUMBER"], roomtype=row["ROOM_TYPE"], maxOccupancy=row["MAX_OCCUPANCY"], occupants=row["OCCUPANTS"], price=row["PRICE"], bedsAvailable=row["MAX_OCCUPANCY"], tier = row["TIER"], space=True )
            db.session.add(newRoom)
        
        db.session.commit()

        return csvData
    

@app.route('/extractroomtypecsv', methods=['GET', 'POST'])
def extractroomtypecsv():
    with open('Documents/ROOM_TYPE.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csvData = []

        for row in csv_reader:
            print(row)
            csvData.append(row)
            newRoom = RoomType(name=row["ROOM_TYPE"], range=row["PRICE_RANGE"], basic=row["BASIC"], premium=row["PREMIUM"] )
            db.session.add(newRoom)
        
        db.session.commit()

        return csvData
    


@app.route('/extractroomlocationcsv', methods=['GET', 'POST'])
def extractroomlocationcsv():
    with open('Documents/ROOM_LOCATION.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csvData = []

        for row in csv_reader:
            print(row)
            csvData.append(row)
            newRoom = RoomLocation(floor=row["FLOOR"], location=row["ROOM_LOCATION"])
            db.session.add(newRoom)
        
        db.session.commit()

        return csvData
    

    
@app.route('/route_name', methods=['GET', 'POST'])
def extractCsv(filename):
     with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            number = line['number']

            id = id.split('-')[0]
            if status == 'paid' and len(id) <= 3:
                amount = line['amount']

                print(str(id) + " - " + amount)
            
                # find candidate and add amount to votes ... 
                candidate = Candidates.query.get_or_404(id)
                candidate.votes += float(amount)
                print(str(id) + " - " + amount)

        db.session.commit()
        all = []
        candidates = Candidates.query.all()
        for candidate in candidates:
            candidate = {
                candidate.name:candidate.votes
            }
            all.append(candidate) 
        return make_response(all)




@app.route('/new',methods=['GET','POST'])
def new():
    form=NewRegistration()
    if request.method=='POST':
        # Handle POST Request here
        return render_template('new.html')
    return render_template('new.html', form=form)

@app.route('/payment/<string:id>', methods=['GET', 'POST'])
def payment(id):
    form=PaymentForm()
    print(id)
    session["roomnumber"] = id
    form.roomNumber.data = "Block " + session["roomlocation"] + "Room "+ session["roomnumber"]
    occupant = Occupant.query.get_or_404(session['occupantId'])
    room = Room.query.get_or_404(id)
    
    try:
        occupant.roomCost = float(room.price)
        occupant.roomid = room.id
        db.session.commit()
    except Exception as e:  
        print(e)


    if request.method == 'POST':
        if form.validate_on_submit:
            print("validated")
            baseUrl = "https://sandbox.prestoghana.com"
            paymentUrl = "https://sandbox.prestoghana.com/korba"
            min = float(room.price)*0.60
            if form.amount.data == None:
                form.amount.data = min
            paymentInfo = {
                    "appId":"prontohostel",
                    "ref":form.name.data,
                    "reference":str(form.id.data),
                    "description":str(form.id.data),
                    "paymentId":form.id.data, 
                    "phone":"0"+str(form.phone.data[-9:]),
                    "amount":form.amount.data,
                    "total":str(form.amount.data), #TODO:CHANGE THIS!
                    "recipient":"external", #TODO:Change!
                    "percentage":"5",
                    "callbackUrl":baseUrl+"/notify/",#TODO: UPDATE THIS VALUE
                    "firstName":form.name.data,
                    "network":form.network.data,
                }
     
            r = httpx.post(paymentUrl, json=paymentInfo)
            print(r)

            sendsms(str(paymentInfo["paymentId"]), paymentInfo["firstName"],paymentInfo["description"], "web", paymentInfo["phone"], )
            updateOccupant(paymentInfo["amount"], occupant)
            return "Done!"
        else:
            print(form.errors)
            
    else:
        room = Room.query.get_or_404(id)
        print(room.price)
        min = float(room.price)*0.60
        print("This is a get request")

        occupant = Occupant.query.get_or_404(session["occupantId"])
        occupant.room = room.number
        occupant.block = room.block
        db.session.commit()

        form.name.data = occupant.name
        form.phone.data = occupant.phone
        form.amount.data = min
        form.roomNumber.data ="Block " + room.block +" Room " +str(room.number)
    return render_template('payment.html', form=form, occupant=occupant, minAmount=min, maxAmount=room.price)


def updateOccupant(amount, occupant):
    # update balance
    amountBalance = occupant.roomCost - float(amount) #6000 - 3000 = 3000
    # update block 
    block = Blocks.query.get_or_404(occupant.block) #find Block
    block.paid += amount #Update amount paid per block

    # update room
    # update 
    
    # Room cost - amount paid
    
    # Current balance + amount paid
    occupant.amountPaid += amount
    occupant.due = amountBalance #wrong
    outstanding = occupant.roomCost - amount
    
    block.due += occupant.roomCost
    block.outstanding += outstanding

    # set room to hidden if full
    room =  Room.query.get_or_404(occupant.roomid)
    room.occupants += 1
    room.bedsAvailable -= 1
    
    db.session.commit()

    if room.bedsAvailable <= 0:
        room.space = False
        db.session.commit()

    sendTelegram("Block " + str(room.block)+ " Room " + str(room.number) + "has been purchased successfully by "+ str(occupant.name)+ " " + str(occupant.phone)+ ".\nAmount Paid "+ str(amount) + "\nRemaining Beds: "+ str(room.bedsAvailable))
    
    return occupant
# -------------- ADMIN -----------

@app.route('/resetDashboard', methods=['GET', 'POST'])
def resetDashboard():
    for b in Blocks.query.all():
        b.paid = 0
        b.outstanding = 0
        b.due = 0
    
    for o in Occupant.query.all():
        db.session.delete(o)

    db.session.commit()

    return "Done!"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    occupants = Occupant.query.all()
    totalOccupants = Occupant.query.count()
    paid = 0
    due = 0
    for o in occupants:
        if o.amountPaid:
            paid +=  o.amountPaid 
        if o.due:
            due += o.roomCost
    
    totalNumberOfBeds = 0

    for r in Room.query.all():
        totalNumberOfBeds += r.maxOccupancy

    availableBeds = totalNumberOfBeds-totalOccupants
    occupancyRate = totalNumberOfBeds/availableBeds

    print("totalNumberOfBeds:" + str(totalNumberOfBeds))
    print("availableBeds:" + str(availableBeds))
    # print("totalNumberOfBeds:" + totalNumberOfBeds)

    occupancyRate = round(occupancyRate/100, 2)
    amountOutstanding =  due - paid

    # for bed in beds:


    
    return render_template('dashboard.html', occupancyRate=str(occupancyRate)+"%",outstanding=amountOutstanding, paid=paid, due=due, tenants="6000")

@app.route('/allblocks/<string:id>', methods=['GET', 'POST'])
@app.route('/allblocks', methods=['GET', 'POST'])
def allblocks(id="0"):
    print(id)
    blocks = Blocks.query.all()
    filterDict = {
        "0":"All",
        "1":"outstanding",
        "2":"due",
        "3":"paid"
    }
    print(filterDict[id])
    return render_template('allblocks.html', blocks=blocks, filter=filterDict[id])

@app.route('/adminblock/<int:id>', methods=['GET', 'POST'])
def adminblock(id):
    occupants = Occupant.query.filter_by(block = id).all()
    print(occupants)
    return render_template('adminoccupants.html', alloccupants=occupants)

@app.route('/master', methods=['GET', 'POST'])
def master():

    return render_template('master.html')


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route('/details', methods=['GET', 'POST'])
def details():
    form = DetailsForm()
    if form.validate_on_submit():
        # Handle POST Request here
        return redirect(url_for('form'))  # Redirect to the 'new_route' function
    
    return render_template('details.html', form=form)

@app.route('/details1', methods=['GET', 'POST'])
def details1():
    form = DetailsForm()
    if form.validate_on_submit():
        # Handle POST Request here
        return redirect(url_for('form'))  # Redirect to the 'new_route' function
    
    return render_template('details1.html', form=form)

@app.route('/details2', methods=['GET', 'POST'])
def details2():
    form = DetailsForm()
    if form.validate_on_submit():
        # Handle POST Request here
        return redirect(url_for('form'))  # Redirect to the 'new_route' function
    
    return render_template('details2.html', form=form)

@app.route('/details3', methods=['GET', 'POST'])
def details3():
    form = DetailsForm()
    if form.validate_on_submit():
        # Handle POST Request here
        return redirect(url_for('form'))  # Redirect to the 'new_route' function
    
    return render_template('details3.html', form=form)

@app.route('/viewrooms', methods=['GET', 'POST'])
def viewrooms():

    return render_template('viewrooms.html')

@app.route('/faq', methods=['GET', 'POST'])
def faq():

    return render_template('faq.html')

# @app.route('/sendTelegram', methods=['GET', 'POST'])
def sendTelegram(params):
    url = "https://api.telegram.org/bot5873073506:AAGRf5b4sjmEzDUbApytx4lKoew_WbdrGsA/sendMessage?chat_id=-839615923&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    return content

@app.route('/sendsms', methods=['GET', 'POST'])
def sendsms(recieptNumber, guestName, bookingReference, paymentMethod, phone):

    message = "Receipt Number:" +recieptNumber + "\n Date: "+ datetime.utcnow().strftime('%c') + "\nGuest Name:" + guestName + "\nBooking Reference: " + bookingReference + "\nPayment Method: " + paymentMethod + "\nReview occupancy terms and conditions here. \nDial *192*456*908# and use your booking reference to make future payments during your occupancy term. \nThank you for choosing Pronto Hostels. We hope you have a great stay with us!"
    r = sendRancardMessage(phone ,message)
    print(r)
    return "r"

# @app.route('/route_name', methods=['GET', 'POST'])
# def method_name():
#        paymentInfo = {
#             "appId":"pronto",
#             "ref":payment.ref,
#             "reference":payment.ref,
#             "paymentId":payment.id, 
#             "phone":"0"+payment.account[-9:],
#             "amount":payment.amount,
#             "total":payment.total,
#             "recipient":"payment", #TODO:Change!
#             "percentage":"3",
#             "callbackUrl":prestoHerokuUrl+"prontoconfirm/"+str(payment.id),#TODO: UPDATE THIS VALUE
#             "firstName":payment.account,
#             "network":mobileNetwork,
#         }

#     r = httpx.post(url, json = paymentInfo)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, host='0.0.0.0', debug=True)