from dataclasses import dataclass, field


@dataclass
class TreeNode:
    char: str = None
    children: dict = field(default_factory=dict)
    terminal: bool = False


def next_char(node, part_word):
    try:
        c = part_word[0]
        rest_word = part_word[1:]
        try:
            return next_char(node.children[c], rest_word)
        except KeyError:
            return []
    except IndexError:
        if node.terminal:
            return list(node.children.keys()) + [None]
        else:
            return list(node.children.keys())


def add(node, word):
    try:
        c = word[0]
        rest_word = word[1:]
        try:
            child = node.children[c]
        except KeyError:
            child = TreeNode(c)
        node.children[c] = child
        add(child, rest_word)
    except IndexError:
        node.terminal = True


def make_word_tree(wordlist):
    dt = TreeNode()
    for word in wordlist:
        add(dt, word)
    return dt
