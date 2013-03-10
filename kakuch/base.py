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
                 my_port="8888"):

        self.config = config

        self.target_host = self.config.get("target_host", target_host)
        self.target_port = self.config.get("target_port", target_port)

        self.my_host = self.config.get("my_host", my_host)
        self.my_port = self.config.get("my_port", my_port)
