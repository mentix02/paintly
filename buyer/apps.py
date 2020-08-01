from django.apps import AppConfig


class BuyerConfig(AppConfig):
    name = 'buyer'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import buyer.signals
