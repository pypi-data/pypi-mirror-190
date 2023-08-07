from client import PlaygroundClient
import random, math
import json


# The following line are an example of how to use the API
class TestSnake(PlaygroundClient):
    def __init__(self, auth, endpoint="http://18.234.186.54:8083"):
        print(auth, endpoint)
        super().__init__(
            "snake",
            model_name="tic_tac_toe_robot" + str(random.randrange(100, 1000)),
            endpoint=endpoint,
            # auth = auth,
            max_exchange=50000,
        )

    def _parse_state(self, state_str):
        """Helper method to parse state string into something computer readable"""
        state_dict = json.loads(state_str)
        return tuple(state_dict["apple"]), [tuple(elem) for elem in state_dict["snake"]]

    def callback(self, state, reward):
        # TODO: Convert this state to JSON
        # Assume string is (apple_x, apple_y); [(snake_x, snake_y), ...]
        # Assume board size is even
        # Apply a basic strategy that will keep snake alive as long as
        # possible and eventually cover the whole board, ignoring the apple
        apple, snake = self._parse_state(state)
        head = snake[-1]

        SIZE = 10
        x, y = head
        if head == (SIZE - 1, SIZE - 2):
            return "S"

        if head == (0, SIZE - 1):
            return "N"

        if y == SIZE - 1:
            return "W"

        if x % 2 == 0:
            if y == 0:
                return "E"
            return "N"
        else:
            if y == SIZE - 2:
                return "E"
            return "S"

    def gameover_callback(self):
        pass


endpoint = "http://127.0.0.1:8083/"
auth = {"token": "brrrlin", "user_id": "sample_id", "api_key": "400"}
t = TestSnake(auth=auth, endpoint=endpoint)
t.run()
