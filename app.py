from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv

app = Flask(__name__)
app.secret_key = 'my_secret_key_123'  # Needed for flashing messages

# In-memory counters
slot_limits = {
    "internship": 0,
    "attachment": 0,
    "job": 0
}

MAX_SLOTS = 10

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/careers')
def careers():
    return render_template("careers.html")

@app.route('/contact')
def contact():
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
