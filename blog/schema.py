import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from .models import Blog
from account.models import User


class BlogType(DjangoObjectType):
    class Meta: 
        model = Blog
        fields = (
            'id', 'title', 'author', 'body',
            'date', 'image', 'saved', 'likes',
            )  


class Query(graphene.ObjectType):
    blogs = graphene.List(BlogType)
    blog = graphene.Field(BlogType, id=graphene.ID())

    def resolve_blogs(root, info, **kwargs):
        # Querying a list
        return Blog.objects.all()

    def resolve_blog(root, info, id, **kwargs):
        # Querying a object
        return Blog.objects.get(id=id)
 

class BlogInput(graphene.InputObjectType):
    title = graphene.String()
    author = graphene.String()
    body = graphene.String()
    image = graphene.String()


class CreateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInput(required=True)

    blog = graphene.Field(BlogType)
    
    @login_required
    @staticmethod
    def mutate(root, info, input, **kwargs):
        author = User.objects.get(id=input.author)
        blog = Blog.objects.create(
            title=input.title,
            author=author,
            body=input.body,
            image=input.image,
        )
        blog.save()
        return CreateBlog(blog=blog)


class UpdateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInput(required=False)
        id = graphene.ID(required=True)

    blog = graphene.Field(BlogType)
    
    @login_required
    @staticmethod
    def mutate(root, info, input, id):
        blog = Blog.objects.get(pk=id)
        if info.context.user == blog.author :
            if input.title != None :
                blog.title = input.title
            if input.body != None :
                blog.body = input.body
            if input.image != None :
                blog.image = input.image
        blog.save()
        return UpdateBlog(blog=blog)


class DeleteBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    blog = graphene.Field(BlogType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        blog = Blog.objects.get(pk=id)
        if info.context.user == blog.author :
            blog.delete()
            return DeleteBlog(blog=blog)


class LikeBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    blog = graphene.Field(BlogType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        blog = Blog.objects.get(pk=id)
        user = info.context.user
        if user not in blog.likes.all() :
            blog.likes.add(user)
        else:
            blog.likes.remove(user)

        return LikeBlog(blog=blog)


class SaveBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    blog = graphene.Field(BlogType)
    
    @login_required
    @staticmethod
    def mutate(root, info, id):
        blog = Blog.objects.get(pk=id)
        user = info.context.user
        if user not in blog.saved.all() :
            blog.saved.add(user)
        else:
            blog.saved.remove(user)

        return SaveBlog(blog=blog)


class Mutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    delete_blog = DeleteBlog.Field()
    like_blog = LikeBlog.Field()
    save_blog = SaveBlog.Field()
