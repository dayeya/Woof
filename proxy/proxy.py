from socket import *
from threading import Thread
from typing import List, Dict, Tuple, Any, Union

from util_modules.network_client import Client
from util_modules.network import create_thread, send, recv
from util_modules.network import all_interfaces, listen_bound

Address = Tuple[str, int]

class Proxy:
    def __init__(self, addr: Address=(all_interfaces, 60000)) -> None:
        """
        Creates a proxy at addr.

        Args:
            addr (tuple[str, int], optional): Location. Defaults to ('localhost', 60000).
        """
        self.__ip, self.__port = addr
        self.__main_sock = socket(AF_INET, SOCK_STREAM)
        
        # Bind and start listening.
        self.__main_sock.bind(addr)
        self.__main_sock.listen(listen_bound)
        
        # Start proxy.
        self.__boot_proxy()
        
    def __accept_client(self) -> Client:
        """
        Waits for a client, return a new Client.

        Returns:
            Client: Client object of the accepeted end-point.
        """
        return Client(self.__main_sock.accept())
    
    def __boot_proxy(self) -> None:
        while True:
            client = self.__accept_client()
            print(f'[+] Logged a new client! {client}')
            
            # Create thread and start it.
            thread: Thread = create_thread(self.__handle_client, args=client)
            thread.start()
            
    def start(self) -> None:
        self.__boot_proxy()
            
    def __handle_client(client: Client) -> None:
        while True:
            data = recv(client.sock)
            if not data: break
            send(f'ECHO: {data}')
            
        # End communication with client.
        client.close()
        
if __name__ == '__main__':
    waf = Proxy()
    waf.start()