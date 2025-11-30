from pathlib import Path
from md_parser import Parser
from renderer import HTMLRenderer

def convert_all(input_dir: str, output_dir: str):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    parser = Parser()
    renderer = HTMLRenderer()
    
    print(f"Scanning {input_path} for markdown files...")
    
    files_processed = 0
    for md_file in input_path.glob('*.md'):
        print(f"Processing {md_file.name}...")
        
        # Read Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse and Render
        doc = parser.parse(content)
        html_content = renderer.render(doc)
        
        # Wrap in a basic HTML structure for better viewing
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{md_file.stem}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
        h1, h2, h3 {{ color: #333; }}
        p {{ line-height: 1.6; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
        
        # Write HTML
        output_file = output_path / f"{md_file.stem}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
            
        files_processed += 1
        
    print(f"Done! Processed {files_processed} files. Check {output_path} for results.")

if __name__ == "__main__":
    # You can configure these paths
    INPUT_DIR = "test_data"
    OUTPUT_DIR = "output_html"
    
    convert_all(INPUT_DIR, OUTPUT_DIR)
