import numpy as np
import copy, logging
from bitstring import BitArray

""" Hash function implement as random matrix. Bucket dimension specific number of buckets in model."""
class SimpleRandomHashFunction:
    def __init__(self, data_dimension, bucket_dimension, min_value=-1, max_value=1, need_int = False):
        self.create_model = False
        self.bucket_dimension = bucket_dimension
        if need_int == True:
            self.random_projection = np.random.randint(min_value,max_value+1, (bucket_dimension, data_dimension))
        else:
            self.random_projection = np.random.uniform(min_value, max_value, (bucket_dimension, data_dimension))

    """ Change matrix with maparmetr alfa using weight of item in dataset. Value = value * weight ^ alfa.
    Bimap is maping items to their int id."""
    def alfa_change_matrix(self, alfa, weight_of_items, bimap_item_id):
        for item in weight_of_items:
            for i in range(len(self.random_projection)):
                self.random_projection[i][bimap_item_id[item]] *= ((weight_of_items[item]) ** alfa)

    """ Hash data to buckets using created hash function."""
    def hash_data_in_buckets(self, idmap_user_item_with_value):
        self.buckets = {}
        for item in idmap_user_item_with_value:
            if len(self.random_projection) == 0:
                if 0 not in self.buckets:
                    value = []
                    value.append(item)
                    self.buckets[0] = value
                else:
                    self.buckets[0].append(item)
            else:
                hash_vector = self.hash_one_vector(self.random_projection, idmap_user_item_with_value[item])
                bucket_number = self.binary_list_to_number(hash_vector)
                if bucket_number not in self.buckets:
                    value = [item]
                    self.buckets[bucket_number] = value
                else:
                    self.buckets[bucket_number].append(item)
        self.create_model = True

    """ Return bucket model. Buckets -> Map<bucket_number, List<users>>."""
    def get_buckets(self):
        return self.buckets

    """ Convert binary list to number."""
    def binary_list_to_number(self, binary_list):
        b = BitArray(binary_list)
        return b.uint

    """ Sum of dot two vectors."""
    def sum_dot_vector_to_sparse_vector(self, normal_vector, sparse_vector):
        sum = 0.0
        for item in sparse_vector:
            sum += normal_vector[item] * sparse_vector[item]
        return sum

    """ Hash one vector by random_projection hash function."""
    def hash_one_vector(self, random_projection, one_vector):
        hash_vector = []
        for random in random_projection:
            dot_prod = self.sum_dot_vector_to_sparse_vector(random, one_vector)
            if dot_prod > 0:
                hash_vector.append(1)
            else:
                hash_vector.append(0)
        return hash_vector

    """ Hash one user to bucket and return possible users.
    Max_ham_dist parametr witch buckets include to possibles. (Size of neighborhood)
    0 is only one buckets where is user. 1 is user buckets and buckets on 1 haming distance.
    TO DO: Is hamming dist best fo near buckets?
    TO DO: There is big problem when you have many buckets (2^20) and finding neighborhood bigger than 1, but the one is the best."""
    def hash_user_in_buckets(self, user, max_ham_dist, buckets_map):
        if not self.create_model:
            logging.error("ERROR: Not created model cant return users.")
            print ("ERROR: Not created model cant return users.")
            exit(1)
        hash_vector = self.hash_one_vector(self.random_projection, user)
        bucket_number = self.binary_list_to_number(hash_vector)
        if self.bucket_dimension > 10:
            if max_ham_dist > 2:
                possible_buckets = self.gen_near_buckets2(max_ham_dist=max_ham_dist, to_compare=bucket_number)
            else:
                possible_buckets = self.gen_near_buckets(buckets_map, max_ham_dist, bucket_number)
        else:
            if max_ham_dist > 1:
                possible_buckets = self.gen_near_buckets2(max_ham_dist=max_ham_dist, to_compare=bucket_number)
            else:
                possible_buckets = self.gen_near_buckets(buckets_map, max_ham_dist, bucket_number)
        users = []
        for i in possible_buckets:
            if i not in self.buckets:
                continue
            users = [*users, *self.buckets[i]]
        return users

    """ Function return near buckets to one specific.
    This is very fast for small hamming distance. For example < 3."""
    def gen_near_buckets(self, buckets_map, max_hamming_dist, to_compare_bucket):
        good_buckets = {}
        good_buckets[to_compare_bucket] = True
        queue = copy.deepcopy(buckets_map[to_compare_bucket])
        queue.append(-1)
        while (len(queue) > 0):
            piece = queue.pop(0)
            if piece == -1:
                max_hamming_dist -= 1
                if len(queue) == 0:
                    break
                queue.append(-1)
                continue
            if max_hamming_dist > 0:
                good_buckets[piece] = True
                to_add = buckets_map[piece]
                for i in to_add:
                    if i not in good_buckets:
                        queue.append(i)
        return good_buckets

    """ Function return near buckets to one specific.
    This is faster for big hamming distance. For example > 2."""
    def gen_near_buckets2(self, max_ham_dist, to_compare):
        numbers = []
        for i in range(0, 2 ** self.bucket_dimension):
            if bin(i ^ to_compare).count('1') <= max_ham_dist:
                numbers.append(i)
        return numbers