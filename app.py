from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import csv

app = Flask(__name__)
app.secret_key = 'my_secret_key_123'  # Needed for flashing messages

# ===mail configuaration ===

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'danmajor787@gmail.com'  # your Gmail
app.config['MAIL_PASSWORD'] = 'dkmfxalvhktzlwjw'     # App Password
app.config['MAIL_DEFAULT_SENDER'] = 'danmajor787@gmail.com'

mail = Mail(app)

# In-memory counters
slot_limits = {
    "internship": 0,
    "attachment": 0,
    "job": 0
}

MAX_SLOTS = 10

@app.route('/', methods=["GET", "POST"])
def index():
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email_address = request.form.get('email_address')
        subject = request.form.get('subject')
        message = request.form.get('message')
        msg = Message(subject=f"Contact Form:{subject}", sender=email_address,
                     recipients=["danmajor787@gmail.com"], body=f"From: {full_name}<{email_address}>\n\n{message}" )
        try:
            mail.send(msg)
            return render_template('message_info.html')
        except Exception as e:
            print(f"Email sending failed:", e)
            return render_template('invalid_email.html')    

        
        #return redirect(url_for('index'))
    return render_template("index.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/terms_of_service')
def terms_of_service():
    return render_template("terms_of_service.html")

@app.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html")

@app.route('/privacy_policy')
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route('/sitemap')
def sitemap():
    return render_template("sitemap.html")

@app.route('/invalid_email')
def invalid_email():
    return render_template("invalid_email.html")

@app.route('/careers')
def careers():
    return render_template("careers.html")
@app.route('/message_info')
def message_info():
    return render_template("message_info.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email_address = request.form.get('email_address')
        subject = request.form.get('subject')
        message = request.form.get('message')

        try:
            msg = Message(subject=f"Contact Form:{subject}", 
                          
                          sender=email_address,
                          recipients=["danmajor787@gmail.com"], 
                          body=f"From: {full_name}<{email_address}>\n\n{message}" )
           
            mail.send(msg)
            return render_template('message_info.html')
        except Exception as e:
            print(f"Email sending failed:", e)
            return ('not sent') #render_template('invalid_email.html')
        
        #return redirect(url_for('contact'))
    
    return render_template("contact.html")



@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/properties')
def properties():
    return render_template("properties.html")

@app.route('/thank_you')
def thank_you():
    return render_template("thank_you.html")


@app.route('/failed')
def failed():
    return render_template("failed.html")

@app.route('/apply', methods=["GET", "POST"])
def apply():
    app_type = request.args.get("type")
    if app_type not in slot_limits:
        return "Invalid application type.", 400

    if request.method == "POST":
        full_name = request.form["full_name"].strip().lower()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()

        # Ensure file exists before checking for duplicates
        if os.path.exists("applications.csv"):
            with open("applications.csv", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 4:
                        continue
                 
                    existing_name = row[0].strip().lower() 
                    existing_email = row[1].strip().lower() 
                    existing_phone = row[2].strip()
                    

                    if (full_name == existing_name and
                        email == existing_email and
                        phone == existing_phone):

                        #flash("❌ You have already applied using this information.")
                        return redirect(url_for("failed"))

        if slot_limits[app_type] >= MAX_SLOTS:
            return f"No more vacant slots for {app_type}", 403

        job_type = request.form.get("job_type", "")  # Only used for job

        # Save the new applicant
        with open("applications.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([full_name, email, phone, app_type, job_type])

        slot_limits[app_type] += 1
        #flash("✅ Thank you! Your application has been received.")
        return redirect(url_for('thank_you'))

    # GET request
    job_slots = slot_limits["job"]
    general_slots = max(slot_limits["internship"], slot_limits["attachment"])
    return render_template(
        "apply.html", 
        app_type=app_type,
        job_slots=job_slots,
        general_slots=general_slots
    )

if __name__ == "__main__":
    app.run(debug=True)
