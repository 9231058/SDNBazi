from pox.core import core
from pox.lib.util import str_to_bool
import pox.openflow.libopenflow_01 as of
import re

log = core.getLogger()
validator = "00:00:00:00:00:01"
allowed_hosts = ["00:00:00:00:00:01"]

class AccessControl(object):
    def __init__(self, connection, transparent):
        # We want to hear PacketIn messages, so we listen
        # to the connection
        connection.addListeners(self)
        self.connection = connection
        self.transparent = transparent

    def _handle_PacketIn(self, event):
        packet = event.parsed
        src = str(packet.src)
        des = str(packet.dst)
        # We want hosts
        if (re.match("00:00:00:00:00:*",src)):
            if re.match(validator,src) and dst not in allowed_hosts:
                log.info("The winner is %s" % dst)
                allowed_hosts.append(dst)
            else:
                   if(src not in allowed_hosts or dst not in allowed_hosts):
                       log.info("Let catch this packet %s -> %s" % (packet.src, packet.dst))
                       # Adds drop rule - Rule without action is a drop rule
                       msg = of.ofp_flow_mod()
                       msg.match = of.ofp_match.from_packet(packet, event.port)
                       msg.idle_timeout = 14
                       msg.hard_timeout = 94
                       msg.priority = 1000
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
