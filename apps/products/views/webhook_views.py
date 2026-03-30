import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from apps.products.services.whatsapp_webhook_service import WhatsAppWebhookService


@csrf_exempt
def whatsapp_webhook(request):
    # ==================================================
    # META WEBHOOK VERIFICATION (GET)
    # ==================================================
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return HttpResponse(challenge, status=200)

    return JsonResponse(
        {
            "status": "error",
            "message": "Webhook verification failed",
            "received_mode": mode,
            "received_token": verify_token,
        },
        status=403
    )

    # ==================================================
    # WHATSAPP INCOMING MESSAGE (POST)
    # ==================================================
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))

            service = WhatsAppWebhookService()
            service.process(payload)

            return JsonResponse({"status": "ok"}, status=200)

        except Exception as exc:
            return JsonResponse(
                {"status": "error", "message": str(exc)},
                status=500
            )

    return JsonResponse({"detail": "Method not allowed"}, status=405)