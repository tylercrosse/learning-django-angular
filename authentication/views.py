
import json

from django.contrib.auth import authenticate, login

from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from authentication.permissions import IsAccountOwner
from authentication.models import Account
from authentication.serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body.decode())
        print data

        email = data.get('email', None)
        password = data.get('password', None)

        account = authenticate(email=email, password=password)
        print account

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)
