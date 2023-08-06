# RPS Client SDK Python

-   [x] RPS Webhook
-   [ ] RPS WebSocket
-   [ ] RPS SendFile

### Install via `pip`

```shell
pip install rps_client
```

### Usages

```python
from rps_client.models import RpsClientOptions, RpsHookRequest
from rps_client.sdk import RpsClient

API_KEY = 'YOUR_API_KEY'
DATA = RpsHookRequest(
    data={
        'mytext': 'my world is here',
        'bool': True,
    },
    type='test',
    details={
        'name': 'Hello World',
        'number': 1000,
    }
)

sdk = RpsClient(RpsClientOptions.builder().api_key(TEST_API_KEY).build())
reponse = sdk.send(DATA)
print(response.data)
```

### Build, Install, and Test from Source

```shell
make
```

### Build and Install from Source

```shell
make build install
```

### Run test

```shell
make test
```

### Publish

-   Set Token

```shell
poetry config pypi-token.pypi my-token
```

-   Publish

```shell
make publish
```

### Contributors

-   Sambo Chea <sombochea@cubetiqs.com>
