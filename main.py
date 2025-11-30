from pathlib import Path
from md_parser import Parser
from renderer import HTMLRenderer

def main():
    input_markdown = Path("sample.md").read_text(encoding="utf-8")
    
    # 1. Parse
    parser = Parser()
    doc = parser.parse(input_markdown)
    
    print("Parsed AST:")
    print(doc.pretty())
    print("-" * 20)

    # 2. Render
    renderer = HTMLRenderer()
    html = renderer.render(doc)
    
    print("Generated HTML:")
    print(html)

if __name__ == "__main__":
    main()
