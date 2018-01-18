from pox.core import core
from pox.lib.util import str_to_bool

log = core.getLogger()

hosts = [
        "00:00:00:00:00:01",
        "00:00:00:00:00:02",
        "00:00:00:00:00:03",
        "00:00:00:00:00:04",
        "00:00:00:00:00:05",
        "00:00:00:00:00:07",
        "00:00:00:00:00:08"
        ]

allowed_hosts = []

class AccessControl(object):
    def __init__(self, connection, transparent):
        # We want to hear PacketIn messages, so we listen
        # to the connection
        connection.addListeners(self)
        self.transparent = transparent

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if str(packet.src) == "00:00:00:00:00:01" and str(packet.dst) in hosts:
            log.info("Packet form the source is here")
            log.info("The winner is %s" % packet.dst)
            allowed_hosts.append(packet.dst)


class access_ctl(object):
    """
    Waits for OpenFlow switches to connect and makes them Fekri's switches.
    """
    def __init__ (self, transparent):
        core.openflow.addListeners(self)
        self.transparent = transparent

    def _handle_ConnectionUp (self, event):
        log.debug("Connection %s" % (event.connection,))
        AccessControl(event.connection, self.transparent)


def launch(transparent=False):
    log.info("Hello form Fekri")

    core.registerNew(access_ctl, str_to_bool(transparent))
