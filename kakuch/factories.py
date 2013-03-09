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
from OpenSSL import SSL

from twisted.internet import reactor, ssl

from base import KObject


class SSLFactory(ssl.DefaultOpenSSLContextFactory, KObject):
    """
    SSL factory class for twisted
    """
    cacert = None

    def getContext(self):

        x = self._context

        # Setting SSL verification flags
        x.set_verify(
            SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
            self.verify_cert,
        )

        # Since we have self-signed certs we have to explicitly
        # tell the server to trust them.
        x.load_verify_locations(self.cacert)
        return x

    def verify_cert(self, connection, x509, errnum, errdepth, ok):
        """
        Verify remote certificate
        """
        if not ok:
            self.logger.error(
                'invalid cert from subject: %s' % x509.get_subject())
            return False
        else:
            self.logger.info("Cert is fine.")
            return True
