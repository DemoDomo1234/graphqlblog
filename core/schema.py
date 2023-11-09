import graphene
from blog.schema import Query as BlogQuery, Mutation as BlogMutation
from account.schema import Query as AccountQuery, Mutation as AccountMutation
from comment.schema import Query as CommentQuery, Mutation as CommentMutation


class Query(BlogQuery, AccountQuery, CommentQuery):

    pass

class Mutation(BlogMutation, AccountMutation, CommentMutation):

    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
