from Lib.HelpFunction import stop_stopwatch, start_stopwatch
from Lib.data.DataCSV import DataCSV
from Lib.PreprocessClass import Preprocess

"""Method manage getting data and preprocessing for both tests."""
def get_and_preprocess_data(arguments, min_items_for_user = 1):

    preprocess_class = Preprocess(arguments=arguments)
    preprocess_class.add_data(DataCSV().get_data(conf_dic=arguments))

    arguments["logp"].p("Count of rows in ", arguments["infile"], " data: ", preprocess_class.get_count(), print_level=1)


    # Preprocessing raw data for algorithm, create dictionaries, map users and item to int id,
    # count weight of items, and count sum of user vectors for cosine similarity.
    time_p = start_stopwatch()
    preprocess_base_data, test_users, test_users_id = preprocess_class.preprocessing(min_items_for_user=min_items_for_user)

    arguments["logp"].p("Count of users in base data: ", len(preprocess_base_data.get_rawdata()), print_level=1)
    arguments["logp"].p("Count of items in base data: ",
                            preprocess_base_data.count_of_base_data_items(), print_level=1)
    arguments["logp"].p("Time of preprocess: ", format(stop_stopwatch(time_p), '.2f'), " s", print_level=1)
    arguments["logp"].p("Count of users in test set: ", len(test_users), print_level=1)
    arguments["logp"].p("Percentage of matrix density: ",
                            format(preprocess_class.get_count() / (len(preprocess_base_data.get_user_id_dict()) *
                                                    len(preprocess_base_data.get_item_id_dict())) * 100,'.5f'),
                            " %", print_level=1)
    return preprocess_base_data, test_users, test_users_id