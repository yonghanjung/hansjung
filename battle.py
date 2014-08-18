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

    def search_algorithm():

    # This function gives the random shot
    def gen_new_random_shot():
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        print "MY cand_cord: ", x, y
        if turn_count() == 0:
            return x, y

        else:
            if check_empty(x, y) == 1:
            # check_empty(x,y) == 1  <==> that place is empty
                return x, y
            elif check_empty(x, y) == -1:
            # check_empty(x,y) == -1  <==> that place is not empty
                return gen_new_random_shot()

    def mymain():
        my_remember = record.data
        if len(my_remember) > 0:
            call_remember = my_remember[turn_count() - 1]

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
        else:
            my_last_status = call_remember[1]
            # init / start / miss
            ship_last_cand = call_remember[3]
            # how many ships

            if my_last_status != 'start':
                # Cases
                # 1. turn count > 0 and my last status was 'miss'
                # 2. turn count > 0 and my last status was 'init'

                cand_dir = call_remember[0]
                # this should be reduced when the algorithm started

                if was_that_shot() == -1:
                    # if miss shot,
                    mystatus = "miss"
                    # I have to change mystatus to the miss
                    hit_last_timing = 0
                    search_start_loc = [0, 0]
                    x, y = gen_new_random_shot()
                    my_remember.update(
                        {turn_count(): [cand_dir, mystatus, hit_last_timing, ship_last_cand, search_start_loc]})
                    return x, y
                elif was_that_shot() == 1:
                    # if hit!, then I would have another chances.
                    # That is the case that I am given another chances.
                    # MY ATTACK BEGIN!
                    mystatus = "go"
                    # I changed my status to 'start', so that
                    # from next iter, it starts from 'start'
                    hit_last_timing = turn_count()
                    # I record my new time.
                    # It is okay to give turn_count because this is the case
                    # MY attack begin!
                    search_start_loc = my_last_shot()
                    # I record my last shot location.
                    x, y = search_algorithm(mydirection)
                    cand_dir.remove(mydirection)
                    my_remember.update(
                        {turn_count(): [cand_dir, mystatus, hit_last_timing, ship_last_cand, search_start_loc]})

                    return x, y

            elif my_last_status == 'go':
                # In the case that I just started my algorithm
                hit_last_timing = call_remember[2]

            # If finished, then mystatus should change to start

    return mymain()


'''
1. for-iteration works 

'''
