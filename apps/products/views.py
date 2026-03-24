from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch import ConnectionError
from elasticsearch_dsl import Search, Q
from django.db.models import Q as DjangoQ
from .models import Product
from .serializers import ProductSerializer
from .es_client import es  # cliente centralizado com basic_auth
from django.http import HttpResponse
import requests
from .services import search_products_in_es
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def search_products(request):
    query = request.GET.get("q", "").lower()
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))
    mode = request.GET.get("mode", "default")
    target = request.GET.get("target", None)

    if not query:
        return Response([])

    try:
        # tokens da query
        tokens = query.split()

        if mode == "autocomplete":
            q = Q("multi_match", query=query,
                  fields=["name^3", "brand", "flavor", "target"],
                  type="phrase_prefix")
            s = Search(using=es, index="products").query(q).filter("term", is_active=True)

            # aplica filtros automáticos
            if "feminino" in tokens:
                s = s.filter("term", target="feminino")
            elif "masculino" in tokens:
                s = s.filter("term", target="masculino")

            if "cítrico" in tokens:
                s = s.filter("term", flavor="cítrico")
            elif "amadeirado" in tokens:
                s = s.filter("term", flavor="amadeirado")

            s = s[:5]
            response = s.execute()

            results = [
                {
                    "id": hit.meta.id,
                    "name": hit.name,
                    "brand": hit.brand,
                    "flavor": hit.flavor,
                    "target": hit.target
                }
                for hit in response
            ]
            return Response(results)

        else:
            q = Q("multi_match", query=query,
                  fields=["name^3", "description", "brand", "flavor", "target"],
                  fuzziness="AUTO")
            s = Search(using=es, index="products").query(q).filter("term", is_active=True)

            # aplica filtros automáticos
            if "feminino" in tokens:
                s = s.filter("term", target="feminino")
            elif "masculino" in tokens:
                s = s.filter("term", target="masculino")

            if "cítrico" in tokens:
                s = s.filter("term", flavor="cítrico")
            elif "amadeirado" in tokens:
                s = s.filter("term", flavor="amadeirado")

            if target:
                s = s.filter("term", target=target)

            start = (page - 1) * size
            s = s[start:start + size]
            response = s.execute()

            results = [hit.to_dict() for hit in response]

            return Response({
                "page": page,
                "size": size,
                "total": response.hits.total.value,
                "results": results
            })

    except ConnectionError:
        queryset = Product.objects.filter(is_active=True).filter(
            DjangoQ(name__icontains=query) |
            DjangoQ(description__icontains=query) |
            DjangoQ(brand__icontains=query)
        )

        # aplica filtros automáticos também no fallback ORM
        if "feminino" in query:
            queryset = queryset.filter(target="feminino")
        elif "masculino" in query:
            queryset = queryset.filter(target="masculino")

        if "cítrico" in query:
            queryset = queryset.filter(flavor="cítrico")
        elif "amadeirado" in query:
            queryset = queryset.filter(flavor="amadeirado")

        if target:
            queryset = queryset.filter(target=target)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

import json

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        # Verificação do webhook
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

            # Verifica se existe mensagem
            if "entry" in data and "changes" in data["entry"][0]:
                value = data["entry"][0]["changes"][0]["value"]
                if "messages" in value:
                    message = value["messages"][0]["text"]["body"]
                    sender = value["messages"][0]["from"]

                    print("Mensagem recebida:", message)

                    # Consultar o ES
                    results = search_products_in_es(message)

                    # Responder pelo WhatsApp
                    send_whatsapp_message(sender, results)

            return HttpResponse("EVENT_RECEIVED", status=200)

        except Exception as e:
            print("Erro ao processar webhook:", str(e))
            return HttpResponse("ERROR", status=400)

    return HttpResponse("METHOD_NOT_ALLOWED", status=405)

def send_whatsapp_message(to, results):
    total = len(results)
    shown_results = results[:3]  # mostra só os 3 primeiros

    if total == 0:
        text = "Não encontrei produtos para sua busca. Deseja tentar outra categoria?"
    else:
        text = f"Encontrei {total} perfumes relacionados. Aqui estão os {len(shown_results)} primeiros:\n"
        for r in shown_results:
            # se tiver preço, pode incluir também
            price = r.get("price", None)
            if price:
                text += f"- {r['name']} ({r['brand']}) - R$ {price}\n"
            else:
                text += f"- {r['name']} ({r['brand']})\n"

        if total > len(shown_results):
            text += "\nResponda 'mais' para ver outros."

    url = "https://graph.facebook.com/v25.0/1105730849281197/messages"
    headers = {
        "Authorization": "Bearer SEU_ACCESS_TOKEN_REAL",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Resposta do Cloud API:", response.status_code, response.text)