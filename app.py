# TO RUN FLASK USE THE FOLLOWING COMMAND:
# pip install flask
#  --> if that doesn't work, use: pip3 install flask

# Then, to launch the server execute: flask run

# It will output the url in the terminal

# I'd recommend running from your native computer rn, haven't tried on the student
# machines or collabs yet

from flask import Flask, render_template, request, redirect, url_for, session

from collections import defaultdict

from cryptography import cryptography

users = defaultdict()

app = Flask(__name__)

app.secret_key = 'random_string'

crypto_manager = cryptography()


@app.route("/")
def login():
    return render_template('intro.html')

@app.route("/validate_user", methods=["POST"])
def validate_user():
    # encrypt the password before storage
    input_password = request.form.get("password")
    
    encrypted_password  = encrypt_first_time(input_password)

    # call function to validation username and password
    valid = validate_user_func(request.form.get("email"), encrypted_password)

    # determine outcome based on success of login
    if (valid):
        session['username'] = request.form.get("email")
        return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

    
@app.route("/new_user", methods=["POST"])
def new_user():
    # encrypt the password before storage
    input_password = request.form.get("password")

    encrypted_password  = encrypt_first_time(input_password)

    # call function to validation username and password
    valid = register_user_func(request.form.get("email"), encrypted_password)

    # determine outcome based on success of login
    if (valid):
        session['username'] = request.form.get("email")
        return redirect(url_for('user'))
    else:
        return redirect(url_for('register'))


@app.route("/register")
def register():
    return render_template('create_new.html')

@app.route("/user")
def user():
    return render_template('user_access.html')

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username')
    session.pop('key')
    return redirect(url_for('login'))

@app.route("/store_new", methods=["POST"])
def store_new():
    website = request.form.get("website")
    password = request.form.get("password")

    encrypted_password = encrypt_with_key(password)

    store_new_password(session['username'], website, encrypted_password)

    return redirect(url_for('user'))


@app.route("/retrieve", methods=["POST"])
def retrieve():
    # get the website the user input
    website = request.form.get("website_retreive")
    
    # get the encrypted password from the database
    password = get_password(session['username'], website)

    # check to make sure there was a valid entry there
    if password is None:
        html_text = "<p>*** No entry for " + website + " ***</p>"
    else:
        html_text = "<p>" + website + ": " + decrypt_with_key(password)  + "</p>"

    # include a back button
    html_text += "<button onclick=\"location.href='/user'\">Return</button>"

    return html_text

@app.route("/change", methods=["POST"])
def change():
    website = request.form.get("website_change")
    password = request.form.get("password_change")

    encrypted_password = encrypt_with_key(password)

    change_password(session['username'], website, encrypted_password)

    return redirect(url_for('user'))

@app.route("/view", methods=["POST"])
def view():
    websites_and_passwords = view_all_passwords(session['username'])

    html_text = ""

    for site_and_pass in websites_and_passwords:
        html_text += "<p>" + site_and_pass[0] + ": " + str(decrypt_with_key(site_and_pass[1])) + "</p>"

    html_text += "<button onclick=\"location.href='/user'\">Return</button>"

    print(html_text)

    return html_text

def encrypt_first_time(plain_text):
    fileName = "passwords.txt"

    keyArray = crypto_manager.genKey(len(plain_text), fileName, plain_text)
    keyStream = crypto_manager.keyStream_gen(len(plain_text), keyArray)

    session['key'] = keyStream

    encrypted_password = crypto_manager.rc4_encryption(keyStream, plain_text)

    return encrypted_password

def encrypt_with_key(plain_text):
    fileName = "passwords.txt"

    encrypted_password = crypto_manager.rc4_encryption(session['key'], plain_text)

    return encrypted_password

def decrypt_with_key(encrypted_password):
    fileName = "passwords.txt"

    decryption_output = crypto_manager.rc4_decryption(encrypted_password, session['key'])
    print(decryption_output)

    plain_text = ""

    for letter in decryption_output:
        plain_text += letter

    return plain_text


def validate_user_func(username, encrypted_password):
    # check to see if the user exists
    if not username in users.keys():
        return False
    
    # if the password is wrong, return false
    if not users[username]["master"] == encrypted_password:
        return False

    # else, return true
    return True


def register_user_func(username, encrypted_password):
    # check to see if the user already exists
    if username in users.keys():
        return False
    
    # create the sub hash table for the user
    users[username] = defaultdict()

    # set their password to the encrypted password
    users[username]["master"] = encrypted_password

    return True


def store_new_password(username, new_site, new_password):
    # check to see if a set password already exists
    if new_site in users[username].keys():
        return False
    
    # add the new entry
    users[username][new_site] = new_password

    return True

def get_password(username, site):
    # check to make sure it is a valid site
    if not site in users[username].keys():
        return None
    
    # return the password
    return users[username][site]

def change_password(username, site, new_password):
    # check to make sure it is a valid site
    if not site in users[username].keys():
        return False

    # change the password
    users[username][site] = new_password

    return True

def view_all_passwords(username):
    # return the site names with corresponding passwords
    return users[username].items()

