from rest_framework import serializers
from .models import Task , Project , Comment

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['id','title','description','project','assigned_to','created_by','status','priority','due_date','created_at','updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = '__all__'
        fields = ['id','name','description','members','created_by','status','start_date','end_date','created_at','updated_at']
        read_only_fields = ['created_by' , 'created_at' , 'id']  # id bhi read only hona chahiye

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['task','author','content']