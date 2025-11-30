Techincal Notes:
Dataclasses:
	Default factory:

```python
@dataclass
class Node:
    type: NodeType
    children: List['Node'] = []
	# the above is wrong because when `Node` is initialized the same reference for `children` will shared across isntances of `Node`
	# `field(default_factory=list)` Is use to created a fresh new children's list for every instance of `Node` 
    children: List['Node'] = field(default_factory=list)
```
