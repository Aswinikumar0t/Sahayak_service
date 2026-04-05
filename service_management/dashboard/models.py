from django.db import models


# Create your models here.
class ServicePartner(models.Model):
    PARTNER_TYPE_CHOICES = [
        ('corporate', 'Corporate Partner'),
        ('solo', 'Solo Partner'),
    ]

    name = models.CharField(max_length=200)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"


from django.db import models

# No other imports here - just Django imports

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sub_categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class RatePlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('hourly', 'Per Hour'),
        ('fixed', 'Fixed Price'),
        ('daily', 'Per Day'),
        ('package', 'Package'),
        ('emergency', 'Emergency'),
        ('contract', 'Contract'),
    ]
    
    PLAN_FOR_CHOICES = [
        ('b2c', 'Individual Customer'),
        ('b2b', 'Corporate Client'),
        ('both', 'Both'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    min_hours = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    plan_for = models.CharField(max_length=10, choices=PLAN_FOR_CHOICES, default='both')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name