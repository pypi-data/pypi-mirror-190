#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
import enum
import json
from typing import Dict, Optional

import requests

from .connection import KaranageConnectionInterface
from .exception import KaranageException


class StateSystem(enum.Enum):
    OK = "OK"
    FAIL = "FAIL"
    DOWN = "DOWN"


## Generic karanage sending system.
class KaranageState:
    def __init__(self, connection: KaranageConnectionInterface) -> None:
        """Initialize the communication class.
        :param connection: Connection interface.
        """
        self.connection = connection

    def send(
        self,
        topic: str,
        data: Optional[Dict] = None,
        state: StateSystem = StateSystem.OK,
    ) -> None:
        """Send a message to the server.
        :param topic: Topic where to publish the data.
        :param data: Data to send to the server
        :param state: State of the current system
        """
        if data is None:
            data = {}
        param = {}
        if state is not None:
            param["state"] = state.value
        ret = self.connection.post("state", topic, data=data, params=param)
        if not 200 <= ret.status <= 299:
            raise KaranageException(
                f"Fail send message: '{ret.url}'", ret.status, ret.data
            )

    def gets(self, topic: Optional[str] = None, since: Optional[str] = None) -> Dict:
        """Get all the topic fom the server.
        :param since: ISO1866 time value.
        :return: A dictionary with the requested data.
        """
        param = {}
        if since is not None:
            param["since"] = since
        ret = self.connection.get("state", topic, params=param)
        if 200 <= ret.status <= 299:
            return json.loads(ret.data)
        raise KaranageException(f"Fail get data: '{ret.url}'", ret.status, ret.data)

    def get_history(
        self,
        topic: Optional[str] = None,
        since: Optional[str] = None,
        since_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict:
        """Get all the topic fom the server.
        :param since: ISO1866 time value.
        :param since_id: remote BDD index of the field.
        :param limit: the number of value we want to get
        :return: A dictionary with the requested data.
        """
        param = {}
        if since is not None:
            param["since"] = since
        if since_id is not None:
            param["sinceId"] = since_id
        if limit is not None:
            param["limit"] = limit
        ret = self.connection.get("state_history", topic, params=param)
        if 200 <= ret.status <= 299:
            return json.loads(ret.data)
        raise KaranageException(f"Fail get data: '{ret.url}'", ret.status, ret.data)
