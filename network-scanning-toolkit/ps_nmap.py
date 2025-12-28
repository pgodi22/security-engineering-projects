"""
Author: Patrick Godinez
File Name: ps_nmap.py
Assignment 2

    Description:
        - PSNmap Class - uses the python-nmap library to run traditional NMAP Scans
        - PSNmapConcurrent Class - executes mutliple NMAP scans conccurrently.
"""
from menu_utils import make_record
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    import nmap
    HAVE_PY_NMAP = True
except Exception:
    HAVE_PY_NMAP = False
    
class PSNmapClass:
    """
    this class contains the functions that to perform single-host, single thread scans
    run an namp -sV styel scan for single host and list of ports
    """
    def __init__(self, nmap_args: str = "-sV -Pn"):
        self.nmap_args = nmap_args

    def scan(self, host: str, ports: list):
        """
        Perform the scan of one host over a list of ports

        host: hostname or IP Address
        ports: list of ports
        """
        # sanitize ports to a string
        port_list = []
        for p in ports:
            try:
                port_list.append(str(int(p)))
            except Exception:
                continue
        port_str = ",".join(port_list) if port_list else ""

        results = []

        #if python-nmap is not available, return error records
        if not HAVE_PY_NMAP:
            #return error records for each port
            for p in port_list:
                results.append(make_record(host, int(p), "tcp", "error", reason="Nmap not installed"))
            return results

        try:
            # initialize the nmap port scanner object
            scanner = nmap.PortScanner()
            scan_ret = scanner.scan(hosts=host, ports=port_str, arguments=self.nmap_args)

            #parsing the Nmap results
            host_info = scan_ret.get("scan", {}).get(host, {})
            tcp_info = host_info.get("tcp", {}) if isinstance(host_info.get("tcp", {}), dict) else {}

            #iterate through each port scanned
            for p in port_list:
                pi = int(p)
                # nmap keys may either be an int or a string, try for both
                info = tcp_info.get(pi) or tcp_info.get(str(pi)) or {}

                # extract the common data from Nmap response
                state = info.get("state", "filtered")
                name = info.get("name", "N/A")
                product = info.get("product", "N/A")
                version = info.get("version", "N/A")
                cpe_field = info.get("cpe", "N/A")
                
                # format cpe to a short string
                if isinstance(cpe_field, list):
                    cpe = ";".join(cpe_field) if cpe_field else "N/A"
                else:
                    cpe = cpe_field or "N/A"
                reason = info.get("reason", "N/A")

                # create a standard record for this port
                results.append(make_record(host, pi, "tcp", state, name=name, reason=reason, product=product, version=version, cpe=cpe))

            return results
        
        except Exception as e:
            #handles errors
            for p in port_list:
                results.append(make_record(host, int(p), "tcp", "error", reason=str(e)))
            return results

class PSNmapConcurrentClass:
    """
    This class handles multiple Nmap scans concurrently
    """
    def __init__(self, nmap_args: str = "-sV -Pn", max_workers: int = 10):
        self.nmap_args = nmap_args
        self.max_workers = max_workers

    def scan(self, hosts: list, ports: list):
        """
        hosts: list of hosts
        ports: list of ports
        returns a combined list
        """

        results = []
        #format list of host and ports
        host_list = [h.strip() for h in hosts if str(h).strip()]
        port_list = [str(int(p)) for p in ports if str(p).strip()] # will raise bad entries

        if not HAVE_PY_NMAP:
           #return error records for each port
           for p in port_list:
               results.append(make_record(host, int(p), "tcp", "error", reason="Nmap not installed"))
           return results
    
        def _host_scan(h):
            try:
                scanner = PSNmapClass(nmap_args=self.nmap_args)
                return scanner.scan(h, port_list)
            except Exception as e:
                return [make_record(h, int(p), "tcp", "error", reason=str(e)) for p in port_list]
    
        #launch the concurrent scans
        with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            future_to_host = {exe.submit(_host_scan, h): h for h in host_list}
            
            # process results
            for fut in as_completed(future_to_host):
                try:
                    host_results = fut.result()
                    if isinstance(host_results, list):
                        results.extend(host_results)
                except Exception as e:
                    h = future_to_host.get(fut, "unkown")
                    for p in port_list:
                        results.append(make_record(h, int(p), "tcp", "error", reason=str(e)))
    
        return results