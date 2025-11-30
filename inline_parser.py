import re
from typing import List
from ast_nodes import Node, Text, WikiLink

class InlineParser:
    # Pre-compile regex for performance
    WIKILINK_RE = re.compile(r'\[\[(.*?)(?:\|(.*?))?\]\]')

    def parse(self, text: str) -> List[Node]:
        nodes = []
        last_pos = 0
        
        # Iterate through all regex matches in the string
        for match in self.WIKILINK_RE.finditer(text):
            start, end = match.span()
            
            # 1. Plain text before the link
            if start > last_pos:
                text_chunk = text[last_pos:start]
                nodes.append(Text(text_chunk))
            
            # 2. The WikiLink itself
            target = match.group(1)
            alias = match.group(2) # This will be None if no pipe exists
            nodes.append(WikiLink(target, alias))
            
            last_pos = end
            
        # 3. Remaining plain text after the last link
        if last_pos < len(text):
            nodes.append(Text(text[last_pos:]))
            
        return nodes
