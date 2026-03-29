from apps.products.models import UserSelection


class UserSelectionService:
    @staticmethod
    def save_selection(user_id: str, product_id: str) -> None:
        UserSelection.objects.create(
            user_id=user_id,
            product_id=product_id,
        )