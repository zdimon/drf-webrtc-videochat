from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers.offer_request import OfferRequestSerializer
from .models import Sdp, UserConnection

def index(request):
    return render(request, 'index.html')


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
        print(request.data)
        conn = UserConnection.objects.get(sid=request.data['sid'])
        offer = Sdp()
        offer.sdp = request.data['offer']
        offer.conn = conn
        offer.save()
        return Response({'offer': 'ok'})