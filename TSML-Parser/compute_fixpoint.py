import copy
from mc_class import McClass
from mc_transition import McTransition
from mc_basic_block import McBasicBlock


def compute_fixpoint(model):
    blocks = copy.copy(model.blocks)

    while copy.copy(len(blocks)) != 0:
        for i in range(len(copy.copy(blocks))):
            existing_class_name = []
            for classe in blocks[i].class_instances:
                existing_class_name.append(copy.copy(classe.name))
            feasible_block = True
            for class_instance in blocks[i].blocks:
                if not (class_instance.name in existing_class_name):
                    feasible_block = False
            if feasible_block:
                model.classes.append(copy.copy(compute_fixpoint_for_one_block(blocks[i], blocks[i].name)))
                del blocks[i]

    return model.classes[-1]


def compute_fixpoint_for_one_block(blocks, block_name):
    states = []
    transitions = []
    temp = []
    all_states = []
    candidates = []

    # Création de l'ensemble des états possibles (pas nécessairement accessibles)
    for class_instance in blocks.class_instances:
        # Création d'un premier état (le permier état de toutes les classes_instances)
        temp.append([copy.copy(class_instance.identifier), copy.copy(class_instance.states[0])])

    all_states.append(copy.copy(temp))
    temp = []

    for i in copy.copy(range(len(blocks.class_instances))):
        for j in copy.copy(range(len(all_states))):
            for k in copy.copy(range(1, len(blocks.class_instances[i].states))):
                mini_state = copy.copy(all_states[j])
                mini_state[i] = copy.copy([blocks.class_instances[i].identifier, blocks.class_instances[i].states[k]])
                all_states.append(copy.copy(mini_state))

    # Calcul des états accessibles
    candidates.append(copy.copy(all_states[0]))
    while len(candidates) != 0:
        start = copy.copy(candidates[0])
        candidates = copy.copy(candidates[1:])
        states.append(copy.copy(start))
        for synchronization in blocks.synchronizations:
            under_state_start = []
            under_state_arrival = []
            if synchronization.name is None:
                event_path = copy.copy(synchronization.event_paths)
                for transition in event_path.parent.transitions:
                    if transition.event == event_path.name:
                        associated_start = copy.copy(transition.start)
                        associated_arrival = copy.copy(transition.arrival)
                        associated_event = copy.copy(str(synchronization.event_path))
                under_state_start.append([copy.copy(event_path.parent.identifier), copy.copy(associated_start)])
                under_state_arrival.append([copy.copy(event_path.parent.identifier), copy.copy(associated_arrival)])
            else:
                for event_path in synchronization.event_paths:
                    for transition in event_path.parent.transitions:
                        if transition.event == event_path.name:
                            associated_start = copy.copy(transition.start)
                            associated_arrival = copy.copy(transition.arrival)
                    under_state_start.append([copy.copy(event_path.parent.identifier), copy.copy(associated_start)])
                    under_state_arrival.append([copy.copy(event_path.parent.identifier), copy.copy(associated_arrival)])

            transition_possible = True
            for under_state_start_sub_state in under_state_start:
                if under_state_start_sub_state in start:
                    temp = []
                else:
                    transition_possible = False
            if transition_possible:
                arrival = copy.copy(start)
                for i in copy.copy(range(len(start))):
                    for j in copy.copy(range(len(under_state_start))):
                        if under_state_start[j] == start[i]:
                            arrival[i] = copy.copy(under_state_arrival[j])
                if synchronization.name is None:
                    associated_event = copy.copy(associated_event)
                else:
                    associated_event = copy.copy(synchronization.name)
                transitions.append(McTransition(copy.copy(associated_event), copy.copy(start), copy.copy(arrival)))
                arrival_in_states = False
                for state in states:
                    if arrival == state:
                        arrival_in_states = True
                arrival_in_candidates = False
                for candidate in candidates:
                    if arrival == candidate:
                        arrival_in_candidates = True
                if (not arrival_in_states) and (not arrival_in_candidates):
                    candidates.append(copy.copy(arrival))

    return McClass(block_name, McBasicBlock(states, blocks.events, transitions, []))


