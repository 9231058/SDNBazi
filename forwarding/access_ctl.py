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

        # We want hosts
        if str(packet.src) in hosts and str(packet.dst) in hosts:
            if str(packet.src) == "00:00:00:00:00:01" and str(packet.dst) not in allowed_hosts:
                log.info("The winner is %s" % packet.dst)
                allowed_hosts.append(str(packet.dst))
            if str(packet.src) != "00:00:00:00:00:01" and (str(packet.src) not in allowed_hosts\
                    or str(packet) not in allowed_hosts):
                log.info("Let catch this packet %s -> %s" % (packet.src, packet.dst))

                # Adds drop rule - Rule without action is a drop rule
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 14
                msg.hard_timeout = 94
                self.connection.send(msg)



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
