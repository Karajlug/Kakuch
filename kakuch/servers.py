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

from twisted.internet import reactor

from kakuch.base import KObject
from kakuch.factories import SSLContextFactory
from kakuch.protocols import ReceiverFactory, DispatchClientFactory


class DispatchServer(KObject):
    """
    Dispatch Server class. This class is responsible for dispatching incoming
    traffic to the target host (combination of IP and port ofcourse).
    """
    def __init__(self, config={}, target_host="127.0.0.1",
                 target_port="7777", my_host="127.0.0.1",
                 my_port="8888", sslkey=None, sslcert=None,
                 cacert=None, mode="ssl"):

        self.config = config

        self.target_host = self.config.get("target_host", target_host)
        self.target_port = self.config.get("target_port", target_port)

        self.my_host = self.config.get("my_host", my_host)
        self.my_port = self.config.get("my_port", my_port)

        self.key = self.config.get("sslkey", sslkey)
        self.cert = self.config.get("sslcert", sslcert)
        self.cacert = self.config.get("cacert", cacert)

        self.mode = config.get("mode", mode)

        self.logger.info("SSL KEY: %s" % self.key)
        self.logger.info("SSL CERT: %s" % self.cert)
        self.logger.info("CA CERT: %s" % self.cacert)

        self.target = DispatchClientFactory()
        self.receiver = ReceiverFactory()

        self.receiver.set_target(self.target)
        self.target.set_receiver(self.receiver)

        context_factory = SSLContextFactory(self.key,
                                            self.cert)
        context_factory.cacert = self.cacert

        reactor.listenSSL(int(self.my_port),
                          self.receiver,
                          context_factory)

        reactor.connectTCP(self.target_host,
                            int(self.target_port),
                            self.target)

    def run(self):

        self.logger.info("Running using %s mode..." % self.mode)
        self.logger.info("Listening to %s:%s ..." % (self.my_host,
                                                     self.my_port))
        self.logger.info("Dispatching to %s:%s ..." % (self.target_host,
                                                     self.target_port))

        reactor.run()
