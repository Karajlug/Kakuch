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

from kakuch.ssl import SSLDispatcher
from kakuch.protocols import ProxyFactory


class DispatchClient(SSLDispatcher):
    """
    Dispatch client class. This class is responsible for dispatching client
    traffic to the dispatcher server and deliver back to client
    """
    def __init__(self, **kwargs):
        super(DispatchClient, self).__init__(**kwargs)

        # TODO: Add a timeout support for connect method
        connection = [reactor.connectSSL, {
            "contextFactory": self.context_factory
            }]
        factory = ProxyFactory(target_host=self.target_host,
                               target_port=self.target_port,
                               connection_details=connection)

        reactor.listenTCP(int(self.my_port),
                          factory,
                          interface=self.my_host)

    def run(self):

        self.logger.info("Running using SSL mode...")
        self.logger.info("Listening to %s:%s ..." % (self.my_host,
                                                     self.my_port))
        self.logger.info("Dispatching to %s:%s ..." % (self.target_host,
                                                       self.target_port))

        reactor.run()
