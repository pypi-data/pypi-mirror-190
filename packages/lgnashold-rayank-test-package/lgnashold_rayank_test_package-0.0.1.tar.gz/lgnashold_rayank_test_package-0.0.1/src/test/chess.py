from ..client import PlaygroundClient
import random, math
import json
import attrs


# The following line are an example of how to use the API
class TestChess(PlaygroundClient):
    def __init__(self, endpoint="http://44.205.255.44:8083"):
        super().__init__(
            "chess",
            model_name="chessrobot" + str(random.randrange(100, 1000)),
            endpoint=endpoint,
            max_exchange=5000,
            game_type=2,
        )

    def callback(self, state, reward):
        state = json.loads(state)

        # TODO: Abstract serialization and deserialization
        if state['player_moving'] != self.user_id:
            return None

        print("FEN: ", state['fen'])
        print("Input Move (UCI format, e.g. a2a3): ")
        move_str = input()
        action = {
            'uci': move_str
        }
        return json.dumps(action)

    def gameover_callback(self):
        pass


endpoint = "http://127.0.0.1:8083/"
t = TestChess(endpoint=endpoint)
t.run()
