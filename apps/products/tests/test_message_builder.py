from django.test import SimpleTestCase

from apps.products.whatsapp.message_builder import WhatsAppMessageBuilder


class WhatsAppMessageBuilderTest(SimpleTestCase):
    def test_build_product_details(self):
        product = {
            "name": "Malbec",
            "brand": "O Boticário",
            "description": "Perfume amadeirado",
            "price": 199.90,
            "url": "https://example.com/produto",
        }

        message = WhatsAppMessageBuilder.build_product_details(product)

        self.assertIn("*Malbec*", message)
        self.assertIn("Marca: O Boticário", message)
        self.assertIn("R$ 199.90", message)
        self.assertIn("Comprar:", message)

    def test_build_list_row(self):
        row = WhatsAppMessageBuilder.build_list_row({
            "external_id": "SKU123",
            "name": "Malbec X Desodorante Colônia",
            "description": "Descrição longa do perfume amadeirado sofisticado e intenso",
            "price": 199.90,
        })

        self.assertEqual(row["id"], "SKU123")
        self.assertLessEqual(len(row["title"]), 20)
        self.assertLessEqual(len(row["description"]), 72)

    def test_build_list_row_sem_external_id(self):
        row = WhatsAppMessageBuilder.build_list_row({
            "name": "Produto sem id"
        })

        self.assertIsNone(row)
