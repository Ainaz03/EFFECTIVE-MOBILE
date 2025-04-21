class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


class Server:
    _ip_counter = 1

    def __init__(self):
        self.ip = Server._ip_counter
        Server._ip_counter += 1
        self.buffer = []
        self.router = None

    def send_data(self, data):
        if self.router:
            self.router.buffer.append(data)

    def get_data(self):
        received = self.buffer[:]
        self.buffer.clear()
        return received

    def get_ip(self):
        return self.ip


class Router:
    def __init__(self):
        self.servers = {}  # ip: server
        self.buffer = []

    def link(self, server):
        self.servers[server.get_ip()] = server
        server.router = self

    def unlink(self, server):
        ip = server.get_ip()
        if ip in self.servers:
            del self.servers[ip]
            server.router = None

    def send_data(self):
        for data in self.buffer:
            target_server = self.servers.get(data.ip)
            if target_server:
                target_server.buffer.append(data)
        self.buffer.clear()

router = Router()

sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)

sv_to = Server()
router.link(sv_to)

sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
router.send_data()

msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()