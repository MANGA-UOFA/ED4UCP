import numpy as np
from collections import defaultdict

def get_stats(span1, span2):
    tp = 0
    fp = 0
    fn = 0
    for span in span1:
        if span in span2:
            tp += 1
        else:
            fp += 1
    for span in span2:
        if span not in span1:
            fn += 1
    return tp, fp, fn

def get_nonbinary_spans(actions, SHIFT = 0, REDUCE = 1):
    spans = []
    stack = []
    pointer = 0
    binary_actions = []
    nonbinary_actions = []
    num_shift = 0
    num_reduce = 0
    for action in actions:
        # print(action, stack)
        if action == "SHIFT":
            nonbinary_actions.append(SHIFT)
            stack.append((pointer, pointer))
            pointer += 1
            binary_actions.append(SHIFT)
            num_shift += 1
        elif action[:3] == 'NT(':
            stack.append('(')                        
        elif action == "REDUCE":
            nonbinary_actions.append(REDUCE)
            right = stack.pop()
            left = right
            n = 1
            while stack[-1] is not '(':
                left = stack.pop()
                n += 1
            span = (left[0], right[1])
            if left[0] != right[1]:
                spans.append(span)
            stack.pop()
            stack.append(span)
            while n > 1:
                n -= 1
                binary_actions.append(REDUCE)                
                num_reduce += 1
        else:
            assert False    
    assert(len(stack) == 1)
    assert(num_shift == num_reduce + 1)
    return spans

def is_next_open_bracket(line, start_idx):
    for char in line[(start_idx + 1):]:
        if char == '(':
            return True
        elif char == ')':
            return False
    raise IndexError('Bracket possibly not balanced, open bracket not followed by closed bracket')        

def get_between_brackets(line, start_idx):
    output = []
    for char in line[(start_idx + 1):]:
        if char == ')':
            break
        assert not(char == '(')
        output.append(char)        
    return ''.join(output)

def get_tokens(line):
    output = []
    line_strip = line.rstrip()
    for i in range(len(line_strip)):
        if i == 0:
            assert line_strip[i] == '('        
        if line_strip[i] == '(' and not(is_next_open_bracket(line_strip, i)): # fulfilling this condition means this is a terminal symbol
            output.append(get_between_brackets(line_strip, i))
    output_tokens = []
    for terminal in output:
        terminal_split = terminal.split()
        assert len(terminal_split) == 2 # each terminal contains a POS tag and word                
        output_tokens.append(terminal_split[1])
    return output_tokens

def get_nonterminal(line, start_idx):
    assert line[start_idx] == '(' # make sure it's an open bracket
    output = []
    for char in line[(start_idx + 1):]:
        if char == ' ':
            break
        assert not(char == '(') and not(char == ')')
        output.append(char)
    return ''.join(output)

def get_actions(line):
    output_actions = []
    line_strip = line.rstrip()
    i = 0
    max_idx = (len(line_strip) - 1)
    while i <= max_idx:
        assert line_strip[i] == '(' or line_strip[i] == ')'
        if line_strip[i] == '(':
            if is_next_open_bracket(line_strip, i): # open non-terminal
                curr_NT = get_nonterminal(line_strip, i)
                output_actions.append('NT(' + curr_NT + ')')
                i += 1    
                while line_strip[i] != '(': # get the next open bracket, which may be a terminal or another non-terminal
                    i += 1
            else: # it's a terminal symbol
                output_actions.append('SHIFT')
                while line_strip[i] != ')':
                    i += 1
                i += 1
                while line_strip[i] != ')' and line_strip[i] != '(':
                    i += 1
        else:
            output_actions.append('REDUCE')
            if i == max_idx:
                break
            i += 1
            while line_strip[i] != ')' and line_strip[i] != '(':
                i += 1
    assert i == max_idx    
    return output_actions

def compute_f1(golds, preds, length_cutoff=150):
    corpus_f1 = [0., 0., 0.] 
    sent_f1 = [] 
    for (tree1, tree2) in zip(golds, preds):
        tree1 = tree1.strip()
        action1 = get_actions(tree1)
        sent1 = get_tokens(tree1)
        sent2 = get_tokens(tree2)
        assert len(sent1) == len(sent2)
        if len(sent1) > length_cutoff or len(sent1) == 1:
            continue
        gold_span1 = get_nonbinary_spans(action1)
        tree2 = tree2.strip()
        action2 = get_actions(tree2)
        gold_span2 = get_nonbinary_spans(action2)
        pred_span_set = set(gold_span2[:-1]) #the last span in the list is always the
        gold_span_set = set(gold_span1[:-1]) #trival sent-level span so we ignore it
        tp, fp, fn = get_stats(pred_span_set, gold_span_set) 
        corpus_f1[0] += tp
        corpus_f1[1] += fp
        corpus_f1[2] += fn
        overlap = pred_span_set.intersection(gold_span_set)
        prec = float(len(overlap)) / (len(pred_span_set) + 1e-8)
        reca = float(len(overlap)) / (len(gold_span_set) + 1e-8)
        if len(gold_span_set) == 0:
                reca = 1.
                if len(pred_span_set) == 0:                            
                        prec = 1.
        f1 = 2 * prec * reca / (prec + reca + 1e-8)
        sent_f1.append(f1)
    return sent_f1

def sentence_level_f1(ref, pred, round_it=True):
    count = len(ref)
    ref,pred = zip(*[(r, p) for r, p in zip(ref, pred) if p.strip()])
    if count > len(ref):
        print(count-len(ref), 'discarded!!')
    sent_f1 = compute_f1(ref, pred)
    f1 = np.mean(sent_f1) * 100
    if round_it:
        f1 = round(f1, 1)
    return f1

def simple_tag(tag):
    tag = tag.split('-')[0].split('=')[0]
    if tag.startswith('WH'):
        tag = tag[2:]
    return tag

def span2tag(tree_str):
    def recursive_parse(tokens, start=0, output=defaultdict(list), wordinx=0):
        while start < len(tokens):
            # print(tokens, start, wordinx, output)
            if tokens[start].startswith('('):
                tokens[start] = tokens[start][1:]
                output, end, end_wordinx = recursive_parse(tokens, start+1, output=output, wordinx=wordinx)
                output[(wordinx, end_wordinx)].append(tokens[start])
                wordinx = end_wordinx
                start = end
            elif tokens[start].endswith(')'):
                tokens[start] = tokens[start][:-1]
                return output, start, wordinx
            else:
                start += 1
                wordinx += 1
        return {k: w for k,w in output.items() if k[0]!=k[1]}
                    
    tokens = tree_str.strip().split()
    output = recursive_parse(tokens)
    return output

def constituency_label_recall(golds, preds, length_cutoff=150):
    gold_tags = defaultdict(lambda: 0)
    true_poss = defaultdict(lambda: 0)
    for k, (tree1, tree2) in enumerate(zip(golds, preds)):
        tree1 = tree1.strip()
        action1 = get_actions(tree1)
        sent1 = get_tokens(tree1)
        sent2 = get_tokens(tree2)
        assert len(sent1) == len(sent2)
        span2tags = span2tag(tree1)
        if len(sent1) > length_cutoff or len(sent1) == 1:
                continue
        gold_span1 = get_nonbinary_spans(action1)
        tree2 = tree2.strip()
        action2 = get_actions(tree2)
        gold_span2 = get_nonbinary_spans(action2)
        del span2tags[gold_span1[-1]]
        pred_span_set = set(gold_span2[:-1]) #the last span in the list is always the
        gold_span_set = set(gold_span1[:-1]) #trival sent-level span so we ignore it
        overlap = pred_span_set.intersection(gold_span_set)
        for tags in span2tags.values():
            for tag in tags:
                gold_tags[simple_tag(tag)] += 1
        for span in overlap:
            for tag in span2tags.get(span, []):
                true_poss[simple_tag(tag)] += 1
    recall = {tag: true_poss[tag]/gold_tags[tag] for tag in gold_tags}
    total = sum(gold_tags.values())
    coverage = {tag: gold_tags[tag]/total for tag in gold_tags}
    return recall, coverage