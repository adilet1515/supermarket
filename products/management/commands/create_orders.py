from django.contrib.auth.models import User
from django.core.management import BaseCommand

from products.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        products_names = [
            "Tablet",
            "Smartphone",
            "Display",
        ]
        self.stdout.write(
            self
            .style.SUCCESS(
                "Create some products"
            )
        )
        for name in products_names:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "description": f"description: {name}",
                },

            )
            self.stdout.write(
                f"Created ({created}) product {product}"
                )
        user = User.objects.first()
        products = Product.objects.all()
        for product in products: # type: Product
            order, created = Order.objects.get_or_create(
                promocode=f"{product.pk}_{product.name}".lower(),
                delivery_address=f"ul Kenesary {product.description}",
                user=user,
            )
            if not created:
                continue
            order.product.add(product)

            order.save()

            self.stdout.write(f"Saved order {order}")

        self.stdout.write(
            self.style.SUCCESS(
                "Create some orders"
            )
        )


