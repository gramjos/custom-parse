from ast_nodes import NodeType, Node

class HTMLRenderer:
    def render(self, node: Node) -> str:
        if node.type == NodeType.DOCUMENT:
            return "".join([self.render(child) for child in node.children])
        elif node.type == NodeType.HEADING:
            return f"<h{node.level}>{self.render_children(node)}</h{node.level}>"
        elif node.type == NodeType.PARAGRAPH:
            return f"<p>{self.render_children(node)}</p>"
        elif node.type == NodeType.TEXT:
            return node.content or ""
        else:
            # Fallback for unknown nodes
            return self.render_children(node)

    def render_children(self, node: Node) -> str:
        return "".join([self.render(child) for child in node.children])
