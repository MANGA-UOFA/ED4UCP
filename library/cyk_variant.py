def cyk_variant(span_scores, length):
    scores = [[0]*length]
    spans = [[[]]*length]
    for level in range(1, length):
        scores.append([])
        spans.append([])
        for begin in range(length-level):
            end = begin+level
            this_span = str((begin, end))
            span_score = span_scores.get(this_span, 0)
            left, best_sub_score = max(([(left, scores[left][begin]+scores[level-left-1][begin+left+1]) for left in range(level)]), key=lambda x: x[1])
            score = span_score + best_sub_score
            new_spans = spans[left][begin] + spans[level-left-1][begin+left+1] + [this_span]
            scores[level].append(score)
            spans[level].append(new_spans)
    return spans[-1][0]