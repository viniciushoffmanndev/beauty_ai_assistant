import json
import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.products.services.whatsapp_webhook_service import WhatsAppWebhookService

logger = logging.getLogger(__name__)


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        return _handle_webhook_verification(request)

    if request.method == "POST":
        return _handle_webhook_event(request)

    return JsonResponse({"detail": "Method not allowed"}, status=405)


def _handle_webhook_verification(request):
    mode = request.GET.get("hub.mode")
    verify_token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    logger.info(
        "Webhook verification request | mode=%s | verify_token_received=%s",
        mode,
        bool(verify_token),
    )

    if mode == "subscribe" and verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return HttpResponse(challenge, status=200)

    logger.warning("Invalid webhook verify token")
    return HttpResponse("Invalid verify token", status=403)


def _handle_webhook_event(request):
    try:
        raw_body = request.body.decode("utf-8")
        logger.info("Incoming WhatsApp webhook payload: %s", raw_body)

        payload = json.loads(raw_body)

        service = WhatsAppWebhookService()
        service.process(payload)

        logger.info("WhatsApp webhook processed successfully")
        return JsonResponse({"status": "ok"}, status=200)

    except json.JSONDecodeError:
        logger.exception("Invalid JSON received in WhatsApp webhook")
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON payload"},
            status=400,
        )

    except Exception as exc:
        logger.exception("Error processing WhatsApp webhook")
        return JsonResponse(
            {"status": "error", "message": str(exc)},
            status=500,
        )
