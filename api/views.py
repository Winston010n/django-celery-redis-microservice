import time

from django.core.cache import cache
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import send_welcome_email_task


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()


class StatsView(APIView):
    def get(self, request):
        stats = cache.get("api:v1:stats")
        if stats is None:
            # Simulate a slow statistics calculation to make cache hits visible.
            time.sleep(2)
            stats = {"users_count": 1000, "active_orders": 42}
            cache.set("api:v1:stats", stats, timeout=60)
        return Response(stats)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        send_welcome_email_task.delay(email)
        return Response(
            {"message": "Registration accepted", "email": email.strip()},
            status=status.HTTP_201_CREATED,
        )
