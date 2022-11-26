import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from .models import Coments

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
    coment = graphene.Field(ComentsType, id=graphene.String())

    def resolve_coments(root, info, **kwargs):
        # Querying a list
        return Coments.objects.all()
    def resolve_coment(root, info, **kwargs):
        # Querying a detail
        return Coments.objects.get(id=kwargs['id'])
 
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
    @classmethod
    def mutate(cls, root, info, input):
        coment = Coments()
        coment.body = input.body
        coment.author = input.author
        coment.one_coments = input.one_coments
        coment.tow_coments = input.tow_coments
        coment.blog = input.blog

        coment.save()
        return CreateComents(coment=coment)

class UpdateComents(graphene.Mutation):
    class Arguments:
        input = ComentsInput(required=True)
        id = graphene.ID()

    coment = graphene.Field(ComentsType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, input, id):
        coment = Coments.objects.get(pk=id)
        if self.request.user == coment.author:
            coment.body = input.body
            coment.save()
        return UpdateComents(coment=coment)

class DeleteComents(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    coment = graphene.Field(ComentsType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        coment = Coments.objects.get(pk=id)
        if self.request.user == coment.author :
            coment.delete()
        return DeleteComents(coment=coment)

class LikeComents(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    coment = graphene.Field(ComentsType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        coment = Coments.objects.get(pk=id)
        user = self.request.user
        if user not in coment.liles.all() :
            coment.likes.add(user)
        else:
            coment.likes.remove(user)

        return LikeComents(coment=coment)

class UnLikeComents(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    coment = graphene.Field(ComentsType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        coment = Coments.objects.get(pk=id)
        user = self.request.user
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

coment_schema = graphene.Schema(query=Query, mutation=Mutation)