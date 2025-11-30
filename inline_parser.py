import re
from typing import List
from ast_nodes import Node, Text, WikiLink, Italic

class InlineParser:
    # --- Regex Construction ---

    # 1. WikiLink: [[Target]] or [[Target|Alias]]
    # Group 1: Full match
    # Group 2: Target
    # Group 3: Alias (optional)
    wikilink_pattern = r'(\[\[(.*?)(?:\|(.*?))?\]\])'

    # 2. Italic: *text*
    # Group 4: Full match
    # Group 5: Content
    italic_star_pattern = r'(\*(.+?)\*)'

    # 3. Italic: _text_
    # Group 6: Full match
    # Group 7: Content
    italic_underscore_pattern = r'(_(.+?)_)'

    # Combine and compile
    TOKEN_RE = re.compile(f'{wikilink_pattern}|{italic_star_pattern}|{italic_underscore_pattern}')

    def parse(self, text: str) -> List[Node]:
        nodes = []
        last_pos = 0
        
        # Iterate through all regex matches in the string
        for match in self.TOKEN_RE.finditer(text):
            start, end = match.span()
            
            # 1. Plain text before the match
            if start > last_pos:
                text_chunk = text[last_pos:start]
                nodes.append(Text(text_chunk))
            
            # 2. Handle the match
            if match.group(1): # WikiLink
                target = match.group(2)
                alias = match.group(3)
                nodes.append(WikiLink(target, alias))
            elif match.group(4): # Italic (star)
                content = match.group(5)
                italic = Italic()
                italic.add(Text(content))
                nodes.append(italic)
            elif match.group(6): # Italic (underscore)
                content = match.group(7)
                italic = Italic()
                italic.add(Text(content))
                nodes.append(italic)
            
            last_pos = end
            
        # 3. Remaining plain text after the last match
        if last_pos < len(text):
            nodes.append(Text(text[last_pos:]))
            
        return nodes
