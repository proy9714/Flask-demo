from flask import Response, request
import json
from bson.objectid import ObjectId
from app import app
from dbconnection import db

# CREATE
@app.route('/users', methods=['POST'])
def create():
    try:
        user = {
            "name": request.form["name"],
            "lastName": request.form["lastName"] 
        }

        dbResponse = db.users.insert_one(user)
        print(f"Inserted Id : {dbResponse.inserted_id}")
        
        # for attr in dir(dbResponse):
        #     print(attr)

        return Response(
            response = json.dumps({
                "message": "User created", 
                "id": f"{dbResponse.inserted_id}"
            }),
            status=200,
            mimetype="application/json"    
        )

    except Exception as e:
        print("**********")
        print(e)
        print("**********")

############################################################

# READ
@app.route('/users', methods=['GET'])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])

        return Response(
            response = json.dumps(data),
            status=200,
            mimetype="application/json"    
        )

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
@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name" : request.form["name"]}}
        )

        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")

        if dbResponse.modified_count == 1:
            return Response(
                response = json.dumps({"message": "User Updated"}),
                status=200,
                mimetype="application/json"    
            )
    
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
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})

        if dbResponse.deleted_count == 1:
            return Response(
                response = json.dumps({"message": "User deleted"}),
                status=200,
                mimetype="application/json"    
            )
    
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

