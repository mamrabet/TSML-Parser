def events_to_str(events):
    return 'event ' + ', '.join(events) + ';'


def transitions_and_observers_to_str(transitions, observers):
    if observers:
        return transitions_to_str(transitions) + '\n' + observers_to_str(observers)
    else:
        return transitions_to_str(transitions)


def synchronizations_and_observers_to_str(synchronizations, observers):
    if observers:
        return synchronizations_to_str(synchronizations) + '\n' + observers_to_str(observers)
    else:
        return synchronizations_to_str(synchronizations)


def transitions_to_str(transitions):
    return list_to_lines('transition', transitions)


def synchronizations_to_str(synchronizations):
    return list_to_lines('synchronization', synchronizations)


def observers_to_str(observers):
    if observers:
        return list_to_lines('observer', observers)
    else:
        return ''


def list_to_lines(statement_type, elems):
    res = statement_type + '\n'

    for elem in elems:
        res += '\t' + str(elem) + ';\n'

    return res.strip('\n')


def merge_with(elems, symbol):
    res = ''
    for elem in elems:
        res += elem[0] + '.' + elem[1] + ' '+symbol+' '
    return res.strip(' '+symbol+' ')