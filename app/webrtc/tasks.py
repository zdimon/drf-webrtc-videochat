from celery.decorators import task
import socketio   
from django.conf import settings
from .models import UserConnection, UserProfile
mgr = socketio.RedisManager(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')

@task()
def call_task(caller_id, callee_id):
    caller = UserProfile.objects.get(pk=caller_id)
    callee = UserProfile.objects.get(pk=callee_id)
    for con in UserConnection.objects.filter(user=callee):
        payload = {"login": caller.login}
        mgr.emit('calling', data=payload, room=con.sid)

@task()
def sender_offer_task(sender_id, reciever_id, sender_offer):
    reciever = UserProfile.objects.get(pk=reciever_id)
    sender = UserProfile.objects.get(pk=sender_id)
    # Находим все соединения по принимающей стороне
    for conn in UserConnection.objects.filter(user=reciever):
        # отсылаем сообщения на сокет
        payload = {"sender_login": sender.login,
                   "sender_offer": sender_offer}
        mgr.emit('sender_offer', data=payload, room=conn.sid)
