from flask import Flask, render_template, request, url_for, redirect
from models import db, Person, seedData,UserRegistration
from flask_migrate import Migrate, upgrade
from random import randint
from forms import PersonEditForm, PersonNewForm, UserRegistrationForm
from models import User, user_manager
from flask_user import login_required, roles_required, roles_accepted

app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)
user_manager.app = app
user_manager.init_app(app,db,User)


@app.route("/hej")
def hejPage():
    # på riktigt kolla om inloggad osv sov
    lista = ["Stefan", "Oliver", "Josefine"]
    return render_template('hej.html', inloggad=True, lista=lista,age=49, name="Stefan")



@app.route("/")
def indexPage():
    activePage = "startPage"
    allaPersoner = Person.query.all()
    #antalPersoner = Person count???
    #totSaldo = 
    return render_template('startPage.html', antalPersoner=12, totSaldo=999,activePage=activePage)

# To improve: get med defaultvalue
# search!
@app.route("/personer")
#@login_required
# @roles_accepted('Customer', 'Admin') # AND # OR
def personerPage():
    
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))

    searchWord = request.args.get('q','')

    activePage = "personerPage"
    allaPersoner = Person.query.filter(
        Person.namn.like('%' + searchWord + '%') | 
        Person.city.like('%' + searchWord + '%')  | 
        Person.id.like(searchWord)          )

    if sortColumn == "namn":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Person.namn.desc())
        else:
            allaPersoner = allaPersoner.order_by(Person.namn.asc())

    if sortColumn == "city":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Person.city.desc())
        else:
            allaPersoner = allaPersoner.order_by(Person.city.asc())

    if sortColumn == "postal":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Person.postalcode.desc())
        else:
            allaPersoner = allaPersoner.order_by(Person.postalcode.asc())

    paginationObject = allaPersoner.paginate(page,20,False)


    return render_template('personer.html', 
            allaPersoner=paginationObject.items, 
            page=page,
            sortColumn=sortColumn,
            sortOrder=sortOrder,
            q=searchWord,
            has_next=paginationObject.has_next,
            has_prev=paginationObject.has_prev, 
            pages=paginationObject.pages, 
            activePage=activePage)

@app.route("/userconfirmation")
def userConfirmationPage():
    namnet = request.args.get('namn',"")
    return render_template('userconfirmation.html',namn=namnet)

@app.route("/newuser",methods=["GET", "POST"]) 
def userRegistrationPage():
    form = UserRegistrationForm(request.form) 
    if request.method == "GET":
        return render_template('userregistration.html',form=form)
    if form.validate_on_submit():
        userReg = UserRegistration()
        userReg.email = form.email.data
        userReg.firstname = form.firstname.data
        userReg.lastname = form.lastname.data
        userReg.password = form.pwd.data
        userReg.updates = form.updates.data
        db.session.add(userReg)
        db.session.commit()
        return redirect(url_for('userConfirmationPage', namn=form.firstname.data ))

    return render_template('userregistration.html',form=form)




@app.route("/personnew",methods=["GET", "POST"]) 
# @roles_required("Admin")
def personNewPage():
    form = PersonNewForm(request.form) 

    if request.method == "GET":
        return render_template('personnew.html',form=form)

    if form.validate_on_submit():
        personFromDb = Person()
        personFromDb.namn = form.name.data
        personFromDb.city = form.city.data 
        personFromDb.postalcode = str(form.postalcode.data)
        personFromDb.position = form.position.data
        db.session.add(personFromDb)
        db.session.commit()
        return redirect(url_for('personerPage'))

    return render_template('personnew.html',form=form)


@app.route("/person/<id>",methods=["GET", "POST"])  # EDIT   3
# @roles_required("Admin")
def personPage(id):
    form = PersonEditForm(request.form) 
    personFromDb = Person.query.filter(Person.id == id).first()

    if request.method == "GET":
        form.name.data = personFromDb.namn
        form.city.data = personFromDb.city
        form.postalcode.data = int(personFromDb.postalcode)
        form.position.data = personFromDb.position
        return render_template('person.html',person=personFromDb, form=form)
    if form.validate_on_submit():
        personFromDb.namn = form.name.data
        personFromDb.city = form.city.data 
        personFromDb.position = form.position.data
        personFromDb.postalcode = str(form.postalcode.data)
        db.session.commit()
        return redirect(url_for('personerPage'))
    return render_template('person.html',person=personFromDb, form=form)
    




@app.route("/hopp")
def hoppPage():
    return "<html><body><h1>Hopp</h1></body></html>"

@app.route("/personer2")
def personerPage2():
    
    sortColumn = request.args.get('sortColumn',"namn")
    sortOrder = request.args.get('sortOrder', "asc")
    page = request.args.get('page', 1, type=int)

    activePage = "personerPage"
    allaPersoner = Person.query


    if sortColumn == "namn":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Person.namn.desc())
        else:
            allaPersoner = allaPersoner.order_by(Person.namn.asc())

    if sortColumn == "city":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Person.city.desc())
        else:
            allaPersoner = allaPersoner.order_by(Person.city.asc())

    if sortColumn == "postal":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Person.postalcode.desc())
        else:
            allaPersoner = allaPersoner.order_by(Person.postalcode.asc())

    paginationObject = allaPersoner.paginate(page,20,False)

    return render_template('personer.html', 
                    allaPersoner=paginationObject.items, 
            activePage=activePage)



if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run()


