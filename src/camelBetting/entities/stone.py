class Stone:

    def __init__(self, player: str, positive: bool):
        self.player = player
        if positive:
            self.value = 1
        else:
            self.value = -1
