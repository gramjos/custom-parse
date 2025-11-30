from ast_nodes import Node, Document, Heading, Paragraph, Text, WikiLink, Italic, Bold, CodeBlock
from visitor import NodeVisitor

class HTMLRenderer(NodeVisitor):
    def render(self, node: Node) -> str:
        """Entry point for the renderer."""
        return self.visit(node)

    def visit_Document(self, node: Document) -> str:
        return "".join(self.visit(child) for child in node.children)

    def visit_Heading(self, node: Heading) -> str:
        content = self._render_children(node)
        return f"<h{node.level}>{content}</h{node.level}>"

    def visit_Paragraph(self, node: Paragraph) -> str:
        content = self._render_children(node)
        return f"<p>{content}</p>"

    def visit_Text(self, node: Text) -> str:
        return node.content or ""

    def visit_WikiLink(self, node: WikiLink) -> str:
        display_text = node.alias if node.alias else node.target
        return f'<a href="{node.target}">{display_text}</a>'

    def visit_Italic(self, node: Italic) -> str:
        content = self._render_children(node)
        return f"<em>{content}</em>"

    def visit_Bold(self, node: Bold) -> str:
        content = self._render_children(node)
        return f"<strong>{content}</strong>"

    def visit_CodeBlock(self, node: CodeBlock) -> str:
        content = self._render_children(node)
        # Escape HTML entities if needed, but for now just wrap
        class_attr = f' class="language-{node.language}"' if node.language else ""
        return f'<pre><code{class_attr}>{content}</code></pre>'

    def generic_visit(self, node: Node) -> str:
        # Fallback for unimplemented nodes (like Lists/BlockQuotes if they appear)
        return self._render_children(node)

    def _render_children(self, node: Node) -> str:
        """Helper to visit all children and join their results."""
        return "".join(self.visit(child) for child in node.children)
