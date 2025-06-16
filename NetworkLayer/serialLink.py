class SerialLink:
    def __init__(self, router1, iface1, router2, iface2):
        self.router1 = router1
        self.iface1 = iface1
        self.router2 = router2
        self.iface2 = iface2

    def transmit(self, sender, data, out_iface):
        if sender == self.router1:
            self.router2.receive(data, self.iface2)
        elif sender == self.router2:
            self.router1.receive(data, self.iface1)