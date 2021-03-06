from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers.offer_request import OfferRequestSerializer
from .serializers.call_request import CallRequestSerializer
from .serializers.call_request import AcceptDeclineRequestSerializer
from .serializers.ice_request import IceRequestSerializer
from .models import Sdp, UserConnection, UserProfile
from django.conf import settings
import json
from django.core.exceptions import ObjectDoesNotExist
from .tasks import call_task, sender_offer_task, sender_answer_task, send_ice_task


def index(request):
    return render(request, 'sender.html', {"server_name": settings.DOMAIN_NAME, "socket_url": settings.SOCKET_URL})


def accept(request):
    return render(request, 'reciever.html', {"server_name": settings.DOMAIN_NAME, "socket_url": settings.SOCKET_URL})


@swagger_auto_schema(
    request_body=OfferRequestSerializer
)
class OfferView(APIView):
    """
       Get offer from abonent after click Show cam button.

    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=OfferRequestSerializer
    )
    def post(self, request, format=None):
        payload = request.data
        conn = UserConnection.objects.get(sid=payload['sid'])
        # найдем существующее Sdp или создадим новое
        if payload['type'] == 'sender':
            try:
                offer = Sdp.objects.get(from_user=conn.user)
            except ObjectDoesNotExist:
                offer = Sdp()
        else:
            # если запрашивает принимающий значит Offer уже должен быть 100%
            try:
                offer = Sdp.objects.get(to_user=conn.user)
            except ObjectDoesNotExist:
                Response({'status': 1, 'message': f'Sdp does not exist!'})

        # устанавливаем Offer для передающего и уведомляем принимающую сторону
        if payload['type'] == 'sender':
            
            # найдем принимающего по переданному логину
            try:
                reciever = UserProfile.objects.get(login=payload['reciever_login'])
            except ObjectDoesNotExist:
                Response({'status': 1, 'message': f'Reciever does not exist!'})

            offer.from_user = conn.user
            offer.from_user_sdp = payload['offer']
            offer.to_user = reciever
            # уведомляем принимающую сторону через задачу для celery
            sender_offer_task(conn.user.id, reciever.id, payload['offer'])
        # устанавливаем Offer для принимающего
        else:
            offer.to_user = conn.user
            offer.to_user_sdp = payload['answer']
            # уведомляем передающую сторону через задачу для celery
            sender_answer_task(offer.from_user.id, payload['answer'])
        offer.save()
        return Response({'offer': 'ok'})


class CallView(APIView):
    """
       Call request.

    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=CallRequestSerializer
    )
    def post(self, request, format=None):
        data = json.loads(request.body)
        try:
            callee = UserProfile.objects.get(login=data['login'])
        except ObjectDoesNotExist:
            return Response({'status': 1, 'message': 'User does not connected!'})

        try:
            conn = UserConnection.objects.get(sid=data['sid'])
            caller = conn.user
        except ObjectDoesNotExist:
            return Response({'status': 1, 'message': 'You are not connected!'})

        #call_task.delay(caller.id,callee.id)
        call_task(caller.id, callee.id)

        return Response({'call': 'ok'})



class AcceptView(APIView):
    """
       Accept a call.

    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=AcceptDeclineRequestSerializer
    )
    def post(self, request, format=None):
        data = json.loads(request.body)
        return Response({'call': 'ok'})



class DeclineView(APIView):
    """
       Decline a call.

    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=AcceptDeclineRequestSerializer
    )
    def post(self, request, format=None):
        data = json.loads(request.body)
        return Response({'call': 'ok'})


class IceView(APIView):
    """
       Get ice candidates.

    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=IceRequestSerializer
    )
    def post(self, request, format=None):
        payload = request.data
        # поищем соединение
        try:
            conn = UserConnection.objects.get(sid=payload['sid'])
        except ObjectDoesNotExist:
            return Response({'status': 1, 'message': 'Connection does not exist!'})

        # поищем SDP для передающей стороны
        try:
            sdp = Sdp.objects.get(from_user=conn.user)
            send_ice_task(sdp.to_user.id, payload['ice'])
        except ObjectDoesNotExist:
            print('Sdp for sender not found')

        # поищем SDP для принимающей стороны
        try:
            sdp = Sdp.objects.get(to_user=conn.user)
            send_ice_task(sdp.from_user.id, payload['ice'])
        except ObjectDoesNotExist:
            print('Sdp for reciever not found')

        return Response({'ice': payload})
