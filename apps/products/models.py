from django.db import models


class ProductSource(models.TextChoices):
    BOTICARIO = "boticario", "Boticário"


class ProductTarget(models.TextChoices):
    FEMININO = "feminino", "Feminino"
    MASCULINO = "masculino", "Masculino"
    UNISSEX = "unissex", "Unissex"


class ProductCategory(models.TextChoices):
    PERFUME = "perfume", "Perfume"
    COLONIA = "colonia", "Colônia"
    BODY_SPLASH = "body splash", "Body Splash"
    DESODORANTE = "desodorante", "Desodorante"


class Product(models.Model):
    # Identificação externa
    external_id = models.CharField(max_length=100, db_index=True)
    source = models.CharField(
        max_length=50,
        choices=ProductSource.choices,
        db_index=True,
    )

    # Básico
    name = models.CharField(max_length=255, db_index=True)
    brand = models.CharField(max_length=100, blank=True, default="")

    # Classificação semântica
    target = models.CharField(
        max_length=20,
        choices=ProductTarget.choices,
        null=True,
        blank=True,
        db_index=True,
    )
    category = models.CharField(
        max_length=50,
        choices=ProductCategory.choices,
        null=True,
        blank=True,
        db_index=True,
    )
    flavor = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        help_text="Família olfativa ou perfil aromático",
    )

    # Preços
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    discount = models.PositiveIntegerField(null=True, blank=True)

    # Avaliação
    rating = models.FloatField(null=True, blank=True)
    review_count = models.PositiveIntegerField(null=True, blank=True)

    # Conteúdo
    description = models.TextField(null=True, blank=True)

    # Mídia / links
    url = models.URLField()
    image = models.URLField(null=True, blank=True)

    # Controle
    is_active = models.BooleanField(default=True, db_index=True)
    scraped_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("external_id", "source")
        indexes = [
            models.Index(fields=["source", "external_id"]),
            models.Index(fields=["name", "brand"]),
            models.Index(fields=["is_active", "source"]),
        ]
        ordering = ["-scraped_at"]

    def __str__(self):
        return f"{self.name} ({self.source})"


class UserSelection(models.Model):
    whatsapp_user_id = models.CharField(max_length=30, db_index=True)
    product_reference_id = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["whatsapp_user_id", "-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.whatsapp_user_id} escolheu "
            f"{self.product_reference_id} em {self.created_at}"
        )