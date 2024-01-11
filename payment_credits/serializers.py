from rest_framework import serializers
from .models import *

class PaymentsSerializer(serializers.ModelSerializer):
    method = serializers.CharField(max_length=10)

    class Meta:
        model = PaymentMethod
        fields = ('method',)

    def validate_method(self, value):
        method_choices = ["balance", "points"]
        if value not in method_choices:
            raise serializers.ValidationError("There is no such method.")
        return value