# Beauty AI Assistant

Assistente de recomendação de produtos com integração entre:

- **Django**
- **Elasticsearch**
- **Web Scraping**
- **WhatsApp Cloud API**

O projeto coleta produtos de e-commerce, persiste no banco, indexa no Elasticsearch e permite busca/recomendação via API e WhatsApp.

---

## Features

- Scraping de produtos do site do Boticário
- Persistência em banco com Django ORM
- Indexação e busca com Elasticsearch
- API REST para busca de produtos
- Integração com WhatsApp Webhook
- Fluxo de recomendação com listas, botões e CTA

---

## Arquitetura

O projeto foi reorganizado para uma estrutura mais modular e sustentável:

```bash
apps/products/
├── management/
│   └── commands/
│       └── scraper_products.py
├── parsers/
│   └── whatsapp_webhook_parser.py
├── scraper/
│   └── boticario.py
├── services/
│   ├── product_context_service.py
│   ├── product_recommendation_service.py
│   ├── product_search_service.py
│   ├── user_selection_service.py
│   └── whatsapp_webhook_service.py
├── views/
│   ├── api_views.py
│   └── webhook_views.py
├── whatsapp/
│   ├── client.py
│   ├── handlers.py
│   └── presenters.py
├── constants.py
├── dto.py
├── exceptions.py
├── documents.py
├── models.py
└── urls.py
