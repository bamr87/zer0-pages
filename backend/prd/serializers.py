from rest_framework import serializers
from .models import PRD

class PRDSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    repository_name = serializers.ReadOnlyField(source='repository.name', allow_null=True)

    class Meta:
        model = PRD
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')

