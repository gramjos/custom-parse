from md_parser import Parser
from renderer import HTMLRenderer

def main():
    input_markdown = """
# Hello World
This is a paragraph.
## Subheading
Another paragraph.
    """
    
    # 1. Parse
    parser = Parser()
    doc = parser.parse(input_markdown)
    
    print("Parsed AST:")
    print(doc)
    print("-" * 20)

    # 2. Render
    renderer = HTMLRenderer()
    html = renderer.render(doc)
    
    print("Generated HTML:")
    print(html)

if __name__ == "__main__":
    main()
