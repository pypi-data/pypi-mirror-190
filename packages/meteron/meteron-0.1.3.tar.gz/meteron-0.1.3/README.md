# Meteron AI

Installation:

```bash
pip install meteron
```

Usage:

```python
import json

from meteron import Cluster

# Create your cluster that has one or more servers.
# In this example we will use https://lightning.ai/muse
cluster = Cluster(cluster='lightning-muse',
                  servers=[{
                      'url': 'https://ulhcn-01gd3c9epmk5xj2y9a9jrrvgt8.litng-ai-03.litng.ai/api/predict'
                  }])

cluster.initialize()

# Send the request to the cluster
result = cluster.image_gen(data=json.dumps({'prompt': 'spaceships above alien planet'}))

# Do whatever you want with the result
```