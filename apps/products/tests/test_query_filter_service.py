from django.test import SimpleTestCase

from apps.products.services.query_filter_service import QueryFilterService


class QueryFilterServiceTest(SimpleTestCase):
    def setUp(self):
        self.service = QueryFilterService()

    def test_extract_filters_deve_identificar_target(self):
        filters = self.service.extract_filters("perfume masculino")
        self.assertIn(("target", "masculino"), filters)

    def test_extract_filters_deve_identificar_flavor_sem_acentos(self):
        filters = self.service.extract_filters("perfume citrico")
        self.assertIn(("flavor", "cítrico"), filters)

    def test_extract_filters_deve_identificar_categoria_composta(self):
        filters = self.service.extract_filters("body splash floral")
        self.assertIn(("category", "body splash"), filters)
        self.assertIn(("flavor", "floral"), filters)

    def test_extract_filters_nao_deve_duplicar(self):
        filters = self.service.extract_filters("perfume perfume feminino feminino")
        self.assertEqual(len(filters), len(set(filters)))

    def test_clean_query_remove_termos_de_filtro(self):
        cleaned = self.service.clean_query("perfume feminino boticario floral")
        self.assertEqual(cleaned, "boticario")
