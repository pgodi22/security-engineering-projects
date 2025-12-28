"""
Author: Patrick Godinez
File name: ps_socket.py
Assignment 2

    Description:
        Here we are defining the two socket-based scanner classes
         - PSSocket Class - this one executes single-thread TCP port scans
         - PSSocketConcurrent Class - performs multi-threaded TCP port scans
"""
import socket
from menu_utils import make_record # will add make_record to menu_utils
from concurrent.futures import ThreadPoolExecutor, as_completed


class PSSocketClass:
    """
    This class contains the functions to perform single-threaded TCP socket port scans
    """
    def __init__(self, timeout: float = 1.0):
        # timeout for each socket connection attempt
        self.timeout = timeout
    
    def scan_port(self, host: str, port: int):
        """
        attempt tcp connet to host:port and return a record dictionary
        """
        try:
            # this creates a TCP socket and attempt connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                res = s.connect_ex((host, int(port)))
                if res == 0:
                    # successful conneciton means port is open
                    return make_record(host, int(port), "tcp", "open", name="tcp", reason="connect")
                else:
                    # this means result is closed or unreachable
                    return make_record(host, int(port), "tcp", "closed", name="tcp", reason=f"code_{res}")
        except Exception as e:
            return make_record(host, port, "tcp", "error", reason=str(e))

    def scan(self, host: str, ports: list):
        """
        Scan a single host for a list of ports
        """ 
        results = []
        for p in ports:
            # skip invalid entries
            try:
                p_int = int(p)
            except Exception:
                continue

            rec = self.scan_port(host, p_int)
            results.append(rec)
        
        return results

class PSSocketConcurrentClass:
    """
    This class contains the functions to perform concurrent socket scans
    """
    def __init__(self, timeout: float = 1.0, max_workers: int = 20):
        self.timeout = timeout
        self.max_workers = max_workers

    def _worker(self, host, port):
        """
        this is a worker funciton for a single port scan executed in parallel by ThreadpoolExecutor
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                res = s.connect_ex((host, int(port)))
                if res == 0:
                    return make_record(host, int(port), "tcp", "open", name="tcp", reason="connect")
                else:
                    return make_record(host, int(port), "tcp", "closed", name="tcp", reason=f"code_{res}")
        except Exception as e:
            return make_record(host, port, "tcp", "error", reason=str(e))
    
    def scan(self, host: str, ports: list):
        """
        scan one host concurrently over `ports`. Returns list of record dictionaries.
        """
        #sanitize ports into ints
        port_list = []
        for p in ports:
            try:
                port_list.append(int(p))
            except Exception:
                continue

        results = []
        #Multiple concurrent socket scans managed by ThreadPoolExecutor    
        with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            #submit one per port
            future_to_port = {exe.submit(self._worker, host, p): p for p in port_list}
            # collect results as they complete
            for fut in as_completed(future_to_port):
                results.append(fut.result())

        return results


           