from flask import Flask, request, render_template, redirect, session, Response
from pymongo import MongoClient
import os
import cv2

# setting up database
client = MongoClient(
    "mongodb+srv://lakshu1000:lakshay1920@mlprojects.n13dkun.mongodb.net/&ssl=true&ssl_cert_reqs=CERT_NONE"
)
db = client["XPark"]
users = db["users"]
cameras = db["cameras"]
customers = db["customers"]
parkings = db["parkings"]
settings = db["settings"]

# setting up webcam
def generate_frames(url):
    camera = cv2.VideoCapture(url)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    camera.release()


# setting up app
app = Flask(__name__)
app.secret_key = os.urandom(24)


# admin routes
admin_id = "lakshu1000@gmail.com"

@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email == admin_id and password == "lakshay1920":
        session['user_id'] = email
        return redirect('/admin')
    else:
        return redirect('/login')

@app.route('/admin')
def admin():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            page = request.args.get('page')
            if page == "cameras":
                return render_template('admin.html', page = page, cameras = cameras.find())
            elif page == "parkings":
                return render_template('admin.html', page = page, parkings = parkings.find())
            elif page == "customers":
                return render_template('admin.html', page = page, customers = customers.find())
            elif page == "settings":
                return render_template('admin.html', page = page, settings = settings.find())
            else:
                return render_template('admin.html', page = page)
    else:
        return redirect('/')

@app.route('/add_camera', methods=['POST'])
def add_camera():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            id = request.form.get('camera_id')
            name = request.form.get('camera_name')
            url = request.form.get('camera_url')
            cameras.insert_one({"_id":id, "name":name, "url":url})
            return redirect('/admin?page=cameras')
    else:
        return redirect('/')
        
@app.route('/video_feed', methods=['GET'])
def video_feed():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            camera_id = request.args.get('camera_id')
            camera = cameras.find_one({"_id":camera_id})
            url = camera["url"]
            if len(url) < 3:
                url = eval(url)
            return Response(generate_frames(url), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect('/')

@app.route('/delete_camera', methods=['POST'])
def delete_camera():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            camera_id = request.form.get('camera_id')
            cameras.delete_one({"_id":camera_id})
            return redirect('/admin?page=cameras')
    else:
        return redirect('/')

@app.route('/add_parking', methods=['POST'])
def add_parking():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            id = request.form.get('parking_id')
            name = request.form.get('parking_name')
            location = request.form.get('parking_location')
            parkings.insert_one({"_id":id, "name":name, "location":location})
            return redirect('/admin?page=parkings')
    else:
        return redirect('/')

@app.route('/delete_parking', methods=['POST'])
def delete_parking():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            parking_id = request.form.get('parking_id')
            parkings.delete_one({"_id":parking_id})
            return redirect('/admin?page=parkings')
    else:
        return redirect('/')

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            id = request.form.get('customer_id')
            name = request.form.get('customer_name')
            email = request.form.get('customer_email')
            phone = request.form.get('customer_phone')
            plate = request.form.get('customer_plate')
            parking = request.form.get('customer_parking')
            customers.insert_one({"_id":id, "name":name, "email":email, "phone":phone, "plate":plate, "parkings":parking})
            return redirect('/admin?page=customers')
    else:
        return redirect('/')

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            customer_id = request.form.get('customer_id')
            customers.delete_one({"_id":customer_id})
            return redirect('/admin?page=customers')
    else:
        return redirect('/')

@app.route('/add_setting', methods=['POST'])
def add_setting():
    if 'user_id' in session:
        if session['user_id'] == admin_id:
            id = request.form.get('setting_id')
            name = request.form.get('setting_name')
            value = request.form.get('setting_value')
            settings.insert_one({"_id":id, "name":name, "value":value})
            return redirect('/admin?page=settings')
    else:
        return redirect('/')

@app.route('/admin_logout')
def admin_logout():
    session.pop("user_id")
    return redirect("/")


# user routes
@app.route('/')
def start():
    if 'user_id' in session:
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('home.html')
                               
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/home')
    if 'user_id' in session:
        return redirect('/admin')
    return render_template('login.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('register.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    details = users.find_one({"email" : email, "password":password})
    if details == None:
        return redirect('/register')
    else:
        session['user_id'] = details["email"]
        session['user_name'] = details["name"]
        return redirect('/home')

@app.route('/registration', methods=['POST'])
def registration():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    details = users.find_one({"email":email})
    if details == None:
        users.insert_one({"name":name, "email":email, "password":password})
        return redirect('/login')
    else:
        return redirect('/register')

@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect("/")

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('prof.html', email = session['user_id'], name = session['user_name'])


# running app
if __name__ == '__main__':
    app.run(debug=True)