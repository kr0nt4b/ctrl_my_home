class NextMoment:

    def __init__(self, state, next_check, duration):
        self.state = state
        self.next_check = next_check
        self.duration = duration

    def state(self):
        return self.state

    def set_next_check(self, value):
        self.next_check = value

    def get_next_check(self):
        return self.next_check
