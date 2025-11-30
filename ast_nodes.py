from dataclasses import dataclass, field
from typing import List, Optional, Union
from enum import Enum, auto
#Here

# 1. Node Types
class NodeType(Enum):
    DOCUMENT = auto()
    HEADING = auto()
    PARAGRAPH = auto()
    BLOCK_QUOTE = auto()
    CODE_BLOCK = auto()
    LIST = auto()
    LIST_ITEM = auto()
    TEXT = auto()
    WIKILINK = auto()  # Obsidian specific
    ITALIC = auto()
    BOLD = auto()

# 2. Base Node
@dataclass
class Node:
    type: NodeType
    children: List['Node'] = field(default_factory=list)
    content: Optional[str] = None # For leaf nodes (Text)
    
    def add(self, node: 'Node'):
        self.children.append(node)

    def pretty(self, level: int = 0) -> str:
        indent = "  " * level
        name = self.__class__.__name__
        
        details = []
        if self.content:
            details.append(f"content={repr(self.content)}")
        
        if hasattr(self, 'level'):
            details.append(f"level={getattr(self, 'level')}")
        
        language = getattr(self, 'language', None)
        if language:
            details.append(f"language={language}")
            
        target = getattr(self, 'target', None)
        if target:
            details.append(f"target={target}")
            
        alias = getattr(self, 'alias', None)
        if alias:
            details.append(f"alias={alias}")
            
        detail_str = f" ({', '.join(details)})" if details else ""
        
        result = f"{indent}{name}{detail_str}\n"
        
        for child in self.children:
            result += child.pretty(level + 1)
            
        return result

# 3. Block Nodes
@dataclass
class Document(Node):
    def __init__(self):
        super().__init__(NodeType.DOCUMENT)

@dataclass
class Heading(Node):
    level: int = 1
    def __init__(self, level: int):
        super().__init__(NodeType.HEADING)
        self.level = level

@dataclass
class Paragraph(Node):
    def __init__(self):
        super().__init__(NodeType.PARAGRAPH)

@dataclass
class CodeBlock(Node):
    language: str = ""
    def __init__(self, language: str = ""):
        super().__init__(NodeType.CODE_BLOCK)
        self.language = language

# 4. Inline Nodes
@dataclass
class Text(Node):
    def __init__(self, text: str):
        super().__init__(NodeType.TEXT, content=text)

@dataclass
class WikiLink(Node):
    target: str = ""
    alias: Optional[str] = None
    def __init__(self, target: str, alias: Optional[str] = None):
        super().__init__(NodeType.WIKILINK)
        self.target = target
        self.alias = alias

@dataclass
class Italic(Node):
    def __init__(self):
        super().__init__(NodeType.ITALIC)

@dataclass
class Bold(Node):
    def __init__(self):
        super().__init__(NodeType.BOLD)
