from django.forms import ModelForm, CharField

from products.models import Product


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']

    name = CharField(label="Product Name", max_length=60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            print("name: ",name, "field: ", field, "w", field.widget)
            field.widget.attrs['class'] = 'model-form'

    def save(self, commit=True):
        instance:Product = super().save(commit=False)
        if not instance.description:
            instance.description = f'Product {instance.name} description demo'

        instance.save()
        return instance