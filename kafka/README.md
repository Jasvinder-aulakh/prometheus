kafka_exporterGG

Kafka exporter for Prometheus. For other metrics from Kafka, have a look at the JMX exporter

Table of Contents

Compatibility - Support Apache Kafka version 0.10.1.0 (and later).
Dependency - Prometheus
Download - wget https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-amd64.tar.gz
 
Run
Run Binary
kafka_exporter --kafka.server=kafka:9092 [--kafka.server=another-server ...]

Configure Service-
vim /etc/systemd/system/kafka_exporter.service

[Unit]
Description=Kafka Exporter

[Service]
User=kafka_exporter
ExecStart=/usr/local/bin/kafka_exporter  \
  --kafka.server=kafka-1:9092 --kafka.server=kafka-2:9092 --kafka.server=kafka-3:9092 --kafka.server=kafka-4:9092 --kafka.server=kafka-5:9092 \
  --web.listen-address=:7073 \
  --web.telemetry-path=/metrics
SyslogIdentifier=kafka_exporter
Restart=always
RestartSec=90
StartLimitInterval=400
StartLimitBurst=3


[Install]
WantedBy=multi-user.target


Flags

kafka.server	kafka:9092	Addresses (host:port) of Kafka server
kafka.version	1.0.0	Kafka broker version
sasl.enabled	false	Connect using SASL/PLAIN
sasl.handshake	true	Only set this to false if using a non-Kafka SASL proxy
sasl.username		SASL user name
sasl.password		SASL user password
tls.enabled	false	Connect using TLS
tls.ca-file		The optional certificate authority file for TLS client authentication
tls.cert-file		The optional certificate file for client authentication
tls.key-file		The optional key file for client authentication
tls.insecure-skip-tls-verify	false	If true, the server's certificate will not be checked for validity
topic.filter	.*	Regex that determines which topics to collect
group.filter	.*	Regex that determines which consumer groups to collect
web.listen-address	:9308	Address to listen on for web interface and telemetry
web.telemetry-path	/metrics	Path under which to expose metrics
log.level	info	Only log messages with the given severity or above. Valid levels: [debug, info, warn, error, fatal]
log.enable-sarama	false	Turn on Sarama logging


Notes
If you need to disable sasl.handshake, you could add flag --no-sasl.handshake

Metrics
Documents about exposed Prometheus metrics.
For details on the underlying metrics please see Apache Kafka.

Brokers

Metrics details

Name	Exposed informations
kafka_brokers	Number of Brokers in the Kafka Cluster

Topics
Metrics details

Name	Exposed informations
kafka_topic_partitions	Number of partitions for this Topic
kafka_topic_partition_current_offset	Current Offset of a Broker at Topic/Partition
kafka_topic_partition_oldest_offset	Oldest Offset of a Broker at Topic/Partition
kafka_topic_partition_in_sync_replica	Number of In-Sync Replicas for this Topic/Partition
kafka_topic_partition_leader	Leader Broker ID of this Topic/Partition
kafka_topic_partition_leader_is_preferred	1 if Topic/Partition is using the Preferred Broker
kafka_topic_partition_replicas	Number of Replicas for this Topic/Partition
kafka_topic_partition_under_replicated_partition	1 if Topic/Partition is under Replicated


Consumer Groups
Metrics details

Name	Exposed informations
kafka_consumergroup_current_offset	Current Offset of a ConsumerGroup at Topic/Partition
kafka_consumergroup_lag	Current Approximate Lag of a ConsumerGroup at Topic/Partition


And finally configure in prometheus:

#### Define Kafka Cluster Servers
  - job_name: "KAFKA_CLUSTER"
    file_sd_configs:
    - files:
      - kafka-cluster.yml

and kafka-cluster.yml:

- targets: ['IP:7073']
  labels:
    name: 'kafka-1 - kafka1'
    alias: 'IP'

Grafana Dashboard

Please import json from dashboard/kafka-cluster-overview


