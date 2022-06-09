# Pricing Engine

Pricing Engine based on Partial Book Depth.

## Setup

```bash
# 1. Install dependencies
poetry install

# 2. Copy .env.example to .env and fill in all variables
cp .env.example .env

# 3. Activate python virtual-env
poetry shell

# 4. Execute it
python pricing_engine
```

---
### Confluent Kafka Config (Backup as Reference)

```conf
# Required connection configs for Kafka producer, consumer, and admin
bootstrap.servers=pkc-ew3qg.asia-southeast2.gcp.confluent.cloud:9092
security.protocol=SASL_SSL
sasl.mechanisms=PLAIN
sasl.username={{ CLUSTER_API_KEY }}
sasl.password={{ CLUSTER_API_SECRET }}

# Best practice for higher availability in librdkafka clients prior to 1.7
session.timeout.ms=45000

# Required connection configs for Confluent Cloud Schema Registry
schema.registry.url=https://{{ SR_ENDPOINT }}
basic.auth.credentials.source=USER_INFO
basic.auth.user.info={{ SR_API_KEY }}:{{ SR_API_SECRET }}
```