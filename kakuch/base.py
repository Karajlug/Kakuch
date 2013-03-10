#! /usr/bin/env python
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
import logging

from kakuch.factories import SSLContextFactory


class KObject(object):
    """
    Kakuch objects base class.
    """

    logger = logging.getLogger("Kakuch")


class BaseDispatcher(KObject):
    """
    This class have the baic and common information for all the dispatcher
    classes.

    .. config:: A dictionary object that contains global configurations. Normally
                **Kakuch** use a json configuration file to generate this dictionary

    .. target_host:: IP address or Domain name of the target service.
    .. target_port:: Port number of target service that data should send to.
    .. my_host:: IP address or Domain name of the dispatcher (this class) to bind.
    .. my_port:: Port number to bind.

    """
    def __init__(self, config={}, target_host="127.0.0.1",
                 target_port="7777", my_host="127.0.0.1",
                 my_port="8888", sslkey=None, sslcert=None,
                 cacert=None):

        self.config = config

        self.target_host = self.config.get("target_host", target_host)
        self.target_port = self.config.get("target_port", target_port)

        self.my_host = self.config.get("my_host", my_host)
        self.my_port = self.config.get("my_port", my_port)


class SSLDispatcher(BaseDispatcher):
    """
    This dispatcher class use SSL mutual authentication (2way SSL authentication).
    To provide a secure and authenticated tunnel. In mutual authentication server
    and client authenticate against each other.

    .. sslkey:: SSL private key to use. Private key should belongs to the current
                node.
    .. sslcert:: SSL certificate to use. Certificate file should belongs to current
                 node and be signed by CA private key.
    .. cacert:: The certificate file of CA.
    """
    def __init__(self, sslkey=None, sslcert=None, cacert=None,
                 **kwargs):

        super(SSLDispatcher, self).__init__(**kwargs)
        self.key = self.config.get("sslkey", sslkey)
        self.cert = self.config.get("sslcert", sslcert)
        self.cacert = self.config.get("cacert", cacert)


        should_exit = False

        if not self.key:
            self.logger.critical("Running on 'ssl' mode without SSL private key?")
            should_exit = True

        if not self.cert:
            self.logger.critical("Running on 'ssl' mode without SSL certificate?")
            should_exit = True

        if not self.cacert:
            self.logger.critical("Running on 'ssl' mode using mutual authentication without CA certificate?")
            should_exit = True

        if should_exit:
            exit(1)

        self.logger.info("SSL KEY: %s" % self.key)
        self.logger.info("SSL CERT: %s" % self.cert)
        self.logger.info("CA CERT: %s" % self.cacert)

        self.context_factory = SSLContextFactory(self.key,
                                                 self.cert)
        self.context_factory.cacert = self.cacert
