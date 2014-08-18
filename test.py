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

    def mymain():
        x, y = gen_new_random_shot()
        print "my turn : ", turn_count(), " my cord : ", x, y
        return x, y

    return mymain()
