from library.tree import Tree, extract_words_from_str_tree
from library import MBR

def right_tree(words):
    string = "(. "+' '.join([f'(. {word})' for word in words])+")"
    return Tree(string)

def ensemble(references, right=False, MBR_mode='generative'): # MBR_mode: generative or selective
    MBR_method = MBR.generate if MBR_mode.startswith('gen') else MBR.select
    ensembles = []
    cursed_ids = set()
    for i, reference_trees in enumerate(zip(*[r for r in references])):
        if '\n' in reference_trees:
            cursed_ids.add(i)
            continue
        first_ref_str = reference_trees[0]
        reference_trees = [Tree(r) for r in reference_trees]
        if right:
            reference_trees.append(right_tree(extract_words_from_str_tree(first_ref_str)))
        ens = MBR_method(reference_trees, first_ref_str)
        ensembles.append(ens)

    return ensembles