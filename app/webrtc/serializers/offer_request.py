from rest_framework import serializers


class OfferRequestSerializer(serializers.Serializer):
    sid = serializers.CharField()
    offer = serializers.CharField()