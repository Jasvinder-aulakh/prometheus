#########
##### Aerospike exporter setup in centos 7 to monitor all aerospike cluster metrics through prometheus.

1. Download aerospike_exporter

# wget https://github.com/staticmukesh/aerospike_exporter/releases/download/v0.1.2/aerospike_exporter-v0.1.2.linux-amd64.tar.gz

2. Extract and move to /usr/local/bin

# mv aerospike_exporter /usr/local/bin

3. Create a service file to start aerospike_exporter service

# vim /etc/systemd/system/aerospike_exporter.service

And configure as :

[Unit]
Description=Aerospike Exporter

[Service]
User=aerospike_exporter
ExecStart=/usr/local/bin/aerospike_exporter  \
  --aerospike.addr=Fisrtnode:3000 --aerospike.addr=secondnode:3000 --aerospike.addr=thirdnode:3000 \
  --web.listen-address=:9145 \
  --web.telemetry-path=/metrics
SyslogIdentifier=aerospike_exporter
Restart=always
RestartSec=90
StartLimitInterval=400
StartLimitBurst=3


[Install]
WantedBy=multi-user.target


4. Create a user 

# useradd -s /bin/nologin aerospike_exporter

5. Reload the daemon
  
#  systemctl daemon-reload

6. Start the aerospike_exporter
 
#  systemctl start aerospike_exporter

7. Check port 9145, should be listen

# netstat -ntlp| grep LISTEN

Output should be:  0 :::9145                 :::*                    LISTEN      20223/aerospike_exp

8. Finaly check exporter metrics:

# curl localhost:9145/metrics |head
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0# HELP as_build Build of Aerospike node
# TYPE as_build gauge
as_build{addr="30.51.12.187:3000",alias="",build="4.3.1.4"} 1
# HELP as_edtion Edition of Aerospike node
# TYPE as_edtion gauge
1as_edtion{addr="30.51.12.187:3000",alias="",edition="Aerospike Enterprise Edition"} 1
0# HELP as_node_name Name of Aerospike node
0# TYPE as_node_name gauge
 as_node_name{addr="30.51.12.187:3000",alias="",id="BB93805E179A902"} 1
5# HELP as_ns_allow_nonxdr_writes allow-nonxdr-writes
5861  100 55861    0     0  5505k      0 --:--:-- --:--:-- --:--:-- 6061k
(23) Failed writing body


### Now configure aerospike cluster metrics in prometheus server config:

1. Define Aeerospike exporter node in prometheus.yml file as below:

# vim prometheus.yml

#### Define AEROSPIKE Nodes
  - job_name: "aerospike_exporter"
    file_sd_configs:
    - files:
      - aerospike.yml

2. Define aerospike.yml file

# vim aerospike.yml

####  component aerospike
- targets: ['IP:9145']
  labels:
    name: 'hostname'
    alias: 'IP' 

####### Finally restart the prometheus service

## You will look aeropike node in target and can see all metrics there

## Now grafana setup

Go in dashboard folder in same reposiotary and import the aerospike json in your grafana, you will look aerospike cluster metrics as 
