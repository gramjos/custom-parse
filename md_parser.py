from ast_nodes import Document, Heading, Paragraph, Text, Node
from inline_parser import InlineParser

class Parser:
    def __init__(self):
        self.inline_parser = InlineParser()

    def parse(self, text: str) -> Document:
        doc = Document()
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('#'):
                # Count the number of '#' at the start
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                
                # Ensure valid heading level (1-6)
                level = min(max(level, 1), 6)
                
                content = line[level:].strip()
                heading = Heading(level)
                heading.add(Text(content))
                doc.add(heading)
            else:
                # Treat everything else as a paragraph for now
                p = Paragraph()
                p.add(Text(line))
                doc.add(p)
        
        # --- PASS 2: Inline Parsing ---
        self._process_inline_elements(doc)
                
        return doc

    def _process_inline_elements(self, node: Node):
        """
        Recursively walks the tree. 
        If it finds a Text node, it runs the inline parser and expands it.
        """
        new_children = []
        
        for child in node.children:
            # If we hit a leaf Text node, explode it!
            if isinstance(child, Text):
                parsed_nodes = self.inline_parser.parse(child.content)
                new_children.extend(parsed_nodes)
            else:
                # If it's a block (Heading/Paragraph), recurse deeper
                self._process_inline_elements(child)
                new_children.append(child)
        
        node.children = new_children
