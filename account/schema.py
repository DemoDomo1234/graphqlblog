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
    user = graphene.Field(UserType, id=graphene.String())

    def resolve_user(root, info, **kwargs):
        # Querying a detail
        return User.objects.get(id=kwargs['id'])
 
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

    @login_required
    @classmethod
    def mutate(cls, root, info, input):
        user = User()
        user.username = input.username
        user.name = input.name
        user.email = input.email
        user.body = input.body
        user.image = input.image

        user.save()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
        id = graphene.ID()

    user = graphene.Field(UserType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, input, id):
        user = User.objects.get(pk=id)
        if self.request.user.id == user.id:
            user.name = input.name
            user.email = input.email
            user.body = input.body
            user.image = input.image
            user.save()
        return UpdateUser(user=user)

class FolowUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    user = graphene.Field(UserType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        user = User.objects.get(pk=id)
        myuser = self.request.user
        if myuser not in user.folower.all() :
            user.folower.add(myuser)
        else:
            user.folower.remove(myuser)

        return FolowUser(user=user)

class NotyUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    user = graphene.Field(UserType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        user = User.objects.get(pk=id)
        myuser = self.request.user
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

account_schema = graphene.Schema(query=Query, mutation=Mutation)