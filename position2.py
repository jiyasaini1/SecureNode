#!/usr/bin/python

import sys

from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi(controller=None)
    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',
                          position='35,40,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',
                          position='65,90,0')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8',
                          position='45,55,0')



    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1',
                             position='55,30,0', range=30)

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1',
                           port=6633)
    net.setPropagationModel(model="logDistance", exp=5)
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)
    net.setAssociationCtrl('ssf')
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
