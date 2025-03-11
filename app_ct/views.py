from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Customer, Address
from .serializer import CustomerSerializer, AddressSerializer, CustomerCreateSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    def get_permissions(self):
        # Allow any user to view or create, but restrict update and delete actions to authenticated users only.
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        return CustomerSerializer

    def create(self, request, *args, **kwargs):
        """Register a new customer (Signup)"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login API for customers"""
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                return Response({"message": "Login successful", "customer_id": str(customer.customer_id)}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found, please register first"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        """Retrieve all customers"""
        customers = self.get_queryset()
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrieve a customer by ID"""
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = self.get_serializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Update a customer by ID (authenticated users only)"""
        try:
            customer = Customer.objects.get(pk=pk)
            # Ensure the authenticated user is updating their own account.
            if str(customer.customer_id) != str(request.user.customer_id):
                return Response({"error": "You can only update your own account"}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Delete a customer by ID (authenticated users only)"""
        try:
            customer = Customer.objects.get(pk=pk)
            if str(customer.customer_id) != str(request.user.customer_id):
                return Response({"error": "You can only delete your own account"}, status=status.HTTP_403_FORBIDDEN)
            customer.delete()
            return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """Retrieve all addresses"""
        addresses = self.get_queryset()
        serializer = self.get_serializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrieve an address by ID"""
        try:
            address = Address.objects.get(pk=pk)
            serializer = self.get_serializer(address)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Update an address by ID (only by the owner)"""
        try:
            address = Address.objects.get(pk=pk)
            if str(address.customer.customer_id) != str(request.user.customer_id):
                return Response({"error": "You can only update your own address"}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Delete an address by ID (only by the owner)"""
        try:
            address = Address.objects.get(pk=pk)
            if str(address.customer.customer_id) != str(request.user.customer_id):
                return Response({"error": "You can only delete your own address"}, status=status.HTTP_403_FORBIDDEN)
            address.delete()
            return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
