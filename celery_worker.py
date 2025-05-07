import os
from celery import Celery

# Створюємо екземпляр Celery
app = Celery('email_task', broker='redis://localhost:6379/0')

# Директория, куди будуть зберігатися листи
EMAIL_FOLDER = './emails/'

# Перевіряємо, чи існує папка для збереження email'ів
os.makedirs(EMAIL_FOLDER, exist_ok=True)

@app.task
def save_email_to_folder(subject: str, body: str, to_email: str):
    # Створюємо файл з іменем на основі email
    email_filename = os.path.join(EMAIL_FOLDER, f"{to_email}_email.txt")
    
    # Формуємо текст листа
    email_content = f"Subject: {subject}\nTo: {to_email}\n\n{body}"
    
    # Записуємо лист в файл
    with open(email_filename, 'w') as f:
        f.write(email_content)
    
    print(f"Email saved to {email_filename}")
