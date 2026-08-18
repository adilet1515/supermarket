from django.urls import path
from django.views.generic import TemplateView


from .views import (
    index_view,
    groups_list,
    products_list,
    orders_list,
    IndexView,
    GroupsListView,
    GroupDetailView,
    PermissionsListView,
    ProductsListView,
    ProductDetailView,
    ProductDeleteView,
    ProductCreateView
    )
app_name = 'products'


urlpatterns = [
    # path("", index_view, name="index"),
    # path("", TemplateView.as_view(template_name="products/index.html"), name="index"),
    path("", IndexView.as_view(), name="index"),
    # path("groups/", groups_list, name="groups"),
    path("groups/", GroupsListView.as_view(), name="groups"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/<name>/permissions/", PermissionsListView.as_view(), name="group-permissions"),
    # path("list/", products_list, name="products"),
    path("list/", ProductsListView.as_view(), name="products"),
    path("<int:pk>/", ProductDetailView.as_view() , name="product-detail"),
    path("<int:pk>/confirm-delete", ProductDeleteView.as_view() , name="delete-product"),
    path("create/", ProductCreateView.as_view() , name="create-product"),
    path("orders/",orders_list, name="orders"),
]
