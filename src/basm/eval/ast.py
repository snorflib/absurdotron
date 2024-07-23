import attrs

from src.basm import opcodes, parser

from .memory import Memory


@attrs.frozen
class EvalVisitor(parser.BaseBASMVisitor):
    memory: Memory

    def visit_StrNode(self, node: parser.StrNode) -> str:
        return node.value

    def visit_HexNode(self, node: parser.HexNode) -> int:
        return node.value

    def visit_IdNode(self, node: parser.IdNode) -> str:
        return node.value

    def visit_CallNode(self, node: parser.CallNode) -> opcodes.OpCodeReturn:
        opcode = self.memory[node.opcode.value]
        return opcode(*map(self.visit, node.args))

    def visit_RootNode(self, node: parser.RootNode) -> opcodes.OpCodeReturn:
        r = opcodes.OpCodeReturn()
        for call in node.calls:
            r |= self.visit_CallNode(call)
        return r
