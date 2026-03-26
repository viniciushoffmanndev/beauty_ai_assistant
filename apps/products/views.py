import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch_dsl import Q, Search
from .models import Product
from .serializers import ProductSerializer
from apps.products.whatsapp.handlers import handle_whatsapp_message
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
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == "whatsapp_webhook":
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("VERIFICATION_FAILED", status=403)

    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print("Payload recebido:", data)

            if "entry" in data and "changes" in data["entry"][0]:
                value = data["entry"][0]["changes"][0]["value"]
                if "messages" in value:
                    message = value["messages"][0]["text"]["body"]
                    sender = value["messages"][0]["from"]

                    print("Mensagem recebida:", message)

                    # Chama o handler para processar e responder
                    handle_whatsapp_message(sender, message)

            return HttpResponse("EVENT_RECEIVED", status=200)

        except Exception as e:
            print("Erro ao processar webhook:", str(e))
            return HttpResponse("ERROR", status=400)

    return HttpResponse("METHOD_NOT_ALLOWED", status=405)