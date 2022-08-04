""" indexer.py

Indexes packets in Elasticsearch or dumps them to a file

Copyright (c) 2019 Vic Hargrave

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
"""

from datetime import datetime
import socket
import json


def index_packets(capture):
    """ Index packets generator method.

    :param capture: Series of packets captured by the Tshark object.
    :return: Action JSON object yielded to the Elasticsearch client bulk indexing helper function.
    """
    for packet in capture:
        timestamp = int(packet['timestamp'])/1000
        action = {
            '_op_type': 'index',
            '_index': 'packets-' + datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
            '_source': packet
        }
        yield action


def dump_packets(capture):
    """ Dump packets generator method that prints packets to stdout.

    :param capture: Series of packets captured by the Tshark object.
    :param create_date_utc: Date the PCAP file or live capture was created
    """

    try:
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
    server_address = ("127.0.0.1", 5051)
    tcpsock.connect(server_address)

    for packet in capture:
        msg = json.dumps(packet) + "\n"
        tcpsock.send(msg.encode())

    tcpsock.close()