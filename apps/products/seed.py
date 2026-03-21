from faker import Faker
import random
from apps.products.models import Product

fake = Faker("pt_BR")

brands = ["Malbec", "Floratta", "Egeo", "Lily", "Zaad", "Quasar"]
notes = ["doce", "floral", "amadeirado", "cítrico", "baunilha", "fresco"]
targets = ["feminino", "masculino", "unissex"]

def run():
    for _ in range(50):
        brand = random.choice(brands)
        note = random.choice(notes)
        target = random.choice(targets)

        name = f"{brand} {fake.word().capitalize()}"
        description = f"Perfume {target} com fragrância {note} e toque {fake.word()}"

        Product.objects.create(
            name=name,
            description=description,
            price=round(random.uniform(80, 200), 2),
            category="perfume"
        )

    print("Perfumes gerados com sucesso!")