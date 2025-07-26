class AuthRouter:
    """
    Router vers la base 'auth_db' pour toute l'authentification :
    - app 'authentification' (ton app personnalisée)
    - Django built-in apps nécessaires : 'auth', 'admin', 'sessions', 'authtoken', 'contenttypes'
    """
    route_app_labels = {
        'auth',
        'admin',
        'contenttypes',
        'sessions',
        'authtoken',
        'authentification'
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'auth_db'
        return db == 'default'
