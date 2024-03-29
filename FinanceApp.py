import datetime
import pytz
# Basic Flask imports
from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import from your custom module
from FinanceDB.SetupDB import Finance

# Connect to the database
engine = create_engine("sqlite:///FinanceDB//finance_database.db")

# Initialize Flask
app = Flask(__name__)


@app.route("/")
def on_start():
    return redirect(url_for("read_transactions"))



@app.route("/create_transaction", methods=["POST", "GET"])
def createTransaction():

    if request.method == "POST":
        # Get the data from the form and placed into a variable.
        input_data = request.form

        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()

        # create a new transaction and enter it into the database
        new_transaction = Finance(
            transaction_date_time=datetime.datetime.strptime(
                input_data["transaction_date_time"], "%Y-%m-%dT%H:%M"
            )
            if input_data["transaction_date_time"]
            else pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()),
            transaction_name=input_data["transaction_name"],
            product_details=input_data["product_details"],
            product_seller=input_data["product_seller"],
            expenditure_category=input_data["expenditure_category"],
            expenditure_sub_category=input_data["expenditure_sub_category"],
            amount_spent=input_data["amount_spent"],
        )

        session.add(new_transaction)
        session.commit()
        session.close()
        return redirect(url_for("read_transactions"))

    else:
        return render_template("create_transaction.html")


# Routing for simply reading the database (the 'R' in CRUD)
@app.route("/read_transactions", methods=["POST", "GET"])
def read_transactions():
    
    # Start this page's session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Query all results from the database
    query = session.query(Finance).all()
    
    # render the template and pass the query into the html
    return render_template("read_transactions.html", query = query)


# Routing for editing a transaction, including deletion (the 'U' and 'D' in CRUD)
@app.route("/transaction/<transaction_id>")
def edit(transaction_id):
    
    # Start this page's session
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    # Query the transaction based on the id
    query = session.query(Finance).filter(Finance.transaction_id == transaction_id).one()    
    
    session.close()
    
    # Render the html with the query passed through it
    return render_template("edit_transaction.html", query = query)


# Routing to actually update the transaction
@app.route("/edit_transaction/<transaction_id>", methods = ["POST", "GET"])
def edit_transaction(transaction_id):
    
    if request.method == "POST":
        # Get the data from the form and placed into a variable. 
        input_data = request.form
        
        # A new session will have to be created in every function
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        # Search for the transaction to change based on the transaction id
        query = session.query(Finance).filter(Finance.transaction_id == transaction_id).one()  
        
        # Write the changes to the database
        query.transaction_date_time = datetime.datetime.strptime(input_data["transaction_date_time"], "%Y-%m-%dT%H:%M")  if input_data["transaction_date_time"] else query.transaction_date_time
        query.transaction_name = input_data["transaction_name"]
        query.product_details = input_data["product_details"]
        query.product_seller = input_data["product_seller"]
        query.expenditure_category = input_data["expenditure_category"]
        query.expenditure_sub_category = input_data["expenditure_sub_category"]
        query.amount_spent = input_data["amount_spent"]
        session.commit()
        session.close()
        return redirect(url_for("read_transactions"))
    
    else:
        return redirect(url_for("read_transactions"))


# Routing for deleting a transaction
@app.route("/delete_transaction/<transaction_id>", methods = ["POST", "GET"])
def delete_transaction(transaction_id):
    if request.method == "POST":
        
        # A new session will have to be created in every function
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        # Search for the transaction to change based on the transaction id
        query = session.query(Finance).filter(Finance.transaction_id == transaction_id).one()
        
        # Delete the row
        session.delete(query)
        session.commit()
        session.close()
        
        return redirect(url_for("read_transactions"))
        
    else:
        return redirect(url_for("read_transactions"))


# Routing for simply reading the database (the 'R' in CRUD)
@app.route("/read_transactions")
def read_transactions():
    
    # Start this page's session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Query all results from the database
    query = session.query(Finance).all()
    
    # render the template and pass the query into the html
    return render_template("read_transactions.html", query = query)
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
