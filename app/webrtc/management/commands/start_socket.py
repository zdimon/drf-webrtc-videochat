from django.core.management.base import BaseCommand
import socketio
import eventlet
import threading
from webrtc.models import UserProfile, UserConnection

eventlet.monkey_patch()
mgr = socketio.RedisManager('redis://localhost:6379/0')
sio = socketio.Server(cors_allowed_origins='*',async_mode='eventlet',client_manager=mgr)
app = socketio.WSGIApp(sio)

def add_user_task(sid,data):
    print('Adding user connection')
    # user = Gameuser.objects.get(login=data['login'])
    # user.add_sid(sid)


@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def login(sid, data):
    thread = threading.Thread(target=add_user_task, args=(sid,data))
    thread.start()

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Statrting socket server')
        eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
