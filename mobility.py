#!/usr/bin/python

'This example creates a simple network topology with 1 AP and 4 stations'

import sys

from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.associationControl import associationControl

def topology():
    "Create a network."
    net = Mininet_wifi(controller=None)
    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',
                          position='30,30,0'
                          )
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',
                          position='80,30,0'
                          )
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1',
                             position='20,30,0', range=20)


    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='5',
                             position='60,30,0', range=20)


    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1',
                           port=6633)
    net.setPropagationModel(model="logDistance", exp=5)


    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    # addlink has to come after configure wifinodes
    net.addLink(ap1, ap2)

    net.plotGraph(max_x=100, max_y=100)
    net.setAssociationCtrl('ssf')
    info("*** Starting network\n")
    
    
    net.startMobility(time=0, repetitions=1)
    net.mobility(sta1, 'start', time=1, position='30.0,30.0,0.0')
    net.mobility(sta2, 'start', time=1, position='80.0,30.0,0.0')
    net.mobility(sta1, 'stop', time=50, position='70.0,30.0,0.0')
    net.mobility(sta2, 'stop', time=50, position='30.0,30.0,0.0')

    net.stopMobility(time=50)


    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])


    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
