from .SimpleRandomMatrixHash import SimpleRandomHashFunction
from .SimpleRandomMatrixHash import np
from bitstring import BitArray

""" Class for holding more hash function and return user from it."""
class HashFunction:
    def __init__(self, data, bucket_dimension, arguments, histograms):
        self.histograms = histograms
        self.arguments=arguments
        self.data = data
        self.bucket_dimension = bucket_dimension
        self.buckets_map = {}
        self.hash_function = []
        for i in range(2**bucket_dimension):
            self.buckets_map[i] = self.generate_one_step_near_bucket(np.binary_repr(i, bucket_dimension))

    """ Return preprocess data."""
    def get_preprocess_data(self):
        return self.data

    """ Generated for each bucket one step neighbours."""
    def generate_one_step_near_bucket(self, bin_number_list):
        neighbours = []
        step = 0
        for i in bin_number_list:
            to_return = ""
            to_return += bin_number_list[0:step]
            if i == "0":
                to_return += "1"
            else:
                to_return += "0"
            to_return += bin_number_list[step + 1:self.bucket_dimension]
            step += 1
            neighbours.append(BitArray(bin=to_return).uint)

        return neighbours

    """ Create list of hash function using parametrs."""
    def create_hash_functions(self, number_of_hash_function):
        for matrix in range(number_of_hash_function):
            self.hash_function.append(SimpleRandomHashFunction(bucket_dimension=self.bucket_dimension,
                                                               data_dimension=len(self.data.get_item_id_dict()),
                                                               min_value=-1, max_value=+1))

    """ Create list of hash function, specific in argument line as -m."""
    def create_hash_function_from_argumnets(self, list_of_hash_function):
        for hash_fucn in list_of_hash_function:
            if len(hash_fucn) == 0:
                self.create_hash_functions(1)
            elif len(hash_fucn) == 1:
                hash = SimpleRandomHashFunction(bucket_dimension=self.bucket_dimension,
                                         data_dimension=len(self.data.get_item_id_dict()),
                                         min_value=-1, max_value=+1)
                hash.alfa_change_matrix(alfa=hash_fucn["alfa"],
                                        weight_of_items=self.data.get_weight_of_items(),
                                        bimap_item_id=self.data.get_item_id_dict())
                self.hash_function.append(hash)
            elif len(hash_fucn) == 2:
                self.hash_function.append(SimpleRandomHashFunction(bucket_dimension=self.bucket_dimension,
                                                                   data_dimension=len(self.data.get_item_id_dict()),
                                                                   min_value=hash_fucn["min"], max_value=hash_fucn["max"]))
            elif len(hash_fucn) == 3:
                hash = SimpleRandomHashFunction(bucket_dimension=self.bucket_dimension,
                                         data_dimension=len(self.data.get_item_id_dict()),
                                         min_value=hash_fucn["min"], max_value=hash_fucn["max"])
                hash.alfa_change_matrix(alfa=hash_fucn["alfa"],
                                        weight_of_items=self.data.get_weight_of_items(),
                                        bimap_item_id=self.data.get_item_id_dict())
                self.hash_function.append(hash)
            else:
                self.arguments["logp"].printERROR("ERROR: Some went wront in creating hash functions from arguments.")
                exit(1)

    """ Create model using all hash function and hash data."""
    def create_model(self):
        for i in self.hash_function:
            i.hash_data_in_buckets(self.data.get_new_id_data())
        if self.arguments["hist"]:
            self.print_statistic_of_bucket_to_csv()

    """ Hash one user using all hash function and return possible users to computing cosine similarity."""
    def hash_one_user(self, user, max_ham_dist):
        if len(self.hash_function) == 0:
            self.arguments["logp"].printERROR("ERROR: No hash function created. No model.")
            exit(1)
        brut_vector = []
        for i in self.hash_function:
            users = i.hash_user_in_buckets(user, max_ham_dist, self.buckets_map)
            brut_vector = [*brut_vector, *users]
        brut_vector = np.unique(brut_vector)
        return brut_vector


    """ Print statistic of number of users in buckets.
     Methos also calculate the average weight of item in normalized between 0 and 1"""
    def print_statistic_of_bucket_to_csv(self):
        weight_max = 0
        weights_items = self.data.get_weight_of_items()
        item_id = self.data.get_item_id_dict()
        # Find the max value of weights for finding maximum.
        for i in weights_items:
            if weight_max < weights_items[i]:
                weight_max = weights_items[i]


        anumber_of_hash_func = 0
        # Histogram model print for each hash function.
        for hash in self.hash_function:
            try:
                hist_file = open(self.histograms + str(anumber_of_hash_func) + ".csv", "w")
            except:
                self.arguments["logp"].printERROR("Cant not create output hist file:",
                                                  self.histograms + str(anumber_of_hash_func) + ".csv")

            to_save_map = {}
            max = 0
            min = weight_max
            for i in hash.get_buckets():
                one_line = []
                one_line.append(str(i))
                one_line.append(str((len(hash.get_buckets()[i])/len(self.data.get_new_id_data()))*100))
                sum_in_bucket = 0
                counts = 0
                for user in hash.get_buckets()[i]:
                    for item in self.data.get_new_id_data()[user]:
                        sum_in_bucket += weights_items[item_id.inv[item]]
                        counts += 1
                if max < (sum_in_bucket/counts):
                    max = sum_in_bucket/counts
                if min > (sum_in_bucket/counts):
                    min = sum_in_bucket/counts
                one_line.append(sum_in_bucket/counts)
                to_save_map[i] = one_line

            for line in to_save_map:
                hist_file.write(str(to_save_map[line][0]))
                hist_file.write(",")
                hist_file.write(str(to_save_map[line][1]))
                hist_file.write(",")
                # Min max normalization average weight in bucket.
                hist_file.write(str((to_save_map[line][2]-min)/(max-min)))
                hist_file.write("\n")
            hist_file.close()
            anumber_of_hash_func += 1



