from flask import render_template, flash, redirect, session, url_for, request
from app import app, db
from .forms import AddExpenseForm, SignupForm, SigninForm
from .models import Account,User,Expense

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':

        newuser = User(form.nickname.data, form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit()

        session['email'] = newuser.email
        session['name'] = newuser.nickname
        #flash("nick is %s" % form.nickname.data)

        return redirect(url_for('expenses', nickname =newuser.nickname))


    if request.method == 'GET':
      return render_template('signup.html', form=form)



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()

    if request.method == 'POST':

        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            user = User.query.filter_by(email = form.email.data.lower()).first()
            return redirect(url_for('expenses', nickname =user.nickname))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)
#View method for displaying the expense sheet detail of a loggged in user.
@app.route('/expenses/<nickname>',methods=['GET', 'POST'])
def expenses(nickname):

    if 'email' not in session:
        return redirect(url_for('signin'))

    form = AddExpenseForm()

    user = User.query.filter_by(nickname = nickname).first()


    user_account_list = Account.query.filter_by(user_id=user.id)
    form.account_type.choices = [(acc.acc_name, acc.acc_name) for acc in user_account_list]
    if user_account_list is None:
        #If the user is logging for the first time, show him an empty sheet.
        return render_template('expense.html',
                           title='Home',
                           user=user,
                           account_list = None,
                           form = form)


    if request.method == 'POST':

        if request.form['submit'] == 'Save Account':
            add_acc = Account( acc_name = request.form['acc_name'], user_name = user)
            db.session.add(add_acc)
            db.session.commit()
            flash('New account has been added.')

        elif request.form['submit'] == 'Save Changes':
            description = request.form['description']
            price  = request.form['price']
            type  = request.form['type']
            account_type = request.form['account_type']

            user_account = Account.query.filter_by(user_id=user.id,
                                           acc_name = account_type).first()

            add_into = Expense(description = description, price=price, type=type, acc=user_account)
            db.session.add(add_into)
            db.session.commit()
            flash('Your changes have been saved.')

        elif request.form['submit'] == 'Search':
            total_expense_list = []
            search_key = request.form['keytype']
            search_str = request.form['key']
            if search_key == 'type':
                exp_obj = Expense.query.filter(Expense.type.ilike('%'+search_str+'%'))
            elif search_key == 'desc':
                 exp_obj = Expense.query.filter(Expense.description.ilike('%'+search_str+'%'))
            elif search_key == 'acc_name':
                exp_obj = Expense.query.filter(Expense.acc.acc_name.ilike('%'+search_str+'%'))


            total_balance=0
            total_expense_list.append(exp_obj)

            for exp in exp_obj:
                total_balance = total_balance + exp.price
            return render_template('expense.html',
                           title='Home',
                           user=user,
                           account_list = user_account_list,
                           expense_list = total_expense_list,
                           total_balance = total_balance,
                           form = form
                           )

            #flash('Key: %s' %exp_obj[0].price)
        #return redirect(url_for('expenses'))

    total_expense_list=[]
    total_balance=0

    for accounts in user_account_list:

        ExpenseList = Expense.query.filter_by(acc_id = accounts.id)
        total_expense_list.append(ExpenseList)
        for exp in ExpenseList:
            total_balance = total_balance + exp.price

    #form.account_type.choices = [(acc.acc_name, acc.acc_name) for acc in user_account_list]

    return render_template('expense.html',
                           title='Home',
                           user=user,
                           account_list = user_account_list,
                           expense_list = total_expense_list,
                           total_balance = total_balance,
                           form = form
                           )


@app.route('/logout')
def logout():

  if 'email' not in session:
    return redirect(url_for('signin'))

  session.pop('email', None)
  return redirect(url_for('signup'))
