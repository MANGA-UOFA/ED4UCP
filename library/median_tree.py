def find_median_tree(teacher_trees):
    for tree in teacher_trees:
        tree.root.set_span(0)
    trees_spans = [set(tree.root.get_all_spans()[1:]) for tree in teacher_trees]
    best_tree, best_score = None, -1
    for i, spanset in enumerate(trees_spans):
        score = sum([len(spanset.intersection(other_spanset)) for other_spanset in trees_spans])
        if score > best_score:
            best_tree, best_score = i, score
    return teacher_trees[best_tree]