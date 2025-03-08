from .serializers import CommentSerializer
data = {'lesson':1, 'user':1}
serializer = CommentSerializer(data=data)
print(serializer.is_valid())