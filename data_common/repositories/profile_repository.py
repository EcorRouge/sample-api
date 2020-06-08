import abc


class ProfileRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_or_create_profile(self):
        pass

    @abc.abstractmethod
    def update_profile(self, obj):
        pass

    @abc.abstractmethod
    def update_user_app_metadata(self, obj):
        pass

    @abc.abstractmethod
    def delete_profile(self):
        pass