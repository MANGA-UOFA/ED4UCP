from collections import defaultdict
from library.cyk_variant import cyk_variant

def sum_span_scores(spans, key_function=str):
    output = defaultdict(lambda: 0)
    for span, score in spans:
        output[key_function(span)] += score
    return output

def find_average_tree(teacher_trees, weights, vote_ignoring_level=0):
    K = len(teacher_trees)
    for tree in teacher_trees:
        tree.root.set_span(0)
    trees_spans = [tree.root.get_all_spans()[1:] for tree in teacher_trees]
    size = len(trees_spans[0])+2
    all_spans = []
    for spans, weight in zip(trees_spans, weights):
        all_spans += [(span, weight) for span in spans]
    span_scores = sum_span_scores(all_spans, key_function=str)
    span_scores = {k: v for k, v in span_scores.items() if v>vote_ignoring_level}
    selected_spans = cyk_variant(span_scores, size)
    selected_spans = [[int(s) for s in span[1:-1].split(', ')] for span in selected_spans]
    return selected_spans