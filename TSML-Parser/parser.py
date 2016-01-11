import re
from mc_path import McPath
from mc_model import McModel
from mc_block import McBlock
from mc_class import McClass
from mc_observer import McObserver
from mc_transition import McTransition
from mc_basic_block import McBasicBlock
from mc_internal_block import McInternalBlock
from mc_synchronization import McSynchronization
from tsml_error import TSMLerror


def parse(model_file_path):
    raw_model = get_file_content_as_unique_line(model_file_path)

    try:
        classes, blocks = split_blocks_and_classes(raw_model)
        return McModel(classes, blocks)
    except TSMLerror as details:
        print('TSML error: ' + str(details))


def split_blocks_and_classes(raw_content):
    blocks = []
    classes = []
    content = ''
    imbrications = 0

    for index, token in enumerate(raw_content.split(' ')):
        if token == 'class' or token == 'block':
            imbrications += 1
        elif token == 'end':
            imbrications -= 1
        if imbrications == 0:
            if content.startswith('class'):
                classes.append(read_class(content))
            elif content.startswith('block'):
                blocks.append(read_block(content))
            content = ''
        else:
            content += token + ' '

    return classes, blocks


def read_block(raw_block):
    (name, temp, internal_block) = read_model_element('block', raw_block)

    return McBlock(name, internal_block)


def read_class(raw_class):
    (name, basic_block, temp) = read_model_element('class', raw_class)

    return McClass(name, basic_block)


def read_model_element(model_type, raw_block_or_class):
    regex = model_type + r" (\w+)\s?(.*)"

    (name, raw_inner_block) = re.match(regex, raw_block_or_class).groups()
    basic_block = read_basic_block(raw_inner_block)

    if basic_block is None:
        internal_block = read_internal_block(raw_inner_block)
    else:
        internal_block = None

    return name, basic_block, internal_block


def read_basic_block(raw_basic_block):
    if raw_basic_block.startswith('state'):
        temp, new_raw_basic_block = slice_at('state', raw_basic_block)
        raw_states, temp = slice_at('event', new_raw_basic_block)
        raw_events, temp = slice_at('transition', temp)

        if contains('observer', temp):
            raw_transitions, raw_observers = slice_at('observer', temp)
            observers = read_observers(raw_observers)
        else:
            raw_transitions = temp
            observers = []

        states = tokenize(raw_states)
        events = tokenize(raw_events)
        transitions = read_transitions(raw_transitions)

        if states or events or transitions or observers:
            try:
                return McBasicBlock(states, events, transitions, observers)
            except TSMLerror as details:
                print('TSML error: ' + str(details) + ' in: "' + raw_basic_block + '"')

    return None


def read_internal_block(raw_internal_block):
    blocks, _ = split_blocks_and_classes(raw_internal_block)
    class_instances = read_class_instances(raw_internal_block)
    raw_internal_block = re.split(r"\bend\b", raw_internal_block)[-1]
    _, temp = slice_at('event', raw_internal_block)
    raw_events, raw_synchronizations = slice_at('synchronization', temp)
    events = tokenize(raw_events)

    parts = re.split(r"\bobserver\b", raw_synchronizations)

    if len(parts) == 2:
        raw_synchronizations = parts[0]
        observers = read_observers(parts[1])
    else:
        observers = []

    synchronizations = read_synchronizations(raw_synchronizations)

    return McInternalBlock(blocks, class_instances, events, synchronizations, observers)


def read_class_instances(raw_internal_block):
    class_instances = {}
    parts = raw_internal_block.split(';')

    for part in parts:
        if can_be_class_instances(part):
            results = re.match(r"(?:\s?end)?\s?(\w+)\s?([^;:\.]+)", part)

            if results:
                class_name = results.group(1)
                group = results.group(2)
                names = re.split(r",\s*", group)
                class_instances[class_name] = names

    return class_instances


def can_be_class_instances(part):
    for keyword in ['event', 'observer', 'synchronization', 'transition', 'block', 'class']:
        if contains(keyword, part):
            return False

    if re.search(':', part) or re.search('->', part):
        return False

    return True


def read_transitions(raw_transitions):
    transitions = []
    raw_transitions_list = re.split(';', raw_transitions)

    regex = r"\s?(\w+)\s?:\s?(\w+)\s?->\s?(\w+)"

    for raw_transition in raw_transitions_list:
        if re.search('->', raw_transition):
            event, start, arrival = re.match(regex, raw_transition).groups()
            transitions.append(McTransition(event, start, arrival))

    return transitions


def read_observers(raw_observers):
    observers = []
    raw_observers_list = re.split(';', raw_observers)
    regex = r"\s?(\w+)\s?:\s?(.+)?"

    for raw_observer in raw_observers_list:
        if re.search(':', raw_observer):
            (name, body) = re.match(regex, raw_observer).groups()
            observers.append(McObserver(name, body))

    return observers


def read_synchronizations(raw_synchronizations):
    temp = re.split(r";\s?", raw_synchronizations)
    temp.pop()

    synchronizations = []

    for raw_synchronization in temp:
        synchronizations.append(read_synchronization(raw_synchronization.strip('; ')))

    return synchronizations


def read_synchronization(raw_synchronization):
    if re.search(':', raw_synchronization):
        macro_name, temp = re.match(r"(\w+)\s?:\s?(.*)", raw_synchronization).groups()
        raw_paths = re.split(' & ', temp)
        paths = [read_path(raw_path) for raw_path in raw_paths]

        return McSynchronization(macro_name, paths)
    else:
        return McSynchronization(None, read_path(raw_synchronization))


def read_path(raw_path):
    parent, name = re.split('\.', raw_path)

    return McPath(parent, name)


def slice_at(keyword, string):
    return [elem.strip(' ') for elem in re.split(r"\b" + keyword + r"\b", string)]


def tokenize(string, separator=r",\s*", strip_with=";"):
    if strip_with is not None:
        string = string.strip(strip_with)

    return re.split(separator, string)


def contains(keyword, string):
    return re.search(r"\b" + keyword + r"\b", string)


def get_file_content_as_unique_line(path):
    with open(path, 'r') as file:
        content = file.read().strip(' \t\n\r')
        one_line_content = re.sub(r"(\n|\t|\r\n)", " ", content)
        one_line_with_single_whitespaces = ' '.join(one_line_content.split())

        return one_line_with_single_whitespaces
