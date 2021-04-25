class AppCoreRouter:
    """Control database routing for app_core"""

    route_app_labels = {'auth', 'app_core'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'app_core'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'app_core'
        return None

    def allow_relation(self, obj1, obj2):
        if obj1._state.db in self.route_app_labels and obj2._state.db in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'app_core'
        return None
