from ast_nodes import Document, Heading, Paragraph, Text

class Parser:
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
                
        return doc
