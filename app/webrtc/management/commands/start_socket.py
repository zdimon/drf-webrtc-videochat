from django.core.management.base import BaseCommand
import socketio
import eventlet
import threading
from webrtc.models import UserProfile, UserConnection
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

mgr = socketio.RedisManager(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')

eventlet.monkey_patch()
sio = socketio.Server(cors_allowed_origins='*',
                      async_mode='eventlet',
                      client_manager=mgr)
app = socketio.WSGIApp(sio)


def add_connection_task(sid, data):
    try:
        user = UserProfile.objects.get(login=data['login'])
    except ObjectDoesNotExist:
        print('No user')
        user = UserProfile()
        user.login = data['login']
        user.save()
    con = UserConnection()
    con.user = user
    con.sid = sid
    con.save()


def remove_connection_task(sid):
    try:
        con = UserConnection.objects.get(sid=sid)
        user = con.user
        con.delete()
    except ObjectDoesNotExist:
        pass

    if UserConnection.objects.filter(user=user).count() == 0:
        user.delete()


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    #sio.emit('my event', {'data': 'foobar'})


@sio.event
def login(sid, data):
    thread = threading.Thread(target=add_connection_task, args=(sid, data))
    thread.start()


@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    thread = threading.Thread(target=remove_connection_task, args=(sid,))
    thread.start()


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Statrting socket server')
        eventlet.wsgi.server(eventlet.listen(('', int(settings.SOCKET_PORT))), app)
