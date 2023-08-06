# pynodeinfo

Python NodeInfo library implemented with poetry.


## Usage

```python
import nodeinfo

async main():
    host = "mastodon.social"

    print(await nodeinfo.load(host))
```
