from rest_framework import serializers
from communities.models import Comment

class CommentListSerializer(serializers.ModelSerializer): # 게시글 댓글을 보기위한 Serializer
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields='__all__'