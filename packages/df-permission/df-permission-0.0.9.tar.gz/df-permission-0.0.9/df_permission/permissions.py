from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import Q
from rest_framework.permissions import BasePermission


class DFMethods:
    CREATE = 'create'
    UPDATE = 'update'
    RETRIEVE = 'retrieve'
    LIST = 'list'
    DESTROY = 'destroy'


class DFPermission(BasePermission):
    def get_model_fields(self, view):
        """
        Get not related model fields
        """
        model = self.get_model(view)
        fields = [field.name for field in model._meta.get_fields()]
        return fields

    def get_fields(self, view):
        """
        Fields is permission required and available in df_model
        """
        if hasattr(view, 'df_fields'):
            fields = view.df_fields
        elif hasattr(view, 'get_serializer'):
            serializer = view.get_serializer()
            serializer_fields = list(serializer.fields.keys())

            model_fields = self.get_model_fields(view)

            # get fields only available in model
            fields = [field for field in serializer_fields if field in model_fields]
        else:
            raise AttributeError('df_fields is required')

        return fields

    @staticmethod
    def get_method(view):
        """
        Get and check method is valid
        """
        if not hasattr(view, 'df_method'):
            raise AttributeError('df_method is required')

        method = str(view.df_method).lower()

        if method not in [DFMethods.CREATE, DFMethods.UPDATE, DFMethods.RETRIEVE, DFMethods.LIST, DFMethods.DESTROY]:
            raise ValueError('df_method must be valid value')

        return view.df_method

    @staticmethod
    def get_model(view):
        """
        Get and check model is valid
        """
        if not hasattr(view, 'df_model'):
            raise AttributeError('df_model is required')

        model = view.df_model

        if not issubclass(model, models.Model):
            raise ValueError('df_model is not model class')

        return model

    def get_model_name(self, view):
        """
        Get model name
        """
        model = self.get_model(view)

        return str(model._meta.model_name).lower()

    def get_required_perms(self, view, fields):
        """
        Required permissions for view
        """
        df_method = self.get_method(view)
        df_model = self.get_model_name(view)

        required_perms = [f'{df_method}--{df_model}--{field}' for field in fields]
        return required_perms

    @staticmethod
    def get_user_perms(request):
        """
        Request user permissions
        """
        user = request.user

        user_perms = list(
            Permission.objects.filter(Q(user=user) | Q(group__user=user)).values_list('codename', flat=True))

        return user_perms

    def has_permission(self, request, view):
        user = request.user

        if not (user and user.is_authenticated):
            return False

        if user.is_superuser:
            return True

        # all permission of request user
        user_perms = self.get_user_perms(request)

        # check df_permissions exists
        if hasattr(view, 'df_permissions'):
            return set(view.df_permissions).issubset(user_perms)
        elif hasattr(view, 'get_df_permissions'):
            return set(view.get_df_permissions()).issubset(user_perms)

        fields = self.get_fields(view)

        # required permissions for view
        required_perms = self.get_required_perms(view, fields)

        return set(required_perms).issubset(user_perms)

    def has_object_permission(self, request, view, obj):
        df_user = getattr(view, 'df_user', 'user')
        user = getattr(obj, df_user, None)

        if user is None:
            raise AttributeError(f'{obj} has no attribute {df_user}')

        return request.user == user
