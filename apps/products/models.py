from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()

    flavor = models.CharField(max_length=50, null=True, blank=True)
    target = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    