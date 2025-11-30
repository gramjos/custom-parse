# Obsidian Markdown to HTML

## Usage

### `ctags`
```zsh
ctags -R --languages=Python \
  --exclude=.git \
  --exclude=.venv \
  --exclude=__pycache__ \
  --exclude=build \
  --exclude=dist \
  --exclude='*.egg-info' \
  --exclude=output_html \
  --exclude=test_data
```

To run the parser on the sample input:
```bash
python3 main.py
```

To run the batch converter:
```bash
python3 batch_converter.py
```

## Technical Notes:
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
