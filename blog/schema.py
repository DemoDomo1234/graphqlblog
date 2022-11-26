import graphene
from graphql_jwt.decorators import login_required
from graphene_django import DjangoObjectType
from .models import Blog

class BlogType(DjangoObjectType):
    class Meta: 
        model = Blog
        fields = (
            'id', 'title', 'author', 'body',
            'date', 'image', 'saved', 'likes',
            )  

class Query(graphene.ObjectType):
    blog = graphene.List(BlogType)

    def resolve_blog(root, info, **kwargs):
        # Querying a list
        return Blog.objects.all()
 
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
    @classmethod
    def mutate(cls, root, info, input):
        blog = Blog()
        blog.title = input.title
        blog.author = input.author
        blog.body = input.body
        blog.image = input.image
        blog.save()
        return CreateBlog(blog=blog)

class UpdateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInput(required=True)
        id = graphene.ID()

    blog = graphene.Field(BlogType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, input, id):
        blog = Blog.objects.get(pk=id)
        if self.request.user == blog.author :
            blog.title = input.title
            blog.body = input.body
            blog.image = input.image
            blog.save()
            return UpdateBlog(blog=blog)

class DeleteBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    blog = graphene.Field(BlogType)
    
    @login_required
    @classmethod
    def mutate(cls, root, info, id):
        blog = Blog.objects.get(pk=id)
        if self.request.user == blog.author :
            blog.delete()
            return DeleteBlog(blog=blog)

class LikeBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    blog = graphene.Field(BlogType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        blog = Blog.objects.get(pk=id)
        user = self.request.user
        if user not in blog.liles.all() :
            blog.likes.add(user)
        else:
            blog.likes.remove(user)

        return LikeBlog(blog=blog)

class SaveBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    blog = graphene.Field(BlogType)
    
    @login_required
    @classmethod
    def mutate(self, cls, root, info, id):
        blog = Blog.objects.get(pk=id)
        user = self.request.user
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

blog_schema = graphene.Schema(query=Query, mutation=Mutation)