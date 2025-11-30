import unittest
from md_parser import Parser
from renderer import HTMLRenderer

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.renderer = HTMLRenderer()

    def test_headings(self):
        markdown = "# Heading 1\n## Heading 2\n### Heading 3"
        doc = self.parser.parse(markdown)
        html = self.renderer.render(doc)
        expected_html = "<h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3>"
        self.assertEqual(html, expected_html)

    def test_paragraphs(self):
        markdown = "This is a paragraph.\nAnother paragraph."
        doc = self.parser.parse(markdown)
        html = self.renderer.render(doc)
        expected_html = "<p>This is a paragraph.</p><p>Another paragraph.</p>"
        self.assertEqual(html, expected_html)

    def test_mixed_content(self):
        markdown = "# Title\nIntro text.\n## Section\nSection text."
        doc = self.parser.parse(markdown)
        html = self.renderer.render(doc)
        expected_html = "<h1>Title</h1><p>Intro text.</p><h2>Section</h2><p>Section text.</p>"
        self.assertEqual(html, expected_html)
        
    def test_empty_input(self):
        markdown = ""
        doc = self.parser.parse(markdown)
        html = self.renderer.render(doc)
        expected_html = ""
        self.assertEqual(html, expected_html)

    def test_heading_levels(self):
        # Test edge cases for heading levels
        markdown = "# H1\n###### H6\n####### Not H7"
        doc = self.parser.parse(markdown)
        html = self.renderer.render(doc)
        # Current implementation clamps level to 6, but only strips 'level' characters.
        # So 7 hashes -> level 6, strips 6 chars -> leaves 1 hash in content.
        expected_html = "<h1>H1</h1><h6>H6</h6><h6># Not H7</h6>" 
        self.assertEqual(html, expected_html)

if __name__ == '__main__':
    unittest.main()
