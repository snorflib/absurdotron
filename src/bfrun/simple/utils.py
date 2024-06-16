import bidict


def build_jump_map(code: str) -> bidict.bidict[int, int]:
    jump_map: bidict.bidict[int, int] = bidict.bidict()
    stack: list[int] = []
    current_idx: int = 0

    for current_idx, char in enumerate(code):
        match char:
            case "[":
                stack.append(current_idx)
            case "]":
                if not stack:
                    raise ValueError("Code is trying to close an unexistent loop.")
                jump_map[stack.pop()] = current_idx

    if stack:
        raise ValueError("Code doesn't close all the loops.")

    return jump_map
