from django.core.management import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.db.models import Q

from df_permission.permissions import DFMethods
from df_permission.variables import prefix
from django.apps import apps


class Command(BaseCommand):
    perms = Permission.objects.filter(name__startswith=prefix)
    create_perms = perms.filter(codename__startswith=f'{DFMethods.CREATE}--')
    update_perms = perms.filter(codename__startswith=f'{DFMethods.UPDATE}--')
    list_perms = perms.filter(codename__startswith=f'{DFMethods.LIST}--')
    retrieve_perms = perms.filter(codename__startswith=f'{DFMethods.RETRIEVE}--')
    destroy_perms = perms.filter(codename__startswith=f'{DFMethods.DESTROY}--')

    def make_for_df_methods(self):
        group, _ = Group.objects.get_or_create(name=f'Method: {DFMethods.CREATE}')
        for create_perm in self.create_perms:
            group.permissions.add(create_perm)
        group.save()

        group, _ = Group.objects.get_or_create(name=f'Method: {DFMethods.UPDATE}')
        for update_perm in self.update_perms:
            group.permissions.add(update_perm)
        group.save()

        group, _ = Group.objects.get_or_create(name=f'Method: {DFMethods.LIST}')
        for list_perm in self.list_perms:
            group.permissions.add(list_perm)
        group.save()

        group, _ = Group.objects.get_or_create(name=f'Method: {DFMethods.RETRIEVE}')
        for retrieve_perm in self.retrieve_perms:
            group.permissions.add(retrieve_perm)
        group.save()

        group, _ = Group.objects.get_or_create(name=f'Method: {DFMethods.DESTROY}')
        for destroy_perm in self.destroy_perms:
            group.permissions.add(destroy_perm)
        group.save()

    def handle(self, *args, **options):
        self.make_for_df_methods()

        models = apps.get_models()
        for model in models:
            model_name = str(model._meta.model_name).lower()
            perms_by_model = self.perms.filter(
                Q(codename__contains=f'--{model_name}--') | Q(codename__endswith=f'--{model_name}'))
            group = Group.objects.create(name=f'Model: {model_name}')
            for perm in perms_by_model:
                group.permissions.add(perm)
            group.save()
