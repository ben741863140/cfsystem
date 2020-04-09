from logsystem.celery import app
from celery import shared_task
from board.auto_update import AutoUpdate


@shared_task
def auto_update():
    AutoUpdate.update()


@app.tasks
def update_alone(only_board):
    AutoUpdate.update(only_board)
    return
