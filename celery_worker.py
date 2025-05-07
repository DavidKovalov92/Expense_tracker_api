import os
from celery import Celery

app = Celery("email_task", broker="redis://localhost:6379/0")


EMAIL_FOLDER = "./emails/"

os.makedirs(EMAIL_FOLDER, exist_ok=True)


@app.task
def save_email_to_folder(subject: str, body: str, to_email: str):
    email_filename = os.path.join(EMAIL_FOLDER, f"{to_email}_email.txt")
    email_content = f"Subject: {subject}\nTo: {to_email}\n\n{body}"

    with open(email_filename, "w") as f:
        f.write(email_content)

    print(f"Email saved to {email_filename}")
