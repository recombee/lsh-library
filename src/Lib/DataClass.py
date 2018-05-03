
class DataClass:
    def __init__(self,map_user_item_with_value, bimap_user_id, bimap_item_id,
                 idmap_user_item_with_value, map_item_with_weight_of_item,
                 map_user_sum_product, idmap_user_sum_product):
        self.map_user_item_with_value = map_user_item_with_value
        self.bimap_user_id = bimap_user_id
        self.bimap_item_id = bimap_item_id
        self.idmap_user_item_with_value = idmap_user_item_with_value
        self.map_item_with_weight_of_item = map_item_with_weight_of_item
        self.map_user_sum_product = map_user_sum_product
        self.idmap_user_sum_product = idmap_user_sum_product

    """ Map<user, items<item, value>>."""
    def get_rawdata(self):
        return self.map_user_item_with_value

    """ Bimap<user, user_id>."""
    def get_user_id_dict(self):
        return self.bimap_user_id

    """ Bimap<item, item_id>."""
    def get_item_id_dict(self):
        return self.bimap_item_id

    """ Map<user_id, items<item_id, value>>."""
    def get_new_id_data(self):
        return self.idmap_user_item_with_value

    """ Map<item, weight>."""
    def get_weight_of_items(self):
        return self.map_item_with_weight_of_item

    """ Map<user, sqrt(sum(x^2))>."""
    def get_dict_users_sum_product(self):
        return self.map_user_sum_product

    """ Map<user_id, sqrt(sum(x^2))>."""
    def get_dict_users_id_data_sum(self):
        return self.idmap_user_sum_product

    """ Return number of items in learning part of data."""
    def count_of_base_data_items(self):
        items = {}
        for i in self.map_user_item_with_value:
            for j in self.map_user_item_with_value[i]:
                items[j] = True
        return len(items)




