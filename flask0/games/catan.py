
class Game:
    def __init__(self, players, options=None):
        self.players = players
        self.turn = 0
        self.state = "setup"

    def serialize(self):
        return {"players": self.players, "turn": self.turn, "state": self.state}

    def deserialize(self, data):
        self.players = data["players"]
        self.turn = data["turn"]
        self.state = data["state"]

    def get_state(self):
        return {
            "state": self.serialize(),
            "possible_moves": ["roll_dice", "build_road", "end_turn"],
            "current_players": self.players,
        }

    def make_move(self, move):
        action = move.get("action")
        if action == "end_turn":
            self.turn = (self.turn + 1) % len(self.players)
        return self.get_state()
