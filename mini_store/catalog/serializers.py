from rest_framework import serializers

from catalog.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "price", "stock", "is_active", "created_at")

    def get_name(self, obj: Product) -> str:
        lang = self.context.get("lang", "ar")
        return obj.name_en if lang == "en" else obj.name_ar
