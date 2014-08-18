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

    # def search_algorithm():

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

    def search_algorithm(hit_x, hit_y, my_mode):
        if my_mode == 'first_hit':
            if hit_y != 9:
                return hit_x, hit_y + 1
            else:
                if hit_x != 9:
                    return hit_x + 1, hit_y
                else:
                    return hit_x, hit_y - 1

    def mymain():
        mydata = record.data

        def initial_mydata(x, y, my_mode):
            mydata.update({turn_count(): [my_mode, [x, y]]})
        if turn_count() == 0:
            x, y = gen_new_random_shot()
            initial_mydata(x, y, 'init')
            return x, y
        if turn_count() > 0:
            last_x, last_y = my_last_shot()
            if was_that_shot(last_x, last_y) == 1:
                x, y = search_algorithm(last_x, last_y, 'first_hit')
                mydata.update(
                    {turn_count(): ['first_hit', [last_x, last_y]]})
                if check_empty(x, y) == 1:
                    return x, y
                else:
                    x, y = gen_new_random_shot()
                    return x, y
            else:
                x, y = gen_new_random_shot()
                return x, y

    return mymain()
