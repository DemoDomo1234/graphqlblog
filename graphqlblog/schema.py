import graphene
from blog.schema import Query as BlogQuery, Mutation as BlogMutation
from account.schema import Query as AccountQuery, Mutation as AccountMutation
from coment.schema import Query as ComentQuery, Mutation as ComentMutation


class Query(BlogQuery, AccountQuery, ComentQuery):

    pass

class Mutation(BlogMutation, AccountMutation, ComentMutation):

    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
