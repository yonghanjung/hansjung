import random


def guess(record):
    # EMPTY : 1 // NOT-empty : -1
    def check_empty(x, y):
        myboard = record.get_board()
        if myboard[x][y] != 0:
            return -1
        else:
            return 1

    def was_that_shot(x, y):
    # Check my last shot was hit or not
        mylatest = record.get_latest()
        if mylatest['result'] == 1:
            # That shot was hit!
            return 1
        elif mylatest['result'] == 0:
            # That shot missed
            return -1

    def my_last_shot():
        mylatest = record.get_latest()
        mycord = mylatest['guess']
        return mycord['x'], mycord['y']

    def turn_count():
        return len(record.get_history())

    # This function gives the random shot
    def gen_new_random_shot():
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if turn_count() == 0:
            return x, y

        else:
            if check_empty(x, y) == 1:
            # check_empty(x,y) == 1  <==> that place is empty
                return x, y
            elif check_empty(x, y) == -1:
            # check_empty(x,y) == -1  <==> that place is not empty
                return gen_new_random_shot()

    my_remember = record.data

    # initialized
    if turn_count == 0:
        # Initialization
        cand_dir = ['r', 'l', 'u', 'd']
        ship_cand = [2, 3, 3, 4, 5]
        hit_timing = 0
        x, y = gen_new_random_shot()
        start_loc = [0, 0]

        # update my_remember
        # only record for hit
        # Initialization
        my_remember.update(
            {turn_count(): [cand_dir, 'init', hit_timing, ship_cand, start_loc]})
        return x, y

    status = 'init'
    if len(my_remember) > 0:
        call_remember = my_remember[turn_count() - 1]
        status = call_remember[1]

    def init_rem(my_remember):
        # initialized
        status = "missed"
        cand_dir = ['r', 'l', 'u', 'd']
        ship_cand = call_remember[3]
        start_loc = call_remember[4]
        hit_timing = call_remember[2]
        my_remember.update(
            {turn_count(): [cand_dir, status, hit_timing, ship_cand, start_loc]})
        return my_remember

    # START ##################################################################
    if status == 'init':
        start_x, start_y = my_last_shot()
        if was_that_shot(start_x, start_y) == 1:
            cand_dir = ['r', 'l', 'u', 'd']
            status = "new_shot"
            start_loc = [start_x, start_y]
            cand_dir = call_remember[0]
            if start_x == 0:
                cand_dir.remove('l')
            elif start_y == 0:
                cand_dir.remove('d')
            elif start_x == 9:
                cand_dir.remove('r')
            elif start_y == 9:
                cand_dir.remove('u')
            hit_timing = turn_count() - 1
            direction = cand_dir[len(cand_dir) - 1]
            if direction == 'r':
                new_x = start_x + 1
                new_y = start_y
            elif direction == 'l':
                new_x = start_x - 1
                new_y = start_y
            elif direction == 'u':
                new_x = start_x
                new_y = start_y + 1
            elif direction == 'l':
                new_x = start_x
                new_y = start_y - 1

            my_remember.update(
                {turn_count(): [cand_dir, status, hit_timing, ship_cand, start_loc]})

            return new_x, new_y

        else:
            my_remember = init_rem(my_remember)
            x, y = gen_new_random_shot()
            return x, y

    elif status == 'missed':
        start_x, start_y = my_last_shot()
        if was_that_shot(start_x, start_y) == 1:
            status = "new_shot"
            start_loc = [start_x, start_y]
            cand_dir = call_remember[0]
            if start_x == 0:
                cand_dir.remove('l')
            elif start_y == 0:
                cand_dir.remove('d')
            elif start_x == 9:
                cand_dir.remove('r')
            elif start_y == 9:
                cand_dir.remove('u')
            hit_timing = turn_count() - 1
            direction = cand_dir[len(cand_dir) - 1]
            if direction == 'r':
                new_x = start_x + 1
                new_y = start_y
            elif direction == 'l':
                new_x = start_x - 1
                new_y = start_y
            elif direction == 'u':
                new_x = start_x
                new_y = start_y + 1
            elif direction == 'l':
                new_x = start_x
                new_y = start_y - 1

            my_remember.update(
                {turn_count(): [cand_dir, status, hit_timing, ship_cand, start_loc]})

            return new_x, new_y

        else:
            my_remember = init_rem(my_remember)
            x, y = gen_new_random_shot()
            return x, y
