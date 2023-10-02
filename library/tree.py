from library.stack import Stack

class Node:
    def __init__(self, label):
        self.left = None
        self.right = None
        self.label = label
        self.left_code = None
        self.right_code = None

    def has_child(self):
        return self.left is not None
    
    def get_children(self):
        return list(filter(lambda item: item is not None, [self.left, self.right]))
    
    def __str__(self):
        return f"({self.label}{''.join([' '+str(child) for child in self.get_children()])})"

    def set_span(self, i):
        self.left_code = i
        if self.has_child():
            i = self.left.set_span(i)
            i = self.right.set_span(i)
        else:
            i += 1
        self.right_code = i
        return i

    def get_span(self):
        return self.left_code, self.right_code-1
    
    def get_all_spans(self):
        if self.has_child():
            return [self.get_span()]+self.left.get_all_spans()+self.right.get_all_spans()
        else:
            return []
        
    def __len__(self):
        if self.has_child():
            return len(self.left)+len(self.right)
        else:
            return 1



class Tree:
    def __init__(self, line):
        self.root = Tree.__parse(line)

    def __split_to_childs(line):
        stack = Stack()
        children = []
        inside = False
        for character in line:
            if character=='(':
                stack.push(None)
                if not inside:
                    children.append('')
                inside = True
            if character==')':
                stack.pop()
            if inside:
                children[-1] += character
            if inside and stack.is_empty():
                inside = False
        return children
    
    def __right_binarization(label, children):
        if len(children)==0:
            return Node(label)
        if len(children)==1:
            return Tree.__parse(children[0])
        parent = Node(label)
        parent.left = Tree.__parse(children[0])
        parent.right = Tree.__right_binarization('.', children[1:])
        return parent

    def __parse(line):
        line = line[1:-1].strip()
        children = Tree.__split_to_childs(line)
        return Tree.__right_binarization(line.split()[0], children)
    
    def __str__(self):
        return str(self.root)
    
    def __len__(self):
        return len(self.root)



def add_words_to_str_tree(str_tree, words):
    output = ""
    closed = False
    for c in str_tree:
        if c == ')' and not closed:
            output += " " + words[0]
            words = words[1:]
            closed = True
        elif c != ')':
            closed = False
        output += c
    assert len(words)==0
    return output


def extract_words_from_str_tree(line):
    line = line.strip()
    words = []
    for part in line.split():
        if part[-1] == ')':
            words.append(part.replace(')', ''))
    return words