from rest_framework_json_api import serializers
from vendor_data.models import Customer, Subscription, Gifts

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'postal_code')

class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'plan_name', 'price')

class GiftsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gifts
        fields = ('id', 'plan_name', 'price', 'recipient_email')