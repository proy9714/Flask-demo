import pymongo

# CONNECTING TO DB
try:
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )

    db = mongo.test

    # Trigger exception if cannot connect to db
    mongo.server_info() 

except:
    print("**********")
    print("Cannot connect to DB")
    print("**********")
