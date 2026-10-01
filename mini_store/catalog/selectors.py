from django.db.models import QuerySet

from catalog.models import Product


def get_products(
    *,
    lang: str = "ar",
    category_slug: str | None = None,
    search: str | None = None,
    ordering: str | None = None,
) -> QuerySet[Product]:
    qs = Product.objects.filter(is_active=True).select_related("category")

    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    if search:
        if lang == "en":
            qs = qs.filter(name_en__icontains=search)
        else:
            qs = qs.filter(name_ar__icontains=search)

    if ordering in ["price", "-price", "created_at", "-created_at"]:
        qs = qs.order_by(ordering)
    else:
        qs = qs.order_by("-created_at")

    return qs


def get_product_by_id(*, product_id: int) -> Product | None:
    return Product.objects.filter(id=product_id, is_active=True).first()
