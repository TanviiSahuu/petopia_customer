from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)  

    def save(self, *args, **kwargs):
        """Hash password before saving to DB."""
        if not self.pk or 'password' in kwargs:
            self.password = make_password(self.password)
        super(Customer, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    house_colony = models.CharField(max_length=255, null=False, blank=False)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    pincode = models.CharField(max_length=10, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False, default="India")

    def __str__(self):
        return f"{self.house_colony}, {self.city}, {self.state} - {self.pincode}"
