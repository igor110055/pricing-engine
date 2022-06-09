# Pricing Engine

> **WIP**

Pricing Engine Bruh...


## Confluent Kafka Config

```conf
# Required connection configs for Kafka producer, consumer, and admin
bootstrap.servers=pkc-ew3qg.asia-southeast2.gcp.confluent.cloud:9092
security.protocol=SASL_SSL
sasl.mechanisms=PLAIN
sasl.username={{ CLUSTER_API_KEY }}
sasl.password={{ CLUSTER_API_SECRET }}
sasl.username=YRW5BYWA5UPIVCMV
sasl.password=IspdLpjveC3h9d6FFq8AN9T9ZuaCZgOn15uzacj3PK7+pDrg0NFzGnp9cO/No9bf

# Best practice for higher availability in librdkafka clients prior to 1.7
session.timeout.ms=45000

# Required connection configs for Confluent Cloud Schema Registry
schema.registry.url=https://{{ SR_ENDPOINT }}
basic.auth.credentials.source=USER_INFO
basic.auth.user.info={{ SR_API_KEY }}:{{ SR_API_SECRET }}
```