from ..HelpFunction import cosine_similarity_fmid, count_sum_product
from ..ABCKNN import KNN

class LSHSigMatrix(KNN):
    def __init__(self, hash_function, arguments):
        self.arguments = arguments
        self.data = hash_function.get_preprocess_data()
        self.data_len = len(self.data.get_new_id_data())
        self.hash_function = hash_function
        self.users_to_bucket()

    """ Hash users to bucket and create model."""
    def users_to_bucket(self):
        self.hash_function.create_model()

    """ Find k the nearest users to user in data model using hash function."""
    def find_k_users(self, user, k, max_ham_dist = 0):
        to_test_users = self.hash_function.hash_one_user(user = user, max_ham_dist=max_ham_dist)
        self.arguments["logp"].p("Number of users from bucket model: ", len(to_test_users), " / ",
                                     self.data_len, print_level=3)
        users = []
        for item in to_test_users:
            cosine = cosine_similarity_fmid(user, count_sum_product(user),
                                                                   self.data.get_new_id_data()[item],
                                                                   self.data.get_dict_users_id_data_sum()[item])
            in_item = []
            in_item.append(item)
            in_item.append(cosine)
            users.append(in_item)

        users.sort(key=lambda x: (x[1]), reverse=True)
        return users[:k]

    """ From k_users evaluate weight of items and recommend the top-n."""
    def fink_n_recommendation_from_near_users(self, user, k_users, n):
        items_and_weight = []
        items_and_index = {}
        index = 0
        for u in k_users:
            items = self.data.get_new_id_data()[u[0]]
            weight_of_user = u[1]
            for item in items:
                if item in user: continue
                if item not in items_and_index:
                    pair = [item, items[item] * weight_of_user]
                    items_and_weight.append(pair)
                    items_and_index[item] = index
                    index += 1
                else:
                    items_and_weight[items_and_index[item]][1] += items[item] * weight_of_user
        items_and_weight.sort(key=lambda x: (x[1]), reverse=True)
        return items_and_weight[:n]

    """ Return top-n recommendation, first find the k_nearest users."""
    def find_n_recommendation(self, user, k, n, max_ham_dist = 0):
        return self.fink_n_recommendation_from_near_users(user=user, n=n, k_users=self.find_k_users(user=user, k=k, max_ham_dist=max_ham_dist))
