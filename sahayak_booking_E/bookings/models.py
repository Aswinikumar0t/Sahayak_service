import random
import time
from django.db import models
from django.conf import settings

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_METHOD = [
        ('online', 'Online Payment'),
        ('cash', 'Cash on Service'),
        ('wallet', 'Wallet'),
    ]
    
    # Basic Information
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='bookings', 
        null=True, 
        blank=True
    )
    
    # Service Details
    service_type = models.CharField(max_length=50)
    plan_type = models.CharField(max_length=20)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Time Details
    booking_date = models.DateField()
    booking_time = models.TimeField()
    
    # Address Details
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=255, blank=True)
    
    # Contact Details
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    instructions = models.TextField(blank=True)
    
    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            timestamp = int(time.time())
            random_num = random.randint(1000, 9999)
            self.booking_id = f"SAH{timestamp}{random_num}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.service_type}"