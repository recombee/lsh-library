from bidict import bidict
import random, logging
from .DataClass import DataClass

class Preprocess:
    def __init__(self, arguments):
        self.arguments = arguments
        self.dict_make = False
        self.map_raw_user_item_with_value = {}
        self.bimap_user_id = bidict()
        self.bimap_item_id = bidict()
        self.data_counter = 0
        self.uid = 0
        self.iid = 0

    """ Call function for preprocesing data and creating data structures.
    Return Data class with preprocess base learn data and return testing data."""
    def preprocessing(self, min_items_for_user):
        if len(self.map_raw_user_item_with_value) == 0:
            self.arguments["logp"].printERROR("ERROR: No data load to preprocess.")
            exit(1)
        count_users = len(self.bimap_user_id)
        count_items = len(self.bimap_item_id)
        self.arguments["logp"].p("Count of users in data: ", count_users, print_level=1)
        self.arguments["logp"].p("Count of items in data: ", count_items, print_level=1)
        self.create_data_dict()
        self.count_weight_of_items()
        self.count_sum_product()
        self.split_data_random(size_of_test_set=self.arguments["size_of_test_set"], min_items_for_user=min_items_for_user)

        return DataClass(self.map_user_item_with_value, self.bimap_user_id, self.bimap_item_id,
                         self.idmap_user_item_with_value, self.map_item_with_weight_of_item, self.map_user_sum_product,
                         self.idmap_user_sum_product), self.map_raw_test_user_item_with_value, \
               self.idmap_raw_test_user_item_with_value


    def add_data(self, raw_data):
        for item in raw_data:
            if item[2] is None:
                continue
            if item[1] is None:
                continue
            if item[0] is None:
                continue
            if item[2] <= 0:
                continue
            # Create map<user, items<item, value>>.
            if item[0] not in self.map_raw_user_item_with_value:
                self.map_raw_user_item_with_value[item[0]] = {}
            if item[1] not in self.map_raw_user_item_with_value[item[0]]:
                self.map_raw_user_item_with_value[item[0]][item[1]] = 0
            self.map_raw_user_item_with_value[item[0]][item[1]] = min(
                self.map_raw_user_item_with_value[item[0]][item[1]] + float(item[2]), 1)
            # Create bimap for map user to user id. User is string id and user_id is int id.
            if item[0] not in self.bimap_user_id:
                self.bimap_user_id[item[0]] = self.uid
                self.uid += 1
            if item[1] not in self.bimap_item_id:
                self.bimap_item_id[item[1]] = self.iid
                self.iid += 1

    def get_count(self):
        self.data_counter = 0
        for i in self.map_raw_user_item_with_value:
            self.data_counter += len(self.map_raw_user_item_with_value[i])
        return self.data_counter

    """ Preprocess data from data to dictionary and create bidictionary with int id to string id from data."""
    def preprocess_raw_data_to_map(self):
        self.map_raw_user_item_with_value = {}
        self.bimap_user_id = bidict()
        self.bimap_item_id = bidict()
        uid = 0
        iid = 0
        for item in self.data:
            # Create map<user, items<item, value>>.
            if item[0] in self.map_raw_user_item_with_value:
                self.map_raw_user_item_with_value[item[0]][item[1]] = item[2]
            else:
                items = {item[1]: item[2]}
                self.map_raw_user_item_with_value[item[0]] = items
            # Create bimap for map user to user id. User is string id and user_id is int id.
            if item[0] not in self.bimap_user_id:
                self.bimap_user_id[item[0]] = uid
                uid += 1
            if item[1] not in self.bimap_item_id:
                self.bimap_item_id[item[1]] = iid
                iid += 1
        return len(self.bimap_user_id), len(self.bimap_item_id)

    """ Split data to base data and test data with size in percent from arguments."""
    def split_data_random(self, size_of_test_set, min_items_for_user):
        # Print good users.
        count_of_users = 0
        for user in self.map_raw_user_item_with_value:
            if len(self.map_raw_user_item_with_value[user]) >= min_items_for_user:
                count_of_users += 1
        self.arguments["logp"].p("Count of users with more than ", min_items_for_user-1,
                                " items is: ", count_of_users, print_level=1)
        sum_of_items_over_user = 0

        # If min items for user is defined gen random permutation and check users with more than specific items.
        size_of_test_set = int(len(self.map_raw_user_item_with_value) * size_of_test_set * 1 / 100)
        if size_of_test_set < 1:
            size_of_test_set = 1
        if min_items_for_user <= 1:
            random_users, random_users_id = self.get_random_n_users(size_of_test_set, self.bimap_user_id)
        else:
            random_users = []
            users_for_find, random_users_id = self.get_random_n_users(len(self.map_raw_user_item_with_value),
                                                                      self.bimap_user_id)
            for one_user in users_for_find:
                if len(self.map_raw_user_item_with_value[one_user]) >= min_items_for_user:
                    sum_of_items_over_user += len(self.map_raw_user_item_with_value[one_user])
                    random_users.append(one_user)
                if len(random_users) == size_of_test_set:
                    break
            if len(random_users) < size_of_test_set:
                self.arguments["logp"].printWARNING("There is not ", size_of_test_set,
                                               " users with count of item equal or higher then: ",
                                               min_items_for_user ,
                                               " in data. Size of test set will be: ", len(random_users))

        self.arguments["logp"].p("Average items on one user in test sample is: ",
                                format(sum_of_items_over_user / len(random_users), '.1f'), print_level=1)

        self.map_raw_test_user_item_with_value = {}
        self.idmap_raw_test_user_item_with_value = {}
        for i in random_users:
            self.map_raw_test_user_item_with_value[i] = self.map_raw_user_item_with_value[i]
            self.idmap_raw_test_user_item_with_value[self.bimap_user_id[i]] = self.idmap_user_item_with_value[self.bimap_user_id[i]]
            del self.idmap_user_item_with_value[self.bimap_user_id[i]]
            del self.map_user_item_with_value[i]

    """ Create data dictionary, item with user dictionary, and id dictionary."""
    def create_data_dict(self):
        self.map_item_user_with_value = {}
        self.map_user_item_with_value = {}
        self.idmap_user_item_with_value = {}
        for user in self.map_raw_user_item_with_value:
            for item in self.map_raw_user_item_with_value[user]:
                value = self.map_raw_user_item_with_value[user][item]

                # Create map<item, users<user, value>>.
                if item in self.map_item_user_with_value:
                    self.map_item_user_with_value[item][user] = value
                else:
                    items = {user: value}
                    self.map_item_user_with_value[item] = items

                # Create map<user, items<item, value>>.
                if user in self.map_user_item_with_value:
                    self.map_user_item_with_value[user][item] = value
                else:
                    items = {item: value}
                    self.map_user_item_with_value[user] = items

                # Create map<user_id, items<item_id, value>> new data for LSH.
                if self.bimap_user_id[user] in self.idmap_user_item_with_value:
                    self.idmap_user_item_with_value[self.bimap_user_id[user]][self.bimap_item_id[item]] = value
                else:
                    items = {self.bimap_item_id[item]: value}
                    self.idmap_user_item_with_value[self.bimap_user_id[user]] = items
        self.dict_make = True

    """ Returns list of random n users from data and list of cteated user_id."""
    @staticmethod
    def get_random_n_users(n, bimap_user_id):
        if n > len(bimap_user_id):
            logging.error("ERROR: To many wanted users. Data have only: " + str(len(bimap_user_id)))
            print("ERROR: To many wanted users. Data have only: ", len(bimap_user_id))
            exit(1)
        users = []
        users_id = random.sample(range(0, len(bimap_user_id)), n)
        for number in users_id:
            users.append(bimap_user_id.inv[number])
        return users, users_id

    """ Count sqrt(sums**2) of vectors for cosine similarity."""
    def count_sum_product(self):
        if not self.dict_make:
            self.arguments["logp"].printERROR("ERROR: Dictionary not create -> create_dictionaries()")
            exit(1)
        self.map_user_sum_product = {}
        self.idmap_user_sum_product = {}
        for user in self.map_user_item_with_value:
            values = self.map_user_item_with_value[user]
            value = 0
            for item in values:
                value = value + (values[item] ** 2)
            self.map_user_sum_product[user] = (value ** 0.5)
            self.idmap_user_sum_product[self.bimap_user_id[user]] = (value ** 0.5)

    """ Count the value of items as sum of column item."""
    def count_weight_of_items(self):
        if not self.dict_make:
            self.arguments["logp"].printERROR("ERROR: Dictionary not create -> create_dictionaries()")
            exit(1)
        # Map of sum of weights matrix. Its sum of weight of item of all users.
        self.map_item_with_weight_of_item = {}
        for item in self.map_item_user_with_value:
            weight = 0.0
            for user_item in self.map_item_user_with_value[item]:
                weight += self.map_item_user_with_value[item][user_item]
            self.map_item_with_weight_of_item[item] = weight




