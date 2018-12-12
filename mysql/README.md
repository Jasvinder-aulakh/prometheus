** Prometheus MySQL exporter init script for Centos 6. **

<<<<<<<<<<<<<<<<<<<<< Centos6 >>>>>>>>>>>>>>>>>>>>>
**Step1. >> Create exporter user

useradd -s /sbin/nologin exporter

**Step 2. >> Download and install Prometheus MySQL Exporter:

source: https://github.com/prometheus/mysqld_exporter.git

**Step 3. Create exporter database user

CREATE USER 'exporter'@'localhost' IDENTIFIED BY 'StrongPassword' WITH MAX_USER_CONNECTIONS 3;

GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';

FLUSH PRIVILEGES;


**Step 4.   Configure database credentials

vim /etc/.mysqld_exporter.cnf

Add user details as below:

[client]
user=exporter
password=StrongPassword

Set ownership: sudo chown root:exporter /etc/.mysqld_exporter.cnf


**Step 5. Create daemon configuration file, download from mysql folder.


**Step 6. Provide exec permission.

chmod +x mysqld_exporter

**Step 7.  start the service, just run: and Set it to start on boot

# sudo /etc/init.d/mysqld_exporter start
# chkconfig mysqld_exporter on






  
  
  
  
