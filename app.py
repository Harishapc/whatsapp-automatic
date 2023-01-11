from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://harish:7892307634@cluster0.xpichhr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["bekary"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)
app = Flask(__name__.split('.')[0])

@app.route('/', methods=['GET', 'POST'])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    response = MessagingResponse()
    msg.media("https://images.unsplash.com/photo-1608365151231-7dbed3034787?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80","Welcom")
    user = users.find_one({"number": number})

    if bool(user) ==False :
        response.message(
            "Hi, thanks for contacting *The Red Velvet* \n You can choose from one of th options below: "
            "\n\n*Type*\n\n1️⃣ TO *Contact* us \n2️⃣ To *order* snacks \n3️⃣To know oue *working hours* \n4️⃣ To get "
            "our*Address*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)

        if option == 1:
            response.message("you can contact us through phone or email. \n\n *phone* 997892307634 \n *E-mail* : "
                             "rishandrishcompanies@gmail.com")
        elif option == 2:
            response.message("you have entered *ordering mode*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            response.message(
                "You can select one of the following cakes to order, \n\n *1️⃣Red Velvet*  \n2️⃣Dark Forest "
                "\n3️⃣Ice Cream Cake \n4️⃣Plum Cake \n5️⃣Sponge Cake \n6️⃣Genoise Cake \n7️⃣Carrot Cake "
                "\n8️⃣Butterscotch \n0️⃣Go Back* ")
        elif option == 3:
            response.message("We work on everyday *9 AM to 5 PM*")
        elif option == 4:
            response.message("We work many centres across the city our main centre at *Bangalore*")
        else:
            response.message("Please enter a valid response")
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            response.message(" You can choose from one of th options below: "
                             "\n\n*Type*\n\n1️⃣ TO *Contact* us \n2️⃣ To *order* snacks \n3️⃣To know oue *working hours* \n4️⃣ To get "
                             "our*Address*")
        elif 1 <= option <= 9:
            cakes = ["Red Velvet Cake", "Dark Forest Cake", "Ice Cream Cake", "Plum Cake", "Sponge Cake",
                     "Genoise Cake", "Carrot Cake", "Butterscotch"]
            selected = cakes[option - 1]
            users.update_one(
            {"number": number}, {"$set": {"status": "address"}})
            users.update_one(
            {"number": number}, {"$set": {"item": selected}})
            response.message("Excellent choice😉")
            response.message("Please Enter your address to confirm the order")
        else:
          response.message("Please enter a valid response")
    elif user["status"] == "address":
        selected = user["item"]
        response.message("Thanks for shopping with us")
        response.message(f" your order for {selected} has been received and will be delivered with in an hour")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
    elif user["status"] == "ordered":
        response.message(
            "Hi, thanks for contacting  again * The Red Velvet* \n You can choose from one of th options below: "
            "\n\n*Type*\n\n1️⃣ TO *Contact* us \n2️⃣ To *order* snacks \n3️⃣To know oue *working hours* \n4️⃣ To get "
            "our*Address*")
        users.update_one(
        {"number": number}, {"$set": {"status": "main"}})
        users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)


if __name__ == '__main__':
    app.run()
