from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Customer, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'  
        read_only_fields = ['customer'] 

class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'addresses']

    def update(self, instance, validated_data):
        """Handles updating Customer along with nested addresses."""
        addresses_data = validated_data.pop('addresses', None)

        # Update customer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If addresses are provided, update them
        if addresses_data is not None:
            instance.addresses.all().delete()
            for address_data in addresses_data:
                Address.objects.create(customer=instance, **address_data)

        return instance

class CustomerCreateSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)
    password = serializers.CharField(write_only=True, required=True)  # Ensure password is required and write-only

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'addresses']

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        password = validated_data.pop('password')

        # Hash the password before saving
        validated_data['password'] = make_password(password)

        customer = Customer.objects.create(**validated_data)
        for address_data in addresses_data:
            Address.objects.create(customer=customer, **address_data)

        return customer
