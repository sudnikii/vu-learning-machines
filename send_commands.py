import sys


def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)


def make_move(action, rob):
    # actions
    actions = {
        "R": (5, 0),
        "SR": (10, 0),
        "C": (5, 5),
        "L": (0, 5),
        "SL": (0, 10)
    }

    rob_action = actions[action]
    rob.move(rob_action[0], rob_action[1], 2000)


def get_current_state(simulation, state_cat, irs, close_side, close_center, very_close):
    state = ''
    for i in range(len(irs)):
        if i == 0 or i == 2:
            close = close_side
        else:
            close = close_center

        if simulation:
            if state_cat == 'VCF':
                if irs[i] < very_close:
                    state += 'V'
                elif irs[i] < close:
                    state += "C"
                else:
                    state += "F"
            else:
                if irs[i] < close:
                    state += "C"
                else:
                    state += "F"
        else:
            if state_cat == 'VCF':
                if irs[i] > very_close:
                    state += 'V'
                elif irs[i] > close:
                    state += "C"
                else:
                    state += "F"
            else:
                if irs[i] > close:
                    state += "C"
                else:
                    state += "F"

    return state


def stop(irs, collision):
    for irs_value in irs:
        if irs_value < collision:
            return True


