from rest_framework import serializers
from .models import Blog , BlogComment 

class BlogSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField('username' , read_only = True)

    class Meta:
        model = Blog
        fields = '__all__'

    def get_comments(self , obj):
        data = obj.comment.filter(publish=True)
        return BlogCommentSerializer(data , many=True).data
    

class BlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = [
            'id',
            'author',
            'title',
            'description',
            'created',
            'slug',
            'category',
            'image',
        ]


class BlogCommentSerializer(serializers.ModelSerializer):
    blog_post = serializers.SlugRelatedField('title' , read_only = True)

    class Meta:
        model = BlogComment
        exclude = ['publish']

