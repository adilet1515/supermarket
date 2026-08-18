
from timeit import default_timer
from django.urls import reverse_lazy, reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, Permission
from .models import Product, Order
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView
from .forms import ProductCreateForm

def index_view(request: HttpRequest):
    # print("path: ",request.path)
    # print("method: ",request.method)
    # print("headers: ",request.headers)
    # return HttpResponse("<h1>Hello, products!!!</h1>")
    products = [
        ("Milk",109),
        ("Bread", 59),
        ("Water", 39),
        ("Cheese", 149),
    ]
    context = {
        "time_running":default_timer(),
        "products":products,
    }
    return render(
        request,
        template_name='products/index.html',
        context=context,
    )

class IndexView(TemplateView):
    template_name = 'products/index.html'

    extra_context = {
        "page_title": "Products index page",
    }


    def get_context_data(self, **kwargs):
        products = [
            ("Milk", 109),
            ("Bread", 59),
            ("Water", 39),
            ("Cheese", 149),
        ]
        context = super().get_context_data(**kwargs)
        context.update(
            time_running=default_timer(),
            products=products,
        )
        return context


def groups_list(request: HttpRequest):
    context = {
        "groups":Group.objects.prefetch_related("permissions").all(),
    }
    return render(
        request,
        template_name='products/groups-list.html',
        context=context,
    )

class GroupsListView(ListView):
    template_name = 'products/groups-list.html'
    # model = Group
    queryset = Group.objects.prefetch_related("permissions").all()
    context_object_name = "groups"

class GroupDetailView(DetailView):
    template_name = 'products/group-detail.html'
    # model = Group
    queryset = Group.objects.prefetch_related("permissions").all()
    context_object_name = "group"

class PermissionsListView(ListView):
    template_name = 'products/group_permissions.html'
    # queryset =
    model = Permission
    context_object_name = "permissions"


    def get_queryset(self):
        print("hello get query set")
        qs = super().get_queryset()
        group: Group = get_object_or_404(Group, name=self.kwargs["name"])
        self.kwargs["group"] = group
        # return qs.filter(group_set__pk=group.pk)
        # return qs.filter(group__name=group.name)
        return group.permissions.all()


    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update(group = self.kwargs["group"])
        print("context", context)
        return context


def products_list(request: HttpRequest):
    context = {
        "products": (Product
                     .objects
                     .filter(archived=False)
                     .order_by("-name")
                     .all()),
    }
    return render(
        request,
        template_name='products/products-list.html',
        context=context,
    )
class ProductsListView(ListView):
    # model = Product
    queryset = Product.objects.filter(archived=False)
    ordering = "-name",

class ProductDetailView(DetailView):
    # model = Product
    queryset = Product.objects.filter(archived=False)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("products:products")

    def form_valid(self, form):
        success_url = self.get_success_url()
        # self.object.delete()
        self.object: Product
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class ProductCreateView(CreateView):
    # template_name = 'products/product-create.html'
    model = Product
    # fields = ['name', "description"]
    form_class = ProductCreateForm
    # success_url = reverse_lazy("products:products")
    # success_url = reverse_lazy("products:product-detail")
    
    def get_success_url(self):
        return reverse('products:product-detail', kwargs={'pk': self.object.pk})

def orders_list(request: HttpRequest):
    context = {
        "orders": (
            Order
           .objects
           .select_related("user")
            .prefetch_related("product")
            .order_by("pk")
           .all()),
    }
    return render(
        request,
        template_name='products/orders-list.html',
        context=context,
    )

