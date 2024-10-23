from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import signal

authorizer = DummyAuthorizer()
authorizer.add_user("fabs", "773H", r"C:\Users\PC\Desktop\ftp", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

address = ("172.31.35.188", 21)
server = FTPServer(address, handler)

def signal_handler(signal, frame):
    print("Servidor detenido.")
    server.close_all()

# Asociar la señal SIGINT (Ctrl+C) con la función de manejo de señal
signal.signal(signal.SIGINT, signal_handler)

print("Servidor FTP iniciado. Presiona Ctrl+C para detenerlo.")
server.serve_forever()