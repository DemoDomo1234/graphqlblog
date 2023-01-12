import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType, ObjectType
from .models import User
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta: 
        model = User
        fields = (
            'id', 'username', 'name', 'email',
            'body', 'image', 'folower', 'notifications',
            )  


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())

    def resolve_user(root, info, id, **kwargs):
        # Querying a object
        return User.objects.get(id=id)


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    name = graphene.String()
    email = graphene.String()
    body = graphene.String()
    image = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    coment = graphene.Field(UserType)


    @staticmethod
    def mutate(root, info, input):
        user = User.objects.create(
        username = input.username, name = input.name,
        email = input.email, body = input.body,
        image = input.image,
        )
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=False)
        id = graphene.ID(required=True)

    user = graphene.Field(UserType)
    
    @login_required
    @staticmethod
    def mutate(root, info, input, id):
        user = User.objects.get(pk=id)
        if info.context.user.id == user.id:
            if input.name != None :
                user.name = input.name
            if input.email != None :
                user.email = input.email
            if input.body != None :
                user.body = input.body
            if input.image != None :
                user.image = input.image
        user.save()
        return UpdateUser(user=user)


class FolowUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    user = graphene.Field(UserType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        user = User.objects.get(pk=id)
        myuser = info.context.user
        if myuser not in user.folower.all() :
            user.folower.add(myuser)
        else:
            user.folower.remove(myuser)

        return FolowUser(user=user)


class NotyUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    user = graphene.Field(UserType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        user = User.objects.get(pk=id)
        myuser = info.context.user
        if user not in user.notifications.all() :
            user.notifications.add(myuser)
        else:
            user.notifications.remove(myuser)

        return NotyUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    folow_user = FolowUser.Field()
    noty_user = NotyUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
 