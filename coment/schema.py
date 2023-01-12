import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from .models import Coments
from blog.models import Blog
from account.models import User


class ComentsType(DjangoObjectType):
    class Meta: 
        model = Coments
        fields = (
            'id', 'one_coments', 'author', 'body',
            'date', 'tow_coments', 'blog', 'likes',
            'unlikes',
            )  


class Query(graphene.ObjectType):
    coments = graphene.List(ComentsType)
    coment = graphene.Field(ComentsType, id=graphene.ID())

    def resolve_coments(root, info, **kwargs):
        # Querying a list
        return Coments.objects.all()

    def resolve_coment(root, info, id, **kwargs):
        # Querying a object
        return Coments.objects.get(id=id)
 

class ComentsInput(graphene.InputObjectType):
    author = graphene.String()
    body = graphene.String()
    one_coments = graphene.String()
    tow_coments = graphene.String()
    blog = graphene.String()


class CreateComents(graphene.Mutation):
    class Arguments:
        input = ComentsInput(required=True)

    coment = graphene.Field(ComentsType)

    @login_required
    @staticmethod
    def mutate(root, info, input):
        author = User.objects.get(id=input.author)
        blog = Blog.objects.get(id=input.blog)
        
        coment = Coments()
        coment.body = input.body
        coment.author = author
        if input.one_coments != None:
            one_coments = Coments.objects.get(one_coments=input.one_coments)
            coment.one_coments = input.one_coments
        if input.tow_coments != None:
            tow_coments = Coments.objects.get(tow_coments=input.tow_coments)
            coment.tow_coments = input.tow_coments
        coment.blog = blog

        coment.save()
        return CreateComents(coment=coment)


class UpdateComents(graphene.Mutation):
    class Arguments:
        input = ComentsInput(required=False)
        id = graphene.ID(required=True)

    coment = graphene.Field(ComentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, input, id):
        coment = Coments.objects.get(pk=id)
        if info.context.user == coment.author:
            coment.body = input.body
            coment.save()
        return UpdateComents(coment=coment)


class DeleteComents(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    coment = graphene.Field(ComentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        coment = Coments.objects.get(pk=id)
        if info.context.user == coment.author :
            coment.delete()
        return DeleteComents(coment=coment)


class LikeComents(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    coment = graphene.Field(ComentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        coment = Coments.objects.get(pk=id)
        user = info.context.user
        if user not in coment.liles.all() :
            coment.likes.add(user)
        else:
            coment.likes.remove(user)

        return LikeComents(coment=coment)


class UnLikeComents(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    coment = graphene.Field(ComentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        coment = Coments.objects.get(pk=id)
        user = info.context.user
        if user not in coment.unliles.all() :
            coment.unlikes.add(user)
        else:
            coment.unlikes.remove(user)

        return UnLikeComents(coment=coment)


class Mutation(graphene.ObjectType):
    create_coment = CreateComents.Field()
    update_coment = UpdateComents.Field()
    delete_coment = DeleteComents.Field()
    like_coment = LikeComents.Field()
    unlike_coment = UnLikeComents.Field()

