from datetime import datetime
from sqlite3 import Timestamp
from flask import Flask, jsonify, redirect, request, session
import uuid
from passlib.hash import pbkdf2_sha256
from app import resource, users, transactions, projects

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):

        # User Object
        user = {
            "_id":  uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password":request.form.get('password'),
        }

        # Password encryption
        
        user["password"]=pbkdf2_sha256.encrypt(user['password'])

        # Database call to check existing user

        if users.find_one({ "email": user['email'] }):
            return jsonify({"error":"Account already exists, please Login!"}), 400

        # Database call to insert on success

        if users.insert_one(user):
           return self.start_session(user) 

        return jsonify({"error":"Signup Failed!"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def signin(self):
        user = users.find_one({ "email": request.form.get('email') })

        if user and pbkdf2_sha256.verify(request.form.get('password'),user['password']):
            return self.start_session(user)
        
        return jsonify({"error":"Invalid Credentials / User not Found"}), 401

class Hardware:

    def checkout(self):
        # User Object
        hardware = {
            "user_id": request.form.get('userId'),
            "project_id":"P0",
            "transaction_type":"checkout",
            "user_email": request.form.get('userEmail'),
            "hw_set": request.form.get('gridRadiosCheckOut'),
            "hw_units": request.form.get('checkoutQ'),
        }

        # Database call to check existing quantity

        # if users.find_one({ "email": user['email'] }):
        #     return jsonify({"error":"Account already exists!"}), 400

        if hardware['hw_set']=="HWSet A":
            avial = resource.find_one({"id":"1"})
            avail = int(avial['hwset1_availability'])
            ask = int(hardware['hw_units'])

            if  ask >= avail:
                diff = ask - avail
                resource.update_one({"id":"1"},{"$set":{"hwset1_availability":0}})
                return jsonify({"error":"Please Note, Could not check out "+str(diff)+" Orders!"}), 400

            else:
                diff = avail - ask
                resource.update_one({"id":"1"},{"$set":{"hwset1_availability":diff}})
                transactions.insert_one(hardware)
                return jsonify({"Success":"Order Processed!"}), 200
        
        elif hardware['hw_set']=="HWSet B":
            avial = resource.find_one({"id":"1"})
            avail = int(avial['hwset2_availability'])
            ask = int(hardware['hw_units'])

            if  ask >= avail:
                diff = ask - avail
                resource.update_one({"id":"1"},{"$set":{"hwset2_availability":0}})
                return jsonify({"error":"Please Note, Could not check out "+str(diff)+" Orders!"}), 400

            else:
                diff = avail - ask
                resource.update_one({"id":"1"},{"$set":{"hwset2_availability":diff}})
                transactions.insert_one(hardware)
                return jsonify({"Success":"Order Processed!"}), 200

        return jsonify(hardware), 400
    
    def checkin(self):
        # User Object
        hardware = {
            "user_id": request.form.get('userId'),
            "project_id":"P0",
            "transaction_type":"checkin",
            "user_email": request.form.get('userEmail'),
            "hw_set": request.form.get('gridRadiosCheckIn'),
            "hw_units": request.form.get('checkinQ'),
        }

        # Database call to check existing quantity

        if hardware['hw_set']=="HWSet A":
            avial = resource.find_one({"id":"1"})
            avail = int(avial['hwset1_availability'])
            cap = int(avial['hwset1_capacity'])
            ask = int(hardware['hw_units'])
            
            if  ask > cap or (ask + avail) > cap:
                return jsonify({"error":"Cannot Check in more than Capacity!"}), 400

            else:
                updated_cap = avail + ask
                resource.update_one({"id":"1"},{"$set":{"hwset1_availability":int(updated_cap)}})
                transactions.insert_one(hardware)
                return jsonify({"Success":"Order Processed!"}), 200

        if hardware['hw_set']=="HWSet B":
            avial = resource.find_one({"id":"1"})
            avail = int(avial['hwset2_availability'])
            cap = int(avial['hwset2_capacity'])
            ask = int(hardware['hw_units'])
            
            if  ask > cap or (ask + avail) > cap:
                return jsonify({"error":"Cannot Check in more than Capacity!"}), 400

            else:
                updated_cap = avail + ask
                resource.update_one({"id":"1"},{"$set":{"hwset2_availability":int(updated_cap)}})
                transactions.insert_one(hardware)
                return jsonify({"Success":"Order Processed!"}), 200
    
        return jsonify(hardware), 400
    

class Project:

    def start_session(self, project):
        session['logged_in'] = True
        session['project'] = project
        return jsonify(project), 200

    def create(self):
        project = {
            "_id":  uuid.uuid4().hex,
            "project_name": request.form.get('project_name'),
            "project_description": request.form.get('project_description'),
            "project_id":request.form.get('project_id'),
        }

        if users.find_one({ "projects_id": project['project_id'] }):
            return jsonify({"error":"Project already exists!"}), 200

        # Database call to insert on success

        if projects.insert_one(project):
           return self.start_session(project) 

        return jsonify({"error":"Project Creation Failed!"}), 200

    def retrieve(self):
        project = projects["project_id"]

        if request.form.get('project_id') in project:
            return self.start_session(project)
        
        return jsonify({"error":"Invalid Details / Project not Found"}), 200
