from abc import ABC, abstractmethod
from typing import List, Optional
from ast_nodes import Node, Heading, CodeBlock, Paragraph, Text

class LineReader:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.current_index = 0

    def peek(self) -> Optional[str]:
        if self.has_next():
            return self.lines[self.current_index]
        return None

    def next(self) -> Optional[str]:
        if self.has_next():
            line = self.lines[self.current_index]
            self.current_index += 1
            return line
        return None

    def has_next(self) -> bool:
        return self.current_index < len(self.lines)

class BlockProcessor(ABC):
    @abstractmethod
    def can_start(self, line: str) -> bool:
        pass

    @abstractmethod
    def run(self, parent: Node, reader: LineReader) -> Node:
        pass

class HeadingProcessor(BlockProcessor):
    def can_start(self, line: str) -> bool:
        return line.startswith('#')

    def run(self, parent: Node, reader: LineReader) -> Node:
        line = reader.next()
        if line is None:
            raise ValueError("Unexpected end of input in HeadingProcessor")
        
        level = 0
        for char in line:
            if char == '#':
                level += 1
            else:
                break
        
        level = min(max(level, 1), 6)
        content = line[level:].strip()
        
        heading = Heading(level)
        heading.add(Text(content))
        parent.add(heading)
        return heading

class CodeBlockProcessor(BlockProcessor):
    def can_start(self, line: str) -> bool:
        return line.strip().startswith('```')

    def run(self, parent: Node, reader: LineReader) -> Node:
        start_line = reader.next() # Consume the opening fence
        if start_line is None:
            raise ValueError("Unexpected end of input in CodeBlockProcessor")

        language = start_line.strip()[3:].strip()
        code_block = CodeBlock(language)
        
        code_content = []
        while reader.has_next():
            line = reader.peek()
            if line is None:
                break
                
            if line.strip().startswith('```'):
                reader.next() # Consume closing fence
                break
            
            # Consume the line
            content_line = reader.next()
            if content_line is not None:
                code_content.append(content_line)
            
        full_content = "\n".join(code_content)
        code_block.add(Text(full_content))
        parent.add(code_block)
        return code_block

class ParagraphProcessor(BlockProcessor):
    def can_start(self, line: str) -> bool:
        return line.strip() != ""

    def run(self, parent: Node, reader: LineReader) -> Node:
        paragraph = Paragraph()
        lines = []
        
        while reader.has_next():
            line = reader.peek()
            if line is None:
                break
            
            # Stop if we hit an empty line (paragraph break)
            if not line.strip():
                reader.next() # Consume the empty line
                break
                
            # Stop if we hit something that looks like another block
            if line.startswith('#') or line.strip().startswith('```'):
                break
                
            content_line = reader.next()
            if content_line is not None:
                lines.append(content_line)
            
        content = " ".join(lines).strip()
        paragraph.add(Text(content))
        parent.add(paragraph)
        return paragraph
