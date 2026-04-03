from apps.products.models import UserSelection


class UserSelectionService:
    @staticmethod
    def save_selection(user_id: str, external_product_id: str) -> None:
        UserSelection.objects.create(
            whatsapp_user_id=user_id,
            product_reference_id=external_product_id,
        )
