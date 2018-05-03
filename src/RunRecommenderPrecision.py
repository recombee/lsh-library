import Constants as const
from Lib.HelpFunction import AverageTimeChecker
from RecommenderPrecisionTesting import test_one_user, stop_stopwatch, start_stopwatch
import argparse, collections
from ArgumentParse import need_parse_argument, parse_arguments_for_program
from DataDbgetParse import get_and_preprocess_data
from Lib.WriteFileCVS import WriteFileCSV
from Lib.brut_force.UserKNN import UserKNN
from Lib.LSH_models.HashFunction import HashFunction
from Lib.LSH_models.LSHSigMatrix import LSHSigMatrix

# Parsing arguments from terminal
arguments = parse_arguments_for_program(args=need_parse_argument(parser=argparse.ArgumentParser("LSH"),
                                                                 recommender_precision=1), recommender_precision=1)
# Preprocess and split data
preprocess_base_data, test_users, test_users_id = get_and_preprocess_data(arguments=arguments,
                                                                          min_items_for_user = const.MIN_ITEMS_FOR_USER)
# Create file for write data
stastistic_file = WriteFileCSV(write_file=arguments["write_file"]+"_BF", separator=',',
                               list_of_columns=["time", "k", "coverage", "recall", "bucket_dim", "repeat"],
                               arguments=arguments)


# Create KNN model for recommending n items for user.
brut_force_model = UserKNN(data=preprocess_base_data)

# Testing recommendation of brute force model.
if arguments["compare"]:
    # Counter of users for detailed print.
    number_of_user = 1
    # Stopwatch to meansure time of evalute knn queries in model.
    average_time = AverageTimeChecker()
    # Recall for each k and user.
    recommendation_user_recall = {}
    # Coverage for each k
    map_k_recommended_items = {}
    for test_user in test_users:
        arguments["logp"].p("Test user number: ", number_of_user, print_level=3)
        number_of_user += 1
        test_one_user(user=test_user, user_items=test_users[test_user],
                      model=brut_force_model, arguments=arguments,
                      recommendation_user_recall=recommendation_user_recall,
                      map_k_recommended_items=map_k_recommended_items, time_meter=average_time)
        arguments["logp"].p(" ", print_level=3)

    # Save results to file. Order by k.
    od = collections.OrderedDict(sorted(recommendation_user_recall.items()))
    for k, v in od.items():
        to_save = {}
        to_save["time"] = 1
        reference_time = average_time.get_average_time()
        to_save["k"] = k
        to_save["coverage"] = len(map_k_recommended_items[k]) / preprocess_base_data.count_of_base_data_items()
        sum_recall = 0
        for i in v:
            sum_recall += v[i]
        to_save["recall"] = sum_recall / len(v)
        stastistic_file.write_line(dict=to_save)



# Test UserKNN recommneder precision over arguments given in command line.
for bucket_dimension in range(arguments["dim_reduce_start"],arguments["dim_reduce_end"]):
    for j in range(arguments["repeat"]):
        time_p = start_stopwatch()
        # Create hash function for LSH model.
        hash_function = HashFunction(data=preprocess_base_data,
                                     bucket_dimension=bucket_dimension,
                                     arguments=arguments,
                                     histograms=(arguments["write_file"] + "_MODEL_"))
        hash_function.create_hash_functions(number_of_hash_function=arguments["standart_hash"])
        hash_function.create_hash_function_from_argumnets(list_of_hash_function=arguments["hash"])
        # Create LSH model.
        LSH_model = LSHSigMatrix(hash_function=hash_function, arguments=arguments)
        arguments["logp"].p("Time of creating LSH model: ",
                                format(stop_stopwatch(time_p), '.3f'),
                                " s", print_level=1)
        # Test model for different size of check buckets.
        for test_hamming_distance_of_buckets in range(arguments["ham_dist_start"], arguments["ham_dist_end"]):
            stastistic_file = WriteFileCSV(write_file=arguments["write_file"] +
                                                      "_LSH_d_" + str(bucket_dimension) + "_c_" +
                                                      str(test_hamming_distance_of_buckets),
                                           separator=',',
                                           list_of_columns=["time", "k", "coverage", "recall", "bucket_dim",
                                                            "repeat", "test_ham_dist"]
                                           , arguments=arguments)

            # Counter of users for detailed print.
            number_of_user = 1
            # Stopwatch to meansure time of evalute knn queries in model.
            average_time = AverageTimeChecker()
            # Recall for each k and user.
            recommendation_user_recall = {}
            # Coverage for each k
            map_k_recommended_items = {}

            for test_user in test_users_id:
                arguments["logp"].p("Test user number: ", number_of_user, print_level=3)
                number_of_user += 1
                test_one_user(user=test_user, user_items=test_users_id[test_user],
                              model=LSH_model, arguments=arguments,
                              recommendation_user_recall=recommendation_user_recall,
                              map_k_recommended_items=map_k_recommended_items, time_meter=average_time,
                              test_ham_dist = test_hamming_distance_of_buckets )
                arguments["logp"].p(" ", print_level=3)

            if arguments["compare"]:
                arguments["logp"].p("Average time to find K nearest user LSH: ",
                                    format(average_time.get_average_time() / reference_time, '.3f'), "  to BF", print_level=2)
            else:
                arguments["logp"].p("Average time to find K nearest user LSH: ",
                                    format(average_time.get_average_time(), '.3f'), " s", print_level=2)


            # Save results to file. Order by k.
            od = collections.OrderedDict(sorted(recommendation_user_recall.items()))
            for k, v in od.items():
                to_save = {}
                to_save["test_ham_dist"] = test_hamming_distance_of_buckets
                to_save["bucket_dim"] = bucket_dimension
                to_save["repeat"] = j
                if arguments["compare"]:
                    to_save["time"] = average_time.get_average_time() / reference_time
                else:
                    to_save["time"] = average_time.get_average_time()

                to_save["k"] = k
                to_save["coverage"] = len(map_k_recommended_items[k]) / preprocess_base_data.count_of_base_data_items()
                sum_recall = 0
                for i in v:
                    sum_recall += v[i]
                to_save["recall"] = sum_recall / len(v)
                stastistic_file.write_line(dict=to_save)

arguments["logp"].printSUCCESS("Program succeeded. Data stored in: ",
                               arguments["write_file"],
                               "_<model>*<arguments>*",
                               stastistic_file.get_suffix(), "\n")