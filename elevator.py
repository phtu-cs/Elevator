import sys
import threading
import time


class Elevator:
    def __init__(self):
        self.num_floors = 10 # total number of floors; default: 1-10
        self.log_name = "log.txt"
        file = open(self.log_name,"r+")
        file.truncate(0)
        file.close()

        self.quries = []
        '''queries sent by users e.g. {"button": to, "floor": 10} (to floor 10),
        {"button": down, "floor": 10} (some people on 10th floor what to go downstairs)
        {"button": up, "floor": 5} (some people on 5th floor what to go upstairs)
        quries is a priority queue, the front query is processed '''

        self.moving_direction = "up" # 3 cases: up down and stop; default: up
        self.curr_floor = 1 # initially, the elevator is on the 1st floor; default: 1st
        self.unit_move_time = 3 # time for the elevator to move 1-floor distance (second); default: 1
        self.door_open_time = 5 # lasting time for the opening door of elevator (second); default: 3

    def run(self):

        # multi-threading
        input_thread = threading.Thread(target=self.read_input)
        input_thread.daemon = True
        input_thread.start()

        while True:
            # elevator is operating which isn't blocked by user inputs
            self.move()

    def read_input(self):
        # read input from command line, if user inputs "where", it shows the position of the elevator

        self.intro()

        while True:
            a = input()
            b = a.split()

            if len(b) == 2:
                button = b[0]
                if not b[1].isnumeric():
                    self.raise_error()
                    continue
                else:
                    floor = int(b[1])

                if (button == "up" or button == "down" or button == "to") and (floor <= self.num_floors and floor >= 1):

                    if button == "up" and floor == self.num_floors:
                        self.raise_error()
                        continue
                    elif button == "down" and floor == 1:
                        self.raise_error()
                        continue

                    if button == "up":
                        message = "someone on " + str(floor) + " floor wants to go upstairs."
                    elif button == "down":
                        message = "someone on " + str(floor) + " floor wants to go downstairs."
                    elif button == "to":
                        message = "someone inside the elevator want to go to " + str(floor) + " floor."
                    else:
                        assert False
                    self._output_message(message)
                    self.insert_query(button, floor)
                else:
                    self.raise_error()

            elif len(b) == 1:
                if b[0] == "where":
                    message = "elevator is currently on " + str(self.curr_floor) + " floor."
                    self._output_message(message)
                else:
                    self.raise_error()
            else:
                self.raise_error()

    def insert_query(self, button: str, floor: int):

        ''' insert query based on queries' score() '''

        # invalid queries, because the elevator is already at the queried position
        if button == "to" and floor == self.curr_floor and self.moving_direction == "stop":
            # do nothing
            message = "Elevator won't move! It is already here!"
            self._output_message(message)
            return
        if button == self.moving_direction and floor == self.curr_floor:
            # do nothing
            return

        query = {"button": button, "floor": floor}

        insert_pos = 0
        for idx, q in enumerate(self.quries):
            insert_pos = idx
            if self.score(query) < self.score(q):
                break
            else:
                insert_pos = idx + 1

        self.quries.insert(insert_pos, query)

    def process_queries(self):
        '''process the front query'''
        if self.quries:
            q0 = self.quries.pop(0)
            assert q0["floor"] == self.curr_floor
            if q0["button"] != "to":
                self.moving_direction = q0["button"]

        while len(self.quries) != 0 and self.score(self.quries[0]) == 0:
            self.quries.pop(0)

    def process_queries_after_door_close(self):
        '''process the front query after the door is closed '''
        if self.quries:
            q0 = self.quries[0]
            if q0["floor"] == self.curr_floor:
                if q0["button"] != "to":
                    self.moving_direction = q0["button"]
                self.quries.pop(0)

    def move(self):
        if self.quries:
            des = int(self.quries[0]["floor"])
            if des < self.curr_floor:
                time.sleep(self.unit_move_time)
                self.curr_floor -= 1
                self.moving_direction = "down"
            elif des > self.curr_floor:
                time.sleep(self.unit_move_time)
                self.curr_floor += 1
                self.moving_direction = "up"
            elif des == self.curr_floor:
                self.process_queries()
                if not self.quries:
                    self.moving_direction = "stop"
                else:
                    if self.curr_floor == 1:
                        self.moving_direction = "up"
                    elif self.curr_floor == self.num_floors:
                        self.moving_direction = "down"

                self._open_door()
                self._enter_des()
                time.sleep(self.door_open_time)
                self._close_door()
                self.process_queries_after_door_close()

            self._moving_status()

    def score(self, query):

        ''' score considers both energy and time efficiency,
        we simulate elevators in common school/apartment building '''

        score = 0
        des_floor = query["floor"]
        button = query["button"]
        diff_floor = des_floor-self.curr_floor
        if self.moving_direction == "up":
            if diff_floor >= 0:
                if button == "up" or button == "to":
                    score = diff_floor
                elif button == "down":
                    score = diff_floor + 2*(self.num_floors-des_floor)
            elif diff_floor < 0:
                if button == "down" or button == "to":
                    score = abs(diff_floor) + 2*(self.num_floors-self.curr_floor)
                elif query["button"] == "up":
                    score = des_floor - 1 + (self.num_floors-self.curr_floor) + self.num_floors - 1

        elif self.moving_direction == "down":

            if diff_floor <= 0:
                if button == "down" or button == "to":
                    score = abs(diff_floor)
                elif button == "up":
                    score = (self.curr_floor-1) + (des_floor - 1)
            elif diff_floor > 0:
                if button == "up" or button == "to":
                    score = (self.curr_floor - 1) + des_floor - 1
                elif query["button"] == "down":
                    score = self.num_floors - 1 + self.num_floors-des_floor + self.curr_floor - 1
        elif self.moving_direction == "stop":
            score = abs(diff_floor)

        return score

    def intro(self):
        message = ("INPUT COMMAND EXAMPLE: \"to 10\" means pushing the button inside the elevator "
        "to the 10th floor; \"up 5\" means pushing the up button on the 5th floor outside the elevator; " 
        "\"down 4\" means pushing the down button on the 4th floor outside the elevator; "
        "\"where\" outputs the positon of the elevator")
        self._output_message(message)

    def _open_door(self):
        message = "Door opens, at " + str(self.curr_floor) + " floor."
        self._output_message(message)

    def _close_door(self):
        message = "Door closes, at " + str(self.curr_floor) + " floor"
        self._output_message(message)

    def _output_message(self,message):
        print(message)
        with open(self.log_name, 'a') as f:
            f.write(message + "\n")
            f.close()

    def _enter_des(self):
        message = "Please enter destination in " + str(self.door_open_time) +  "s: "
        self._output_message(message)

    def _moving_status(self):
        if self.moving_direction != "stop":
            message = "Elevator is going " + self.moving_direction + "," + " currently on " \
                      + str(self.curr_floor) + " floor."
        else:
            message = "Elevator stops," + " currently on " + str(self.curr_floor) + " floor"

        self._output_message(message)

    def raise_error(self):
        # when input is not in correct format
        print("Wrong format! Please input again! (e.g. \"down 9\", \"up 5\", \"to 4\") "
              "Note there is no \"down 1\" and \"up %d\"" % self.num_floors)


if __name__ == "__main__":
    e = Elevator()
    e.run()
