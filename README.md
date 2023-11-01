# fastapi_healthz

Streamline your health checks with FastAPI using this user-friendly health check module. It serves as the foundational
component for integrating and enhancing health checks within FastAPI.

This core module doesn't include any service checkers by default, but it offers a simple method for adding them. The
reason for housing various modules separately is to accommodate the distinct dependencies required for each, ensuring
that you only import the specific packages you need, thereby preventing any unnecessary package bloat.

**This package is Pydantic v2 compliant**.

## Install

`pip install fastapi-healthz` or `poetry add fastapi-healthz`

## Adding Health Checks

Here is what you need to get started.

```python
from fastapi import FastAPI
from fastapi_healthz import (
    HealthCheckRegistry,
    HealthCheckRabbitMQ,
    HealthCheckRedis,
    HealthCheckUri,
    HealthCheckDatabase,
    health_check_route,
)

app = FastAPI()

# Add Health Checks
_healthChecks = HealthCheckRegistry()

# SQLAlchemy
_healthChecks.add(HealthCheckDatabase(uri="dialect+driver://username:password@host:port/database"))
# RabbitMQ
_healthChecks.add(HealthCheckRabbitMQ(host="localhost", port=5672, vhost="", username="username", password="pwd", ssl=True))
# Redis
_healthChecks.add(HealthCheckRedis(uri="redis://[password:]host:port/database"))
# This will check external URI and validate the response that is returned.
_healthChecks.add(HealthCheckUri(uri="https://www.reddit.com/r/aww.json"))

app.add_api_route('/health', endpoint=health_check_route(registry=_healthChecks))

```

## Returned Data

When you initiate a health check request, it will examine all the submitted entries and execute a fundamental query on
each of them. If the results conform to expectations, a status code of 200 is returned. However, if an error is
encountered, a 500 error response will be provided.

```json
{
    "status":"Healthy",
    "totalTimeTaken":"0:00:00.671642",
    "entities":[
        {
            "alias":"db",
            "status":"Healthy",
            "timeTaken":"0:00:00.009619",
            "tags":["db"]
        },
        {
            "alias":"reddit",
            "status":"Unhealthy",
            "timeTaken":"0:00:00.661716",
            "tags":["uri"]
        }
    ]
}
```

## Writing a custom checker
You can effortlessly extend the functionality of this foundational module by incorporating additional health checks for
various services. Simply create a new service that imports the HealthCheckAbstract. Then, build the corresponding class
around this abstract.

Once your service is prepared, integrate it into the HealthCheckRegistry, and you're all set to commence testing.