from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Detail, Transaction
from .serializers import UserDetailsSerializer, TransactionSerializer, RegisterSerializer, FinancialDetailsSerializer, \
    ChangePasswordSerializer, CreateTransactionSerializer, UpdateTransactionSerializer, DestroyTransactionSerializer


# Create your views here.


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterSerializer
    model = User
    permission_classes = []


class RetrieveUserDetailsView(ListAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.request.user.check_password(request.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            if request.data.get("new_password") != request.data.get("password_confirm"):
                response = {
                    'status': 'failed',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Password do not Match',
                    'data': []
                }
                return Response(response)
            request.user.set_password(request.data.get("new_password"))
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserDetailsView(UpdateAPIView):
    serializer_class = UserDetailsSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            try:
                request.user.first_name = request.data.get("first_name")
                request.user.last_name = request.data.get("last_name")
                request.user.username = request.data.get("username")
                request.user.email = request.data.get("email")
                request.user.save()
            except():
                response = {
                    'status': 'failed',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Unable to change',
                    'data': []
                }
                return Response(response)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Details Updated',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailsView(ListAPIView):
    serializer_class = FinancialDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Detail.objects.filter(user=self.request.user)


class TransactionList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    model = Transaction

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionListID(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    model = Transaction

    def get_queryset(self):
        print(self.kwargs)
        return Transaction.objects.filter(user=self.request.user, id=self.kwargs['id'])


class TransactionListMonth(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    model = Transaction

    # filterset_fields = ('get_month')

    def get_queryset(self):
        print(self.kwargs)
        query_set = Transaction.objects.filter(user=self.request.user)
        [print(object, object.get_month, self.kwargs['month'], type(object.get_month), type(self.kwargs['month'])) for
         object in query_set]

        print([object for object in query_set if object.get_month == self.kwargs['month']])
        return [object for object in query_set if object.get_month == self.kwargs['month']]


class CreateTransaction(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTransactionSerializer
    model = Transaction


class UpdateTransaction(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateTransactionSerializer
    model = Transaction
    queryset = Transaction.objects.all()


class DeleteTransaction(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DestroyTransactionSerializer
    model = Transaction
    queryset = Transaction.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.user != request.user:
                response = {
                    "success": False,
                    "message": "Object Not Found"
                }
                return Response(data=response, status=status.HTTP_204_NO_CONTENT)
            details = Detail.objects.filter(user=request.user)
            details = details[0]

            if instance.type == 0:
                details.income -= instance.amount
            elif instance.type == 1:
                details.housing -= instance.amount
            elif instance.type == 2:
                details.food -= instance.amount
            elif instance.type == 3:
                details.healthcare -= instance.amount
            elif instance.type == 4:
                details.transportation -= instance.amount
            elif instance.type == 5:
                details.recreation -= instance.amount
            elif instance.type == 6:
                details.miscellaneous -= instance.amount

            details.totalExpenditure = (
                    details.housing + details.food + details.healthcare + details.transportation + details.recreation + details.miscellaneous)
            details.savings = details.income - details.totalExpenditure
            details.save()
            self.perform_destroy(instance)
            response = {
                "success": True,
                "message": "Object Deleted"
            }
        except():
            response = {
                "success": False,
                "message": "Object Not Deleted"
            }
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)


class DeleteUser(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            response = {
                "success": True,
                "message": "User Deleted"
            }
        except():
            response = {
                "success": False,
                "message": "User Not Deleted"
            }
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)
