import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.products.services.whatsapp_webhook_service import WhatsAppWebhookService


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if verify_token == "SEU_VERIFY_TOKEN":
            return HttpResponse(challenge)

        return HttpResponse("Token inválido", status=403)

    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            WhatsAppWebhookService.process(payload)
            return JsonResponse({"status": "ok"}, status=200)

        except Exception as exc:
            return JsonResponse(
                {"status": "error", "detail": str(exc)},
                status=500
            )

    return JsonResponse({"detail": "Método não permitido"}, status=405)