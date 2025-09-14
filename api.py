from flask import Flask, request, jsonify
from controller import Controller
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    controller=Controller()
    data=request.json
    username=data['username']
    password=data['password']
    token=controller.loginQuery(username, password)
    if(token):
        data={
            'success':True,
            'token':token
        }
        return jsonify(data)
    else:
        data={
            'success':False
        }
        return jsonify(data)

@app.route("/tokenLogin")
@cross_origin()    
def tokenLogin():
    controller=Controller()
    auth=request.headers.get('Authorization')
    arr=auth.split(' ')
    token=arr[1]
    val=controller.tokenLogin(token)
    data={
        'success':val
    }
    return jsonify(data)

@app.route("/data", methods=["GET"])
@cross_origin()
def getData():
    controller=Controller()
    data=controller.getData()
    return jsonify(data)
    

@app.route("/deleteData", methods=["POST"])
@cross_origin()
def deleteData():
    controller=Controller()
    data=request.json
    val=controller.deleteData(data['id'])
    returnData={
        'success':val
    }
    return jsonify(returnData)

@app.route("/saveData", methods=["POST"])
@cross_origin()
def saveData():
    controller=Controller()
    data=request.json
    val=controller.insertData(data['username'], data['password'], data['isAdmin'])
    returnData={
        'success':val
    }
    return jsonify(returnData)

@app.route("/update", methods=["POST"])
@cross_origin()
def updateData():
    controller=Controller()
    data=request.json
    val=controller.updateData(data['key'], data['value'], data['id'])
    returnData={
        'success':val
    }
    return jsonify(returnData)


