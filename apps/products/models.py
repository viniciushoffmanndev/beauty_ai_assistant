from django.db import models

class Product(models.Model):
    # Identificação
    external_id = models.CharField(max_length=100)
    source = models.CharField(max_length=100)  # ex: boticario

    # Básico
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    
    # Preços
    price = models.FloatField()
    old_price = models.FloatField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)

    # Avaliação
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)

    # Conteúdo
    description = models.TextField(null=True, blank=True)

    # Mídia / links
    url = models.URLField()
    image = models.URLField(null=True, blank=True)

    # Controle
    is_active = models.BooleanField(default=True)
    scraped_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("external_id", "source")

    def __str__(self):
        return f"{self.name} ({self.source})"
    