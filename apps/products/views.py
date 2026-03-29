import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch_dsl import Q, Search
from .models import Product
from .serializers import ProductSerializer
from apps.products.whatsapp.handlers import handle_whatsapp_message, handle_list_reply, handle_button_reply
from apps.products.services  import search_products_in_es, buscar_produto_por_id
from apps.products.whatsapp.client import send_whatsapp_message, send_whatsapp_image, send_whatsapp_buttons, send_whatsapp_list
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

@api_view(['GET'])
def search_products(request):
    query = request.GET.get("q", "")  # parâmetro de busca opcional

    # Se não tiver query, retorna todos os produtos (limitado)
    if not query:
        resp = es.search(index="products", body={"query": {"match_all": {}}}, size=20)
    else:
        resp = es.search(
            index="products",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name", "brand", "description"]
                    }
                }
            },
            size=20
        )

    # Extrai apenas os documentos
    produtos = [hit["_source"] for hit in resp["hits"]["hits"]]

    return Response(produtos)

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            entry = data["entry"][0]["changes"][0]["value"]

            if "messages" in entry:
                for msg in entry["messages"]:
                    to = msg.get("from")
                    
                    # Caso seja mensagem interativa
                    if msg["type"] == "interactive":
                        if msg["interactive"]["type"] == "list_reply":
                            product_id = msg["interactive"]["list_reply"]["id"]
                            product = produtos_cache.get(product_id)
                            handle_list_reply(entry["contacts"][0]["wa_id"], product_id, product)
                        elif msg["interactive"]["type"] == "button_reply":
                            button_id = msg["interactive"]["button_reply"]["id"]
                            product = produtos_cache.get("produto_1")  # exemplo
                            handle_button_reply(entry["contacts"][0]["wa_id"], button_id, product)
                    
                    # Caso seja mensagem de texto normal
                    elif msg["type"] == "text":
                        query = msg["text"]["body"]
                        handle_whatsapp_message(to, query, msg)

            return JsonResponse({"status": "ok"})
        except Exception as e:
            print("Erro ao processar webhook:", e)
            return JsonResponse({"error": str(e)}, status=400)

    if request.method == "GET":
        verify_token = "meu_token_de_verificacao"
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return JsonResponse(int(challenge), safe=False)
        else:
            return JsonResponse({"error": "Verificação falhou"}, status=403)
