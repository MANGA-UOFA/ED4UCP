from library.tree import Tree, extract_words_from_str_tree, add_words_to_str_tree

def right(tree):
    words = extract_words_from_str_tree(tree)
    string = "(. "+' '.join([f'(. {word})' for word in words])+")"
    return add_words_to_str_tree(str(Tree(string)), words)

def left(tree):
    if type(tree) is not list:
        tree = extract_words_from_str_tree(tree)
    if len(tree)==1:
        return f"(. {tree[0]})"
    return f"(. {left(tree[:-1])} (. {tree[-1]}))"

def oracle(tree):
    return add_words_to_str_tree(str(Tree(tree)), extract_words_from_str_tree(tree))
