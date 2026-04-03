# Testes adicionados - Parte 3

## Arquivos
- `test_query_filter_service.py`
- `test_whatsapp_webhook_parser.py`
- `test_whatsapp_webhook_service.py`
- `test_handlers.py`
- `test_message_builder.py`

## O que está sendo validado
- extração de filtros semânticos
- limpeza da query
- parsing do payload do webhook do WhatsApp
- fluxo do serviço do webhook
- handlers do WhatsApp
- builder de mensagens

## Como rodar

### Rodar todos os testes do app
```bash
python manage.py test apps.products.tests
```

### Rodar um arquivo específico
```bash
python manage.py test apps.products.tests.test_handlers
```

### Rodar uma classe específica
```bash
python manage.py test apps.products.tests.test_handlers.WhatsAppHandlersTest
```

## Observações
Se algum import quebrar, o motivo mais provável é diferença entre:
- sua estrutura atual do projeto
- a estrutura refatorada da Parte 1 + Parte 2

Nesse caso, ajuste apenas os imports mantendo a lógica dos testes.
