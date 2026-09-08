import sqlite3

def parse_firewall_log(file_path="firewall.log"):
    parsed_logs=[]
    with open(file_path, "r") as file:
        for line in file:
            if "filterlog" in line:     
                syslog_header, csv_part = line.split("]: ",1)
                timestamp = " ".join(syslog_header.split()[:3])
                #.strip to remove the \n
                clean_list = csv_part.strip().split(",")
                #ipv4 for pfsense rulenumber
                if clean_list[0] == "4":
                    interface = clean_list[4]
                    action = clean_list[6]
                    src_ip = clean_list[18]
                    dest_ip = clean_list[19]
                    proto = clean_list[16]
                    if proto in ["tcp", "udp"]:
                        src_port = clean_list[20]
                        dest_port = clean_list[21]
                    else:
                        src_port = "N/A"
                        dest_port = "N/A"
                    
                #ipv6 for pfsense rule number
                elif clean_list[0] == "6":
                    interface = clean_list[4]
                    action = clean_list[6]
                    src_ip = clean_list[15]
                    dest_ip = clean_list[16]
                    proto = clean_list[12]
                    if proto in ["tcp", "udp"]:
                        src_port = clean_list[17]
                        dest_port = clean_list[18]
                    else:
                        src_port = "N/A"
                        dest_port = "N/A"
                else: 
                    continue
                
                log_entry = {   
                    "ip_version": f"IPv{clean_list[0]}",
                    "interface": interface,
                    "action": action,
                    "protocol": proto.upper(),
                    "src_ip": src_ip,
                    "dest_ip": dest_ip,
                    "src_port": src_port,
                    "dest_port": dest_port,
                    "timestamp": timestamp
                }
                
                parsed_logs.append(log_entry)

    return parsed_logs

def log_db(parsed_logs):
    con = sqlite3.connect("soc_dashboard.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS firewall_logs(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ip_version TEXT,
                   interface TEXT,
                   action TEXT,
                   protocol TEXT,
                   src_ip TEXT,
                   dest_ip TEXT,
                   src_port TEXT,
                   dest_port TEXT,
                   timestamp TEXT,
                   abuse_score REAL,
                   country TEXT,
                   isp TEXT,
                   UNIQUE(timestamp, src_ip, src_port, dest_ip, dest_port, protocol)
                   )
                   """)
    for entry in parsed_logs:
        cur.execute("""
                    INSERT OR IGNORE INTO firewall_logs 
                    (ip_version, interface, action, protocol, src_ip, dest_ip, src_port, dest_port, timestamp, abuse_score, country, isp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (entry["ip_version"], entry["interface"], entry["action"], entry["protocol"], entry["src_ip"], entry["dest_ip"], 
                          entry["src_port"], entry["dest_port"], entry["timestamp"], 
                          None, None, None)) 
                    #reminder ? values only take values as pure data, preventing sql injection
    con.commit()
    con.close()
                
        

if __name__ == "__main__":
    parsed_logs = parse_firewall_log("firewall.log")
    log_db(parsed_logs)
    print(f"Successfully parsed {len(parsed_logs)} log entries,")

#references:
#https://docs.netgate.com/pfsense/en/latest/monitoring/logs/raw-filter-format.html
#https://python-reference.readthedocs.io/en/latest/docs/str/strip.html
#https://www.w3schools.com/python/ref_string_split.asp
#https://docs.python.org/3/library/sqlite3.html