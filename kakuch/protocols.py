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

from kakuch.base import KObject


class ReceiverProtocol(protocol.Protocol, KObject):
    """
    Receiver protocol just dispatch the received data after client verification
    to the target host

    ..target:: The DispatchFactory instance that will be connect to the target host
    """
    def __init__(self, target):
        self.target = target

    def dataReceived(self, data):
        self.logger.debug("Send data to %s" % self.target)
        self.target.send(data)


class ReceiverFactory(protocol.Factory, KObject):
    """
    This receiver factory use ReceiverProtocl to get data from Kakuch client
    and dispatch them to the target host

    """
    protocol = ReceiverProtocol

    def set_target(self, target):
        """
        ..target:: The DispatchFactory instance that will be connect to the target host
        """
        self.target = target

    def buildProtocol(self, addr):
        p = self.protocol(self.target)
        return p


class DispatchProtocol(protocol.Protocol, KObject):
    """
    Dispatch protocol just dispatch the recieved data from the receiver factory
    and pass them to target host

    .. dispatcher:: An instance of Receiver factory
    """

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def dataReceived(self, data):
        self.logger.debug("Send data to %s" % self.dispatcher)
        self.dispatcher.send(data)


class DispatchFactory(protocol.Factory, KObject):
    """
    This class placed between target host and Dispatcher code and deliver the
    client data to the target.
    """
    protocol = DispatchProtocol

    def set_dispatcher(self, dispatcher):
        """
        Set the ReceiverFactory instance of this class

        .. dispatcher:: An instance of Receiver factory
        """
        self.dispatcher = dispatcher

    def buildProtocol(self, addr):
        p = self.protocol(self.dispatcher)
        return p
