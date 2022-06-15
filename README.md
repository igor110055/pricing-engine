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
python price_publisher
```

## Notes

1. To add other sources (e.g. Bybit, FTX), create a function for each and append the result to LockStack.
2. To control (enable / disable) sources, we can create a class for it in the future. 
