import attrs

from src.basm import opcodes, parser
from src.basm.context import Context

from .memory import Memory


@attrs.frozen
class EvalVisitor(parser.BaseBASMVisitor):
    memory: Memory
    context: Context

    def visit_StrNode(self, node: parser.StrNode) -> str:
        return node.value

    def visit_HexNode(self, node: parser.HexNode) -> int:
        return node.value

    def visit_IdNode(self, node: parser.IdNode) -> str:
        return node.value

    def visit_CallNode(self, node: parser.CallNode) -> opcodes.OpCodeReturn:
        opcode = self.memory[node.opcode.value]
        return opcode(*map(self.visit, node.args))(self.context)

    def visit_RootNode(self, root: parser.RootNode) -> opcodes.OpCodeReturn:
        r = opcodes.OpCodeReturn()
        for call in root.nodes:
            r |= self.visit_CallNode(call)  # type: ignore
        return r
