from ..HelpFunction import cosine_similarity_fmid,count_sum_product
from ..ABCKNN import KNN

class UserKNN(KNN):
    def __init__(self, data):
        self.data = data

    """ Find k the nearest users to user in data model."""
    def find_k_users(self, user, k, max_ham_dist = 0):
        users = []
        for item in self.data.get_rawdata():
            if item == user:
                continue
            else:
                cosine = cosine_similarity_fmid(user, count_sum_product(user),
                                                               self.data.get_rawdata()[item],
                                                               self.data.get_dict_users_sum_product()[item])
                in_item = []
                in_item.append(item)
                in_item.append(cosine)
                users.append(in_item)
        users.sort(key=lambda x: (x[1]), reverse = True)
        return users[:k]

    """ From k_users evaluate weight of items and recommend the top n items."""
    def fink_n_recommendation_from_near_users(self, user, k_users, n):
        items_and_weight = []
        items_and_index = {}
        index = 0
        for u in k_users:
            items = self.data.get_rawdata()[u[0]]
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

    """ Return recommendation with find the k_nearest users."""
    def find_n_recommendation(self, user, k, n, max_ham_dist = 0):
        return self.fink_n_recommendation_from_near_users(user=user, n=n, k_users=self.find_k_users(user=user, k=k))

    # Not use in this version, this problem was selved using better check of precision.
    """ Find n "good" users for test model. "Good" user have on k and k+1 different cosine value.
     Is good for small k to get User KNN precision against LSH.
     Because k+1 can be good in LSH but was selected other with same similarity.
     Return list of users for given k."""
    def find_n_good_user(self, k, n):
        count = 0
        users_list = []
        for user in self.data.get_rawdata():
            list = self.find_k_users(user, k+1)
            if list[k-1][1] == list[k][1]:
                continue
            users_list.append(user)
            count += 1
            if count == n:
                break
        return users_list

