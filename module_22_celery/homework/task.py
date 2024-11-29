"""
В этом файле будут Celery-задачи
"""
#Заменил название из за проблем импорта

from celery import Celery, chain
from .image import blur_image
from .mail import send_email
from celery.schedules import crontab
from .shared import subscribers



app = Celery("task",
             broker="redis://localhost:6379/0",
             backend="redis://localhost:6379/0")

@app.task
def image_processing(src_filename: str):
    try:
        print(f"Выполнение обработки изображения: {src_filename}...")
        output_image = blur_image(src_filename)  # Обработка изображения
        return output_image

    except OSError as e:
        print(f"Ошибка при обработке изображения: {e}")
        raise
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        raise

@app.task
def sending_email(output_image: str, receiver_email: str):
    print(f"Отправка результатов {output_image} на адрес: {receiver_email}...")
    sending = send_email(output_image, receiver_email)  # Отправка email
    return sending

@app.task
def process_image_and_send_email(src_filename: str, receiver_email: str):
    # Создаем цепочку задач
    task_chain = chain(image_processing.s(src_filename), sending_email.s(receiver_email))
    result = task_chain.delay()  # Выполняем цепочку задач
    return result

@app.task
def weekly_mailing(image_path: str):
    print("Отправка еженедельной рассылки...")

    output_image = image_processing(image_path)
    for email in subscribers.keys():
        sending_email.delay(output_image, email)  # Отправка письма с обработанным изображением
        print(f"Отправка письма на {email} - завершена.")

# Каждый понедельник в 9:00
app.conf.beat_schedule = {
    'send-weekly_mailing': {
        'task': 'weekly_mailing',
        'schedule': crontab(0, 9, '*', '*', '*'),
    },
}
