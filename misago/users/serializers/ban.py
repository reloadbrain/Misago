from rest_framework import serializers

from django.utils.translation import ugettext as _

from misago.core.utils import format_plaintext_for_html
from misago.users.models import Ban


def serialize_message(message):
    if message:
        return {
            'plain': message,
            'html': format_plaintext_for_html(message),
        }
    else:
        return None


class BanMessageSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Ban
        fields = [
            'detail',
            'expires_on',
        ]

    def get_detail(self, obj):
        if obj.user_message:
            message = obj.user_message
        elif obj.check_type == Ban.IP:
            message = _("Your IP address is banned.")
        else:
            message = _("You are banned.")

        return serialize_message(message)


class BanDetailsSerializer(serializers.ModelSerializer):
    user_message = serializers.SerializerMethodField()
    staff_message = serializers.SerializerMethodField()

    class Meta:
        model = Ban
        fields = [
            'user_message',
            'staff_message',
            'expires_on',
        ]

    def get_user_message(self, obj):
        return serialize_message(obj.user_message)

    def get_staff_message(self, obj):
        return serialize_message(obj.staff_message)
