from rest_framework import serializers
from .models import *

class CourseCreationSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(max_length=50)
    class Meta:
        model = Course
        fields = ('subject', 'course_name', 'description', 'lecture_price',
                  'package_size', 'thumbnail'
        )

    def validate_subject(self, value):
        subject = Subject.objects.filter(subject_name=value)
        if len(subject) == 0:
            raise serializers.ValidationError("There is no such subject.")
        return subject[0].pk
    
class LectureCreationSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=False)
    class Meta:
        model = Lecture
        fields = ('lecture_title','video')