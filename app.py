import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form

        msg = EmailMessage()
        msg["Subject"] = "Nouvelle inscription - AREOPAGE CLUB"
        msg["From"] = os.environ.get("GMAIL_USER")
        msg["To"] = "areopageclub@gmail.com"

        msg.set_content(
            "\n".join(f"{key}: {value}" for key, value in data.items())
        )

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(
                    os.environ.get("GMAIL_USER"),
                    os.environ.get("GMAIL_APP_PASSWORD")
                )
                smtp.send_message(msg)
        except Exception as error:
            return f"Erreur d'envoi : {error}", 500

        return render_template("success.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
