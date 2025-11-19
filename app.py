from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os, smtplib, csv
from datetime import datetime
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-this-secret")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.join(BASE_DIR, "static", "files")
CONTACT_STORE = os.path.join(BASE_DIR, "contacts.csv")
VISITOR_STORE = os.path.join(BASE_DIR, "visitors.csv")

os.makedirs(FILES_DIR, exist_ok=True)

# Email config (Gmail)
# Email config (Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ❗ DIRECT HARD-CODING (Your request)
MAIL_USERNAME = "udaybheema178@gmail.com"
MAIL_PASSWORD = "wggyoyzbfprxurhc"  # Replace with real Gmail App Password


def send_email(subject, body):
    """Send email to MAIL_USERNAME. Returns (success, info)."""
    if not MAIL_PASSWORD:
        app.logger.warning("MAIL_PASSWORD not set; email skipped.")
        return False, "MAIL_PASSWORD not set"
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = MAIL_USERNAME
        msg["To"] = MAIL_USERNAME
        msg.set_content(body)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
            smtp.send_message(msg)
        return True, "sent"
    except Exception as e:
        app.logger.exception("Failed to send email")
        return False, str(e)

@app.context_processor
def inject_current_year():
    return {"current_year": datetime.now().year}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please provide name, email, and message.", "error")
        return redirect(url_for("home") + "#contact")

    # Save to CSV
    header_needed = not os.path.exists(CONTACT_STORE)
    with open(CONTACT_STORE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["timestamp", "name", "email", "phone", "message"])
        writer.writerow([datetime.utcnow().isoformat(), name, email, phone, message])

    # Send Email ONLY HERE
    subject = f"New Portfolio Contact from {name}"
    body = (
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Message:\n{message}\n"
    )

    success, info = send_email(subject, body)

    if success:
        flash("Thanks — your message was sent!", "success")
    else:
        flash("Saved, but email failed: " + info, "warning")

    return redirect(url_for("home") + "#contact")

@app.route("/resume")
def resume():
    filename = "uday_bheema_resume.pdf"
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        # placeholder file so route doesn't 404; replace file locally with real PDF
        with open(path, "wb") as f:
            f.write(b"Replace this file with your real resume PDF.")
    # log download
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    with open(VISITOR_STORE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), ip, ua, "download_resume", "", ""])
    send_email(f"Resume downloaded — {ip}", f"Resume download by {ip}\nUA: {ua}")
    return send_from_directory(FILES_DIR, filename, as_attachment=True)

@app.route("/resume-view")
def resume_view():
    filename = "uday_bheema_resume.pdf"
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(b"Replace this file with your real resume PDF.")
    # track view
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    with open(VISITOR_STORE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), ip, ua, "view_resume", "", ""])
    send_email(f"Resume viewed — {ip}", f"Resume viewed by {ip}\nUA: {ua}")
    return render_template("resume_view.html", file=filename)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = (data.get("message") or "").strip().lower()
    if not msg:
        reply = "Hi — tell me what you'd like to know (resume, projects, skills)."
    elif any(w in msg for w in ["hi","hello","hey"]):
        reply = "Hello! I'm Uday's portfolio assistant. Ask about projects, skills, or the resume."
    elif "resume" in msg:
        reply = "You can view the resume via the 'View Resume' link, or download it."
    elif "projects" in msg:
        reply = "Featured projects: Multilingual OCR, Encrypted Chat, Portfolio Generator. Want details on one?"
    elif "skills" in msg:
        reply = "Main skills: Python, Machine Learning, Flask, Computer Vision, JavaScript."
    else:
        reply = "Nice question — I'm a simple assistant. Please contact via the form for detailed responses."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
