# -----------------------------------------------------------------------------
#    Kakuch - Traffic wrapper application
#    Copyright (C) 2013 Sameer Rahmani <lxsameer@gnu.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from twisted.internet import protocol
from twisted.internet import defer

from kakuch.base import KObject


class ProxyClientProtocol(protocol.Protocol, KObject):
    """
    """
    def connectionMade(self):
        self.logger.info("Client: connected to peer")
        self.cli_queue = self.factory.cli_queue
        self.cli_queue.get().addCallback(self.server_data_received)

    def server_data_received(self, chunk):
        if chunk is False:
            self.cli_queue = None
            self.logger.info("Client: disconnecting from peer")
            self.factory.continueTrying = False
            self.transport.loseConnection()

        elif self.cli_queue:
            self.logger.info("Client: writing %d bytes to peer" % len(chunk))
            self.logger.debug("Data: %s" % chunk)
            self.transport.write(chunk)
            self.cli_queue.get().addCallback(self.server_data_received)

        else:
            self.factory.cli_queue.put(chunk)

    def dataReceived(self, chunk):
        self.logger.info("Client: %d bytes received from peer" % len(chunk))
        self.factory.srv_queue.put(chunk)

    def connectionLost(self, why):
        if self.cli_queue:
            self.cli_queue = None
            self.logger.info("Client: peer disconnected unexpectedly")


class ProxyClientFactory(protocol.ReconnectingClientFactory, KObject):
    """
    """
    maxDelay = 10
    continueTrying = True
    protocol = ProxyClientProtocol

    def __init__(self, srv_queue, cli_queue):
        self.srv_queue = srv_queue
        self.cli_queue = cli_queue


class ProxyProtocol(protocol.Protocol, KObject):
    """
    """
    def __init__(self, connection_details, target_host,
                 target_port, **kwargs):
        super(ProxyProtocol, self).__init__(**kwargs)
        self.connect = connection_details
        self.target_host = target_host
        self.target_port = target_port

    def connectionMade(self):
        self.srv_queue = defer.DeferredQueue()
        self.cli_queue = defer.DeferredQueue()
        self.srv_queue.get().addCallback(self.client_data_received)

        factory = ProxyClientFactory(self.srv_queue, self.cli_queue)
        self.connect[0](self.target_host, int(self.target_port),
                     factory, **self.connect[1])

    def client_data_received(self, chunk):
        self.transport.write(chunk)
        self.logger.debug("Data: %s" % chunk)
        self.logger.info("Server: writing %d bytes to original client" % len(chunk))
        self.srv_queue.get().addCallback(self.client_data_received)

    def dataReceived(self, chunk):
        self.logger.info("Server: %d bytes received" % len(chunk))
        self.cli_queue.put(chunk)

    def connectionLost(self, why):
        self.cli_queue.put(False)


class ProxyFactory(protocol.Factory, KObject):
    """
    """
    protocol = ProxyProtocol

    def __init__(self, connection_details, target_host,
                 target_port, **kwargs):
        super(ProxyFactory, self).__init__(**kwargs)
        self.connect = connection_details
        self.target_host = target_host
        self.target_port = target_port
        self.logger.info("ProxyFactory initialized.")

    def buildProtocol(self, addr):
        p = self.protocol(target_host=self.target_host,
                          target_port=self.target_port,
                          connection_details=self.connect)
        self.logger.info("ProxyProtocol created")
        return p


class ProxyClientProtocol(protocol.Protocol, KObject):
    """
    """
    def connectionMade(self):
        self.logger.info("Client: connected to peer")
        self.cli_queue = self.factory.cli_queue
        self.cli_queue.get().addCallback(self.server_data_received)

    def server_data_received(self, chunk):
        if chunk is False:
            self.cli_queue = None
            self.logger.info("Client: disconnecting from peer")
            self.factory.continueTrying = False
            self.transport.loseConnection()

        elif self.cli_queue:
            self.logger.info("Client: writing %d bytes to peer" % len(chunk))
            self.logger.debug("Data: %s" % chunk)
            self.transport.write(chunk)
            self.cli_queue.get().addCallback(self.server_data_received)

        else:
            self.factory.cli_queue.put(chunk)

    def dataReceived(self, chunk):
        self.logger.info("Client: %d bytes received from peer" % len(chunk))
        self.factory.srv_queue.put(chunk)

    def connectionLost(self, why):
        if self.cli_queue:
            self.cli_queue = None
            self.logger.info("Client: peer disconnected unexpectedly")


class ProxyClientFactory(protocol.ReconnectingClientFactory, KObject):
    """
    """
    maxDelay = 10
    continueTrying = True
    protocol = ProxyClientProtocol

    def __init__(self, srv_queue, cli_queue):
        self.srv_queue = srv_queue
        self.cli_queue = cli_queue


class ClientListenerProtocol(protocol.Protocol, KObject):
    """
    """
    def __init__(self, connection_details, target_host,
                 target_port, **kwargs):
        super(ProxyProtocol, self).__init__(**kwargs)
        self.connect = connection_details
        self.target_host = target_host
        self.target_port = target_port

    def connectionMade(self):
        self.srv_queue = defer.DeferredQueue()
        self.cli_queue = defer.DeferredQueue()
        self.srv_queue.get().addCallback(self.client_data_received)

        factory = ProxyClientFactory(self.srv_queue, self.cli_queue)
        self.connect[0](self.target_host, int(self.target_port),
                     factory, **self.connect[1])

    def client_data_received(self, chunk):
        self.transport.write(chunk)
        self.logger.debug("Data: %s" % chunk)
        self.logger.info("Server: writing %d bytes to original client" % len(chunk))
        self.srv_queue.get().addCallback(self.client_data_received)

    def dataReceived(self, chunk):
        self.logger.info("Server: %d bytes received" % len(chunk))
        self.cli_queue.put(chunk)

    def connectionLost(self, why):
        self.cli_queue.put(False)


class ClientListenerFactory(protocol.Factory, KObject):
    """
    """
    protocol = ClientListenerProtocol

    def __init__(self, connection_details, target_host,
                 target_port, **kwargs):
        super(ClientListenerFactory, self).__init__(**kwargs)
        self.connect = connection_details
        self.target_host = target_host
        self.target_port = target_port
        self.logger.info("ClientListenerFactory initialized.")

    def buildProtocol(self, addr):
        p = self.protocol(target_host=self.target_host,
                          target_port=self.target_port,
                          connection_details=self.connect)
        self.logger.info("ProxyProtocol created")
        return p
