"""
Name: Patrick Godinez

Description: this file provides a top level menu, implements the network tools submeu
uses helpers in menu_utils.Py for menu display, also uses scanner classes

"""
from ps_socket import PSSocketClass, PSSocketConcurrentClass
from ps_nmap import PSNmapClass, PSNmapConcurrentClass
from menu_utils import get_menu_choice, print_table, save_csv #testing this function may rework


def network_tools_menu():
    """
    provides the network tools submenu and the options for different scans
    """
    while True:
        options = [
            "Socket Scan (Single-Thread)",
            "Socket Scan (Concurrent)",
            "Nmap Scan (Single)",
            "Nmap Scan (Concurrent)",
            "Return to Main Menu"
        ]

        #display menu and get user's selection
        choice = get_menu_choice(options)

        if choice == "Socket Scan (Single-Thread)":
            #single thread TCP socket scan
            print("\n[Socket Scan - Single Thread]\n")
            host = input("Enter target host (e.g. localhost or 127.0.0.1): ").strip() or "localhost"
            ports = input("Enter comma-separated ports: ").strip()

            port_list = [p.strip() for p in ports.split(",") if p.strip()]

            #initializes scanner and runs the scan
            scanner = PSSocketClass(timeout=1.0)
            results = scanner.scan(host, port_list)

            #display results
            print_table(results)

        elif choice == "Socket Scan (Concurrent)":
            #this uses ThreadPoolExecutor to do concurrent socket scans
            print("\n[Socket Scan - Concurrent]\n")
            host = input("Enter target host (e.g. localhost or 127.0.0.1): ").strip() or "localhost"
            ports = input("Enter comma-separated ports: ").strip()

            port_list = [p.strip() for p in ports.split(",") if p.strip()]

            # more max_workers increases scanning speed
            scanner = PSSocketConcurrentClass(timeout=1.0, max_workers=40)
            results = scanner.scan(host, port_list)
            print_table(results)
           
        elif choice == "Nmap Scan (Single)":
            #print("\n[Placeholder]")
            #single host nmap scan
            print("\n[Nmap Scan - Single]\n")
            host = input("Enter target host (e.g. localhost or 127.0.0.1): ").strip() or "localhost"
            ports = input("Enter ports (e.g. 22,80,443): ").strip()

            # provides validated list of ports
            port_list = []
            for p in ports.split(","):
                p = p.strip()
                if not p:
                    continue
                if p.isdigit():
                    port_list.append(p)
                else:
                    try:
                        port_list.append(str(int(p)))
                    except Exception:
                        #ignores bad entries
                        pass
            
            #if no ports provided should use common ports list
            if not port_list:
                port_list = ["22", "80", "443"]

            #run the Nmap Scanner
            scanner = PSNmapClass(nmap_args="-sV -Pn")
            results = scanner.scan(host, port_list)

            #display results
            print_table(results)
        
        elif choice == "Nmap Scan (Concurrent)":
            #concurrent nmap scans across multiple hosts and ports
            print("\n[Nmap Scan - Concurrent]\n")

            use_files = input("Read IPNums.txt & PortNums.txt? (y/n) [y]: ").strip().lower() or "y"

            if use_files == "y":
                # read hosts and ports from files in current directory
                try:
                    with open("IPNums.txt", "r") as f:
                        hosts = [line.strip() for line in f if line.strip()]
                    with open("PortNums.txt", "r") as f:
                        ports = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    # if read rails, print error and return to menu loop
                    print(f"Error reading files: {e}")
                    continue
            else:
                #this is for manual entry, may rework
                host_input = input("Enter Hosts: ").strip()
                hosts = [h.strip() for h in host_input.split(",") if h.strip()]
                port_input = input("Enter Ports: ").strip()
                ports = [p.strip() for p in port_input.split(",") if p.strip()]
            
            #default is 10 but user can input concurrency
            workers = input("Max workers (threads) [default 10]: ").strip()
            try:
                workers = int(workers) if workers else 10
            except ValueError:
                workers = 10
            
            # initialize concurrent Nmap scanner and run
            scanner = PSNmapConcurrentClass(nmap_args="-sV -Pn", max_workers=workers)
            results = scanner.scan(hosts, ports)
            
            #display results
            print_table(results)
        
        else:
            #return to main menu
            break

def main_menu():
    """
    Displays the top level menu CyberSecurity ToolKit.
    """
    while True:
        menu_items = [
            "Network Tools",
            "Forensics Tools",
            "Password Cracking Tools",
            "Quit Program"
        ]

        user_choice = get_menu_choice(menu_items)

        if user_choice == "Network Tools":
            #this takes you to network tools submenu
            network_tools_menu()
        
        elif user_choice == "Forensics Tools":
            #placeholder
            print("\n[Placeholder] Tools submenu pending")
        
        elif user_choice == "Password Cracking Tools":
            #placeholder
            print("\n[Placeholder] Tools submenu pending")
        
        elif user_choice == "Quit Program":
            #graceful exit
            print("\nExiting.... Goodbye!\n")
            break


def main():
    main_menu()

if __name__ == "__main__":
    main()



#print("Setup verified successfully")
