from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from . import serializers
from user.models import AuthorAccount
import logging
from django.core.mail import EmailMultiAlternatives

class ContactUsViewset(APIView):
    serializer_class = serializers.ContactUsSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        user_id = request.data.get('user')

        try:
            user = AuthorAccount.objects.get(id=user_id)
        except AuthorAccount.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(user=user)
            self.send_email(serializer.validated_data)
            return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, contact_data):
        subject = 'Received Contact Message'
        message = f"""
            You have received a new contact message.

            Name: {contact_data.get('name')}
            Email: {contact_data.get('email')}
            Message: {contact_data.get('message')}
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL]
        )

        email.send()