from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url
from web import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url('webssh/',consumers.SshConsumer)
    ])
})