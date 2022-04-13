from flask import Response, render_template, request, redirect, url_for
import json
from bson.objectid import ObjectId
from app import app
from dbconnection import db

# CREATE
@app.route('/create', methods=['POST'])
def create():
    try:
        user = {
            "name": request.form.get("first_name"),
            "lastName": request.form.get("last_name") 
        }

        dbResponse = db.users.insert_one(user)
        print(f"Inserted Id : {dbResponse.inserted_id}")
        
        # for attr in dir(dbResponse):
        #     print(attr)

        # return Response(
        #     response = json.dumps({
        #         "message": "User created", 
        #         "id": f"{dbResponse.inserted_id}"
        #     }),
        #     status=200,
        #     mimetype="application/json"    
        # )

        return redirect(url_for('get_users'))

    except Exception as e:
        print("**********")
        print(e)
        print("**********")

############################################################

# READ
@app.route('/', methods=['GET'])
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])

        return render_template("index.html", data = data)

        # return Response(
        #     response = json.dumps(data),
        #     status=200,
        #     mimetype="application/json"    
        # )

    except Exception as e:
        
        print("**********")
        print(e)
        print("**********")

        return Response(
            response = json.dumps({"message": "Cannot read users"}),
            status=500,
            mimetype="application/json"    
        )

############################################################

# UPDATE
@app.route('/update_user/<id>', methods=['GET' , 'POST'])
def update_user(id):
    try:
        objInstance = ObjectId(id)
        data = list(db.users.find({"_id": objInstance}))
        return render_template("update_user.html", data = data)

    except Exception as e:
        print("**********")
        print(e)
        print("**********")

        return Response(
            response = json.dumps({"message": "Sorry cannot update"}),
            status=500,
            mimetype="application/json"    
        )

@app.route('/update/<id>', methods=['GET' ,'POST' , 'PATCH'])
def update(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name" : request.form.get("first_name"), "lastName" : request.form.get("last_name")}}
        )

        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")

        if dbResponse.modified_count >= 1:
            # return Response(
            #     response = json.dumps({"message": "User Updated"}),
            #     status=200,
            #     mimetype="application/json"    
            # )

            return redirect(url_for('get_users'))
    
        return Response(
            response = json.dumps({"message": "Nothing to update"}),
            status=200,
            mimetype="application/json"    
        )

    except Exception as e:
        print("**********")
        print(e)
        print("**********")

        return Response(
            response = json.dumps({"message": "Sorry cannot update"}),
            status=500,
            mimetype="application/json"    
        )

############################################################

# DELETE
@app.route('/delete/<id>', methods=['GET' , 'POST' , 'DELETE'])
def delete_user(id):
    try:
        print(id)
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})

        if dbResponse.deleted_count == 1:
            # return Response(
            #     response = json.dumps({"message": "User deleted"}),
            #     status=200,
            #     mimetype="application/json"    
            # )

            return redirect(url_for('get_users'))
    
        return Response(
            response = json.dumps({"message": "Nothing to delete"}),
            status=200,
            mimetype="application/json"    
        )

    except Exception as e:
        print("**********")
        print(e)
        print("**********")

        return Response(
            response = json.dumps({"message": "Sorry cannot delete"}),
            status=500,
            mimetype="application/json"    
        )

