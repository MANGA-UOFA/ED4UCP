from library.tree import Tree, extract_words_from_str_tree, add_words_to_str_tree, Node

def filter_by_start(spans, start):
    return [span for span in spans if span[0]==start]
def get_largest_span(spans):
    return max(spans, key=lambda span: span[1]-span[0])
def same_span(span1, span2):
    return span1[0]==span2[0] and span1[1]==span2[1]
def filter_includeds(spans, ref):
    return [span for span in spans if (span[0]>=ref[0] and span[1]<=ref[1] and not same_span(span, ref))]
def spans_except(spans, exceptions):
    return [span for span in spans if not any([same_span(span, e) for e in exceptions])]

def build_sub_tree(root_span, spans):
    if root_span[0]==root_span[1]:
        return Node(root_span[0])
    root = Node(root_span)
    left_possibles = filter_by_start(spans, root_span[0])
    if len(left_possibles)==0:
        root.left = Node(root_span[0])
        root.right = build_sub_tree((root_span[0]+1, root_span[1]), spans)
    else:
        left_root_span = get_largest_span(left_possibles)
        left_spans = filter_includeds(spans, left_root_span)
        right_spans = spans_except(spans, left_spans+[left_root_span])
        if left_root_span[1]<root_span[1]:
            root.left = build_sub_tree(left_root_span, left_spans)
            root.right = build_sub_tree((left_root_span[1]+1, root_span[1]), right_spans)
        else:
            root = build_sub_tree(left_root_span, left_spans)
    return root

def forest_to_tree(forest):
    if type(forest) is list:
        return '(. '+' '.join([forest_to_tree(branch) for branch in forest])+')'
    else:
        return f'(. {forest})'

def node2forest(root):
    if root.has_child():
        return [node2forest(root.left), node2forest(root.right)]
    else:
        return root.label

def span_set_to_tree(size, span_set, reference):
    solution = build_sub_tree([0, size-1], span_set)
    solution = forest_to_tree(node2forest(solution))
    solution = add_words_to_str_tree(str(Tree(solution)), extract_words_from_str_tree(reference))
    return solution