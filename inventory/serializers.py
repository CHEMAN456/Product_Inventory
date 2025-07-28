from rest_framework import serializers
from .models import ProdMast, StckMain, StckDetail

class Prod_serializer(serializers.ModelSerializer):
    class Meta:
        model = ProdMast
        fields = '__all__'

class StckDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StckDetail
        fields = '__all__'      

class StckMainSerializer(serializers.ModelSerializer):
    details = StckDetailSerializer(many=True, read_only=True, source='stckdetail_set')

    class Meta:
        model = StckMain
        fields = ['id', 'transaction_type', 'timestamp', 'reference_number', 'notes', 'created_by', 'details']        