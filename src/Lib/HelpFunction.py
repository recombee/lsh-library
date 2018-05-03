import time, logging
import numpy as np

def start_stopwatch():
    return time.time()

def stop_stopwatch(start):
    return time.time()-start

""" Dot two vectors save as two list in Python"""
def dot_and_sum(first, second):
    result = 0.0
    for item in first:
        if item in second:
            result += first[item] * second[item]
    return result

""" Check length of sparse vector and dot shorter with longer for speed up."""
def dot_sparse_vectors(first,second):
    if len(first) < len(second):
        result = dot_and_sum(first,second)
    else:
        result = dot_and_sum(second, first)
    return result;

""" Compute cosine similarity for two given vectors in data.
data -> map<user, items<item,value>
user1 and user2 is some users from data
sum_product is map<user, sum_product> precomputed sqrt(sum(xi^2))"""
def cosine_similarity_fmid(user, sum_a, user_2, sum_b):
    dot_ab = dot_sparse_vectors(user,user_2)

    # cosine angle between vectors
    cosine = dot_ab / sum_a / sum_b

    return cosine


"""Check precision of userKNN test on six decimal. Penalize every miss value from top k."""
def check_precision_user_knn(reference_list, check_list):
    yes = 0
    first_pointer = 0
    second_pointer = 0
    for i in range(len(check_list)):
        try:
            np.testing.assert_array_almost_equal(reference_list[first_pointer][1], check_list[second_pointer][1],
                                                 decimal=6)
        except:
            if reference_list[first_pointer][1] < check_list[second_pointer][1]:
                logging.error("It did not happen but it happened. KNN accuracy check error.")
                print("It did not happen but it happened. KNN accuracy check error.")
                exit(1)
            first_pointer += 1
            continue
        yes += 1
        first_pointer += 1
        second_pointer += 1
    while second_pointer < len(check_list):
        second_pointer += 1
    return yes / len(check_list)

"""Class for saving time of run and get average time of run."""
class AverageTimeChecker:
    def __init__(self):
        self.sum_of_time = 0
        self.count = 0

    """ Save one time event."""
    def save_time(self, time):
        self.sum_of_time += time
        self.count += 1

    """ Get average from time events."""
    def get_average_time(self):
        return self.sum_of_time / self.count

"""Count sqrt of one vector in cosine similarity."""
def count_sum_product(user):
    value = 0
    for item in user:
        value += (user[item] ** 2)
    return (value ** 0.5)
