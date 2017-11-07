def t_satisfy_b(t_label, b_label):
    """ decide whether label of ts_graph can satisfy label of buchi_graph
    """
    t_s_b = True
    # split label with ||
    b_label = b_label.split('||')
    for label in b_label:
        t_s_b = True
        #spit label with &&
        atomic_label = label.split('&&')
        for a in atomic_label:
            a = a.strip()
            if a == '1':
                continue
            # whether ! in an atomic proposition
            if '!' in a:
                for a_t in t_label:
                    if a[1:] == a_t:
                        t_s_b = False
                        break
            else:
                for a_t in t_label:
                    if a not in a_t:
                        t_s_b = False
                        break
    return t_s_b


print(t_satisfy_b(['r5, rb'],'rb'))