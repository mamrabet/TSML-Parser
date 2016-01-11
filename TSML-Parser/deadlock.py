from string_conversions import merge_with

def print_deadlock_states(synchronized_class):
    states = detect_deadlock_states(synchronized_class)

    if states:
        print('Deadlocks found for the following states:')

        for state in states:
            print('\t' + merge_with(state, '&'))
    else:
        print('No deadlocks found')


def detect_deadlock_states(synchronized_class):
    deadlock_states = []

    for state in synchronized_class.states:
        deadlock_found = True

        for transition in synchronized_class.transitions:
            if transition.start == state:
                deadlock_found = False
                break

        if deadlock_found:
            deadlock_states.append(state)

    return deadlock_states
