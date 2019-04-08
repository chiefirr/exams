from rest_framework import serializers

from exams_api.models import MarksRange


class MarksRangekBaseSerializer(serializers.ModelSerializer):
    """Base marks range serializer"""
    default_error_messages = {
        "bad_range": "Your ranges are not sorted ascendingly.",
    }

    class Meta:
        model = MarksRange
        fields = ('id', 'very_bad', 'bad', 'moderate', 'good', 'very_good',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        if not attrs['very_bad'] < attrs['bad'] < attrs['moderate'] < attrs['good'] < attrs['very_good']:
            self.fail("bad_range")
        return attrs
