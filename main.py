class TuringMachine:

    def __init__(self, states, transitions, start_state, accept_states, reject_states):
        self.states = states
        self.transitions = transitions  # (state, symbol t1, symbol t2) : (state, symbol t1, symbol t2, move t1, move t2)
        self.current_state = start_state
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.blank = '_'
        self.tape1 = None
        self.tape2 = None
        self.head_position_t1 = None
        self.head_position_t2 = None

    def move_head(self, tape, head_position, move_dir):
        if move_dir == '>':
            head_position += 1
            if head_position == len(tape):  # if needed, extend array
                tape.append(self.blank)
        elif move_dir == '<':
            head_position -= 1
            if head_position < 0:  # if needed, extend array
                tape.insert(0, self.blank)
        elif move_dir == '-':
            pass  # do not move head
        return head_position

    def step(self):

        print(f'Tape 1: {self.tape1}')
        print(f'Head position: {self.head_position_t1}')
        print(f'Tape 2: {self.tape2}')
        print(f'Head position: {self.head_position_t2}')

        current_symbol_t1 = self.tape1[self.head_position_t1]
        current_symbol_t2 = self.tape2[self.head_position_t2]

        # if a transition exists for the current configuration
        if (self.current_state, current_symbol_t1, current_symbol_t2) in self.transitions:

            new_state, new_symbol_t1, new_symbol_t2, move_dir_t1, move_dir_t2 = self.transitions[(self.current_state, current_symbol_t1, current_symbol_t2)]

            self.tape1[self.head_position_t1] = new_symbol_t1
            self.tape2[self.head_position_t2] = new_symbol_t2

            print(f'\n(\'{self.current_state}\', \'{current_symbol_t1}\', \'{current_symbol_t2}\')'
                  f'\n{self.transitions[(self.current_state, current_symbol_t1, current_symbol_t2)]}\n')

            # move head on tape 1
            self.head_position_t1 = self.move_head(self.tape1, self.head_position_t1, move_dir_t1)

            # move head on tape 2
            self.head_position_t2 = self.move_head(self.tape2, self.head_position_t2, move_dir_t2)

            self.current_state = new_state

        # if no transition exists for the current configuration, reject
        else:
            self.current_state = self.reject_states[0]

    def run(self, input_str):
        self.tape1 = [self.blank] + list(input_str)
        self.tape2 = [self.blank] * 2

        # start both heads with exactly one blank space to the left
        self.head_position_t1 = 1
        self.head_position_t2 = 1

        while self.current_state not in self.accept_states and self.current_state not in self.reject_states:
            self.step()
        return self.current_state in self.accept_states


def run_machine(machine):
    in_str = input('Input: ')
    res = machine.run(in_str)
    if res:
        print(f'Input \'{in_str}\' was ACCEPTED')
    else:
        print(f'Input \'{in_str}\' was REJECTED')


if __name__ == "__main__":

    states_ = {'qCopy', 'qReturn', 'qSearch', 'qAccept', 'qReject'}
    transitions_ = {
        ('qCopy', '0', '_'): ('qCopy', '_', '0', '>', '>'),
        ('qCopy', '1', '_'): ('qCopy', '_', '1', '>', '>'),
        ('qCopy', '#', '_'): ('qReturn', '_', '#', '-', '<'),
        ('qReturn', '_', '0'): ('qReturn', '_', '0', '-', '<'),
        ('qReturn', '_', '1'): ('qReturn', '_', '1', '-', '<'),
        ('qReturn', '_', '_'): ('qSearch', '_', '_', '>', '>'),
        ('qSearch', '0', '0'): ('qSearch', '0', '0', '>', '>'),
        ('qSearch', '1', '1'): ('qSearch', '1', '1', '>', '>'),
        ('qSearch', '1', '0'): ('qSearch', '1', '0', '>', '-'),
        ('qSearch', '0', '1'): ('qSearch', '0', '1', '>', '-'),
        ('qSearch', '0', '#'): ('qAccept', '0', '#', '-', '-'),
        ('qSearch', '1', '#'): ('qAccept', '1', '#', '-', '-'),
        ('qSearch', '_', '#'): ('qAccept', '_', '#', '-', '-')
    }
    start_state_ = 'qCopy'
    accept_states_ = {'qAccept'}
    reject_states_ = ['qReject']

    tm = TuringMachine(states_, transitions_, start_state_, accept_states_, reject_states_)

    run_machine(tm)
