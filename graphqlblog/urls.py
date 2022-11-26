from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from blog.schema import blog_schema
from account.schema import account_schema
from coment.schema import coment_schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("blog-graphql", GraphQLView.as_view(graphiql=True, schema=blog_schema)),
    path("account-graphql", GraphQLView.as_view(graphiql=True, schema=account_schema)),
    path("coment-graphql", GraphQLView.as_view(graphiql=True, schema=coment_schema)),
]
