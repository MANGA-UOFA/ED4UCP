from library.tree import extract_words_from_str_tree, add_words_to_str_tree
from library.MBRutils import span_set_to_tree
from library.median_tree import find_median_tree
from library.average_tree import find_average_tree

def select(reference_trees, ref_str):
    solution = find_median_tree(reference_trees)
    solution = add_words_to_str_tree(str(solution), extract_words_from_str_tree(ref_str))
    return solution

def generate(reference_trees, ref_str):
    avg = find_average_tree(reference_trees, [1]*len(reference_trees))
    avg = span_set_to_tree(len(reference_trees[0]), avg, ref_str)
    return avg
