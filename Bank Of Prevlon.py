import clrprint
from clrprint import *
import mysql.connector
from flask import Flask, render_template, request,session
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, flash, redirect, url_for
from datetime import datetime
from werkzeug.security import check_password_hash

def amount(x):
    amo=x
    string=" "
    count=0
    balance=str(amo)
    if len(balance)>=4:
        enquiry=balance[-3:]
        varaible=balance[0:-3]
        leng=len(varaible)
        if leng%2==0:
            count=0
        else:
            count=1
        for i in varaible:
            string=string+i
            count=count+1
            if count==2:
                string=string+","
                count=0
        balance=string+enquiry
        return balance
    else:
        return balance

app = Flask(__name__,template_folder='templates',static_url_path='/static')
app.secret_key = 'pavankumarpilaka' 
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/transcition')  # Change the route as needed
def transcition():
    return render_template('transcition.html')




mycon=mysql.connector.connect(host="localhost",user="root",passwd="password",database="bank")
cursor=mycon.cursor()
cursor.execute("select * from  login_details")
data=cursor.fetchall()
user=0

@app.route('/send')  # Change the route as needed
def send_money_page():
    return render_template('send.html')

@app.route('/deposit')  # Change the route as needed
def deposit_money_page():
    return render_template('deposit.html')

@app.route('/balance')  # Change the route as needed
def checkbalance():
    return render_template('balance.html')

@app.route('/withdraw')  # Change the route as needed
def withdraw_money_page():
    return render_template('withdraw.html')

@app.route('/balance-money', methods=['POST'])
def balance_money():
    try:
        mycon = mysql.connector.connect(host="localhost", user="root", passwd="password", database="bank")
        cursor = mycon.cursor(buffered=True)

        phoneno = str(request.form.get('phone'))
        passw = str(request.form.get('balpass'))

        cursor.execute('SELECT * FROM data WHERE phonenumber = %s', (phoneno,))
        balance_details = cursor.fetchone()

        if balance_details and balance_details[4] == passw:
            balan = balance_details[3]
            balan=amount(balan)
            # Assuming amount() is a function to format the balance, replace it with your logic.
            # This example assumes the balance is in INR.
            formatted_balance = f'₹ {balan}'  # Formatting balance with currency symbol
            flash(f'Your balance fetched successfully. Your balance is {formatted_balance}', 'success')
        else:
            flash('Invalid phone number or password', 'error')

        mycon.commit()

    except mysql.connector.Error as err:
        mycon.rollback()
        flash(f"Error: {err}", 'error')

    finally:
        cursor.close()
        mycon.close()

    return render_template('balance.html')

@app.route('/withdraw-money', methods=['POST'])
def withdraw_money():
    try:
        mycon = mysql.connector.connect(host="localhost", user="root", passwd="password", database="bank")
        cursor = mycon.cursor(buffered=True)

        withdraw_no = str(request.form.get('withdraw'))
        depo_pass = str(request.form.get('withpass'))
        amount = float(request.form.get('amount'))

        cursor.execute('SELECT * FROM data WHERE phonenumber = %s', (withdraw_no,))
        withdraw_details = cursor.fetchone()

        # Check if the withdraw_details exist and password matches
        if withdraw_details and withdraw_details[4] == depo_pass:
            balan = withdraw_details[3]
            new_bal = balan - amount

            # Check if the new balance will be greater than or equal to zero
            if new_bal >= 0:
                # Update balance
                cursor.execute("UPDATE data SET balance = %s WHERE phonenumber = %s", (new_bal, withdraw_no))

                current_date = datetime.now().date()
                current_time = datetime.now().time()

                # Insert transaction history
                insert_transaction_query = "INSERT INTO transcition_history (username, date_of_transcition, time_of_transcition, withdraw) VALUES (%s, %s, %s, %s)"
                transaction_data_receiver = (withdraw_no, current_date, current_time, amount)
                cursor.execute(insert_transaction_query, transaction_data_receiver)

                mycon.commit()
                flash('Transaction successful', 'success')
            else:
                flash('Insufficient balance', 'error')
        else:
            flash('Invalid phone number or password', 'error')

    except mysql.connector.Error as err:
        mycon.rollback()
        flash(f"Error: {err}", 'error')

    finally:
        cursor.close()
        mycon.close()

    return render_template('withdraw.html')


@app.route('/deposit-money', methods=['POST'])
def deposit_money():
    try:
        mycon = mysql.connector.connect(host="localhost", user="root", passwd="password", database="bank")
        cursor = mycon.cursor(buffered=True)

        deposit_no = str(request.form.get('deposit'))
        depo_pass = str(request.form.get('depopass'))
        amount = float(request.form.get('amount'))

        cursor.execute('SELECT * FROM data WHERE phonenumber = %s', (deposit_no,))
        deposit_details = cursor.fetchone()

        # Check if the deposit_details exist and password matches
        if deposit_details and deposit_details[4] == depo_pass:
            balan = deposit_details[3]
            new_bal = balan + amount

            # Update balance
            cursor.execute("UPDATE data SET balance = %s WHERE phonenumber = %s", (new_bal, deposit_no))

            current_date = datetime.now().date()
            current_time = datetime.now().time()

            # Insert transaction history
            insert_transaction_query = "INSERT INTO transcition_history (username, date_of_transcition, time_of_transcition, deposit) VALUES (%s, %s, %s, %s)"
            transaction_data_receiver = (deposit_no, current_date, current_time, amount)
            cursor.execute(insert_transaction_query, transaction_data_receiver)

            mycon.commit()
            flash('Transaction successful', 'success')
        else:
            flash('Invalid phone number or password', 'error')

    except mysql.connector.Error as err:
        mycon.rollback()
        flash(f"Error: {err}", 'error')

    finally:
        cursor.close()
        mycon.close()

    return render_template('deposit.html')


@app.route('/send-money', methods=['POST'])
def send_money():
    try:
        mycon = mysql.connector.connect(host="localhost", user="root", passwd="password", database="bank")
        cursor = mycon.cursor(buffered=True)

        sender_phone = str(request.form.get('sender'))
        receiver_phone = str(request.form.get('reciever'))
        amount = float(request.form.get('amount'))

        cursor.execute('SELECT * FROM data WHERE phonenumber = %s', (sender_phone,))
        sender_details = cursor.fetchone()

        # Check if receiver exists
        cursor.execute('SELECT * FROM data WHERE phonenumber = %s', (receiver_phone,))
        reciever_details = cursor.fetchone()

        if sender_details is None:
            flash('Sender not found', 'error')
        elif reciever_details is None:
            flash('Receiver not found', 'error')
        else:
            sender_balance = sender_details[3]
            receiver_balance = reciever_details[3]

            if sender_balance < amount:
                flash('Insufficient funds', 'error')
            else:
                sender_final_balance = sender_balance - amount
                receiver_final_balance = receiver_balance + amount

                update_sender_query = "UPDATE data SET balance = %s WHERE phonenumber = %s"
                cursor.execute(update_sender_query, (sender_final_balance, sender_phone))

                update_receiver_query = "UPDATE data SET balance = %s WHERE phonenumber = %s"
                cursor.execute(update_receiver_query, (receiver_final_balance, receiver_phone))

                current_date = datetime.now().date()
                current_time = datetime.now().time()

                insert_transaction_query = "INSERT INTO transcition_history (username, date_of_transcition, time_of_transcition, withdraw) VALUES (%s, %s, %s, %s)"
                transaction_data_sender = (sender_phone,current_date,current_time, amount)
                cursor.execute(insert_transaction_query, transaction_data_sender)

                insert_transaction_query = "INSERT INTO transcition_history (username, date_of_transcition, time_of_transcition, deposit) VALUES (%s, %s, %s, %s)"
                transaction_data_receiver = (receiver_phone, current_date,current_time, amount)
                cursor.execute(insert_transaction_query, transaction_data_receiver)

                mycon.commit()
                flash('Transaction successful', 'success')

    except mysql.connector.Error as err:
        mycon.rollback()
        flash(f"Error: {err}", 'error')

    finally:
        cursor.close()
        mycon.close()

    return render_template('send.html')
        
def balance():
    mycon=mysql.connector.connect(host="localhost",user="root",passwd="password",database="bank")
    cursor=mycon.cursor()
    cursor.execute('select * from data')
    details=cursor.fetchone()
    global user
    usernm=(input('Plz enter your username for confirmation:'))
    if user==usernm:
        while details:
            if details[0]==user:
                anm=amount(details[3])
                clrprint('Your balance fetched succuesfully\nyour balance is',"₹",anm,clr='green')
                free=int(input('press 1 to continue or 2 to exit'))
                if free==1:
                    main()
                else:
                    break
                
            details=cursor.fetchone()
    else:
        clrprint('Plz enter the valid username.',clr='red')
        fr=int(input('Enter 1 to retry:'))
        if fr==1:
               withdraw()
def depo_history(username):
    mycon = mysql.connector.connect(host="localhost", user="root", passwd="password", database="bank")
    cursor = mycon.cursor()

    cursor.execute('SELECT username, date_of_transcition, time_of_transcition, deposit FROM transcition_history WHERE username = %s AND deposit IS NOT NULL', (username,))
    hist = cursor.fetchall()

    data = []

    if hist:
        for i in hist:
            us = i[0]
            date = i[1]
            time = i[2]
            deposit_amount = i[3]
            data.append((us, date, time, deposit_amount))

    mycon.close()
    return data

@app.route('/deposit_history', methods=['GET', 'POST'])
def deposit_history():
    if request.method == 'POST':
        username = request.form.get('phoneno')  # Assuming you have a form field with the username
        dept_history_data = depo_history(username)
        return render_template('transcition.html', dept_history_data=dept_history_data)
    return render_template('transcition.html')

def with_history(username):
    data = []
    try:
        mycon = mysql.connector.connect(host="localhost", user="root", passwd="password", database="bank")
        with mycon.cursor() as cursor:
            cursor.execute('SELECT username, date_of_transcition, time_of_transcition, withdraw FROM transcition_history WHERE username = %s AND withdraw IS NOT NULL', (username,))
            hist = cursor.fetchall()

            if hist:
                for row in hist:
                    username = row[0]
                    date = row[1]
                    time = row[2]
                    withdraw_amount = row[3]
                    data.append((username, date, time, withdraw_amount))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if mycon:
            mycon.close()
    
    return data

@app.route('/withdraw_history', methods=['GET', 'POST'])
def withdraw_history():
    if request.method == 'POST':
        username = request.form.get('phonenos') # Debug print statement
        dept_history_data1 = with_history(username) # Debug print statement
        return render_template('transcition.html', dept_history_data1=dept_history_data1)
    return render_template('transcition.html')
                 
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with mysql.connector.connect(
                    host="localhost", user="root", passwd="password", database="bank"
            ) as mycon:
                with mycon.cursor() as cursor:
                    cursor.execute("SELECT phonenumber, password,name FROM data WHERE phonenumber = %s", (username,))
                    data = cursor.fetchone()

                    if data:
                        # Successful login
                        session['username'] = data[0]  # Store username in session
                        session['name'] = data[2]  # Store name in session
                        return redirect(url_for('firstpage'))
                    else:
                        message = "Incorrect username or password"

        except mysql.connector.Error as err:
            # Handle database errors
            print(f"Error: {err}")
            message = "An error occurred, please try again later."

    return render_template('login.html', message=message)


@app.route('/firstpage')
def firstpage():
    # Retrieve name from session
    name = session.get('name')
    if name:
        return render_template('firstpage.html', name=name)
    else:
        return redirect(url_for('login'))
 
@app.route('/signup', methods=['POST'])         
def signup():
    phone = request.form['phone']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    balance=1000
    mycon=mysql.connector.connect(host="localhost",user="root",passwd="password",database="bank")
    cursor=mycon.cursor(buffered=True)
    cursor.execute('select * from data')
    details=cursor.fetchall()
    cursor.execute('SELECT * FROM data WHERE phonenumber = %s', (phone,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        flash('Phone number already in use. Please try another phone number.', 'error')
        return redirect(url_for('login'))  # Redirect to login page on error

    try:
        # Insert new user into 'data' table
        insert_user_query = "INSERT INTO data (phonenumber, name, email_id,balance,password) VALUES (%s, %s, %s, %s,%s)"
        user_data = (phone, name, email,balance, password)
        cursor.execute(insert_user_query, user_data)
          
        insert_login_query = "INSERT INTO login_details (phonenumber, password) VALUES (%s, %s)"
        login_data = (phone, password)
        cursor.execute(insert_login_query, login_data)

        current_date = datetime.now().date()
        current_time = datetime.now().time()

        insert_transcition_query = "INSERT INTO transcition_history (username, date_of_transcition, time_of_transcition, deposit) VALUES (%s, %s, %s, 1000)"
        transcition_data = (phone, current_date, current_time)
        cursor.execute(insert_transcition_query, transcition_data)
        
        # Commit changes and close connection
        mycon.commit()
        cursor.close()
        mycon.close()

        flash('Signup is successful! You can now login.', 'success')
        return redirect(url_for('login'))  # Redirect to login page on successful signup
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True) 


    
    
       
    
