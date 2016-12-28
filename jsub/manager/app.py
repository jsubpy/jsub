from jsub.manager.error import AppNotSetupError

class AppManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def build(self, app_data, backend_property):
        if 'type' not in app_data:
            raise AppNotSetupError('Must setup an app in task profile')
        app = self.__ext_mgr.load_ext_common('app', app_data)
        return app.build(backend_property)
