import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from .models import Comments
from blog.models import Blog
from account.models import User


class CommentsType(DjangoObjectType):
    class Meta: 
        model = Comments
        fields = (
            'id', 'reply', 'author', 'body',
            'date', 'reply_to_reply', 'blog', 'likes',
            'un_likes',
            )  


class Query(graphene.ObjectType):
    comments = graphene.List(CommentsType)
    comment = graphene.Field(CommentsType, id=graphene.ID())

    def resolve_comments(root, info, **kwargs):
        # Querying a list
        return Comments.objects.all()

    def resolve_comment(root, info, id, **kwargs):
        # Querying a object
        return Comments.objects.get(id=id)
 

class CommentsInput(graphene.InputObjectType):
    author = graphene.String()
    body = graphene.String()
    reply = graphene.String()
    reply_to_reply = graphene.String()
    blog = graphene.String()


class CreateComments(graphene.Mutation):
    class Arguments:
        input = CommentsInput(required=True)

    comment = graphene.Field(CommentsType)

    @login_required
    @staticmethod
    def mutate(root, info, input):
        author = User.objects.get(id=input.author)
        blog = Blog.objects.get(id=input.blog)
        

        comment = Comments.objects.create(
            body=input.body,
            author=author,
            blog=blog,
            )
        
        if input.reply != None:
            reply = Comments.objects.get(reply=input.reply)
            comment.reply = input.reply
        if input.reply_to_reply != None:
            reply_to_reply = Comments.objects.get(reply_to_reply=input.reply_to_reply)
            comment.reply_to_reply = input.reply_to_reply

        comment.save()
        return CreateComments(comment=comment)


class UpdateComments(graphene.Mutation):
    class Arguments:
        input = CommentsInput(required=False)
        id = graphene.ID(required=True)

    comment = graphene.Field(CommentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, input, id):
        comment = Comments.objects.get(pk=id)
        if info.context.user == comment.author:
            comment.body = input.body
            comment.save()
        return UpdateComments(comment=comment)


class DeleteComments(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    comment = graphene.Field(CommentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        comment = Comments.objects.get(pk=id)
        if info.context.user == comment.author :
            comment.delete()
        return DeleteComments(comment=comment)


class LikeComments(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    comment = graphene.Field(CommentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        comment = Comments.objects.get(pk=id)
        user = info.context.user
        if user not in comment.likes.all() :
            comment.likes.add(user)
        else:
            comment.likes.remove(user)

        return LikeComments(comment=comment)


class UnLikeComments(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    comment = graphene.Field(CommentsType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        comment = Comments.objects.get(pk=id)
        user = info.context.user
        if user not in comment.un_likes.all() :
            comment.un_likes.add(user)
        else:
            comment.un_likes.remove(user)

        return UnLikeComments(comment=comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateComments.Field()
    update_comment = UpdateComments.Field()
    delete_comment = DeleteComments.Field()
    like_comment = LikeComments.Field()
    unlike_comment = UnLikeComments.Field()

