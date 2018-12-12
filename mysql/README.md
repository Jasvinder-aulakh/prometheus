Prometheus MySQL exporter init script for Centos 6 and Centos7.

<<<<<<<<<<<<<<<<<<<<< Centos6 >>>>>>>>>>>>>>>>>>>>>
Step1. >> Create exporter user

useradd -s /sbin/nologin exporter

Step 2. >> Download and install Prometheus MySQL Exporter:

source: https://github.com/prometheus/mysqld_exporter.git

Step 3. Create exporter database user

CREATE USER 'exporter'@'localhost' IDENTIFIED BY 'StrongPassword' WITH MAX_USER_CONNECTIONS 3;

GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';

FLUSH PRIVILEGES;


Step 4.   Configure database credentials

vim /etc/.mysqld_exporter.cnf

Add user details as below:

[client]
user=exporter
password=StrongPassword

Set ownership: sudo chown root:exporter /etc/.mysqld_exporter.cnf


Step 5. Create daemon configuration file

# vim  /etc/sysconfig/mysqld_exporter

# Prometheus mysqld_exporter defaults
# See https://github.com/prometheus/mysqld_exporter
ARGS="--config.my-cnf /etc/.mysqld_exporter.cnf \
  --collect.info_schema.processlist.min_time=0 \
  --collect.info_schema.processlist.processes_by_user  \
  --collect.info_schema.processlist.processes_by_host  \
  --collect.info_schema.tables.databases="*" \
  --collect.mysql.user.privileges \
  --collect.perf_schema.file_instances.filter=".*" \
  --web.listen-address=:9104 \
  --web.telemetry-path=/metrics \
  --collect.mysql.user \
  --collect.info_schema.tables \
  --collect.info_schema.innodb_tablespaces \
  --collect.info_schema.innodb_metrics \
  --collect.global_status \
  --collect.global_variables \
  --collect.slave_status \
  --collect.info_schema.processlist \
  --collect.perf_schema.tablelocks  \
  --collect.perf_schema.eventsstatements \
  --collect.perf_schema.eventswaits \
  --collect.perf_schema.file_events \
  --collect.auto_increment.columns \
  --collect.binlog_size \
  --collect.perf_schema.tableiowaits \
  --collect.perf_schema.indexiowaits \
  --collect.info_schema.tablestats \
  --collect.info_schema.query_response_time \
  --collect.perf_schema.file_instances \
  --collect.perf_schema.replication_group_member_stats \
  --collect.info_schema.userstats \
  --collect.info_schema.clientstats \
  --collect.engine_innodb_status \
  --collect.slave_hosts"
  
  
  Step 5. Create the init script file
  
# vim  /etc/init.d/mysqld_exporter

#!/bin/bash
# mysqld_exporter    This shell script takes care of starting and stopping mysqld_exporter
#
# chkconfig: 2345 80 80
# description: Mysqld exporter start script
# processname: mysqld_exporter
# config: /etc/.mysqld_exporter.cnf
# pidfile: /var/run/mysqld_exporter.pid

# Source function library - For CentOS
. /etc/rc.d/init.d/functions

RETVAL=0
PROGNAME=mysqld_exporter
PROG=/usr/local/mysqld_exporter/${PROGNAME}
RUNAS=exporter
LOCKFILE=/var/lock/subsys/${PROGNAME}
PIDFILE=/var/run/${PROGNAME}.pid
LOGFILE=/var/log/${PROGNAME}.log
DAEMON_SYSCONFIG=/etc/sysconfig/${PROGNAME}

# GO CPU Limit

#GOMAXPROCS=$(grep -c ^processor /proc/cpuinfo)
GOMAXPROCS=1

# Source config

. ${DAEMON_SYSCONFIG}

start() {
    if [[ -f $PIDFILE ]] > /dev/null; then
        echo "mysqld_exporter is already running"
        exit 0
    fi

    echo -n "Starting mysqld_exporter service…"
    daemonize -u ${USER} -p ${PIDFILE} -l ${LOCKFILE} -a -e ${LOGFILE} -o ${LOGFILE} ${PROG} ${ARGS}
    RETVAL=$?
    echo ""
    return $RETVAL
}

stop() {
    if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
        echo "Service not running"
        return 1
    fi
    echo 'Stopping service…'
    #kill -15 $(cat "$PIDFILE") && rm -f "$PIDFILE"
    killproc -p ${PIDFILE} -d 10 ${PROG}
    RETVAL=$?
    echo
    [ $RETVAL = 0 ] && rm -f ${LOCKFILE} ${PIDFILE}
    return $RETVAL
}

status() {
    if [ -f "$PIDFILE" ] || kill -0 $(cat "$PIDFILE"); then
      echo "mysqld exporter service running..."
      echo "Service PID: `cat $PIDFILE`"
    else
      echo "Service not running"
    fi
     RETVAL=$?
     return $RETVAL
}

# Call function
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 2
esac



Step 6. Provide exec permission.

chmod +x mysqld_exporter

Step 7.  start the service, just run: and Set it to start on boot

# sudo /etc/init.d/mysqld_exporter start
# chkconfig mysqld_exporter on






  
  
  
  
