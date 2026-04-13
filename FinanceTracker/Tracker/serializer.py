from rest_framework import serializers
from .models import Finance

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = ['id', 'amount', 'type', 'date', 'created_by'] 
        read_only_fields = ['created_by', 'id']  # id bhi read only hona chahiye
