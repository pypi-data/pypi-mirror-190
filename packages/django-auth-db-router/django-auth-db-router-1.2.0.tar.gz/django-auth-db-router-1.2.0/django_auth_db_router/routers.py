from django.conf import settings


class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'auth', 'contenttypes', 'admin', }

    # add auditlog app label to route_app_labels. Why? Because auditlog needs auth and contenttypes models to work
    route_app_labels.add('auditlog')

    try:
        token_table = settings.REST_AUTH_TOKEN_TABLE
    except NameError:
        token_table = 'AUTHENTICATION_TOKEN'

    route_db_tables = {token_table, 'django_session'}

    try:
        auth_db = settings.AUTH_DB
    except NameError:
        auth_db = 'default'

    def db_for_read(self, model, **hints):
        if hasattr(model, 'Database') and getattr(model.Database, 'db'):
            return getattr(model.Database, 'db')
        if model._meta.db_table in self.route_db_tables:
            return self.auth_db
        if model._meta.app_label in self.route_app_labels:
            return self.auth_db
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model, 'Database') and getattr(model.Database, 'db'):
            return getattr(model.Database, 'db')
        if model._meta.db_table in self.route_db_tables:
            return self.auth_db
        if model._meta.app_label in self.route_app_labels:
            return self.auth_db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels or
                obj1._meta.db_table in self.route_db_tables or
                obj2._meta.db_table in self.route_db_tables
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == self.auth_db
        return None
