import argparse
from ArgumentParse import need_parse_argument, parse_arguments_for_program
from Lib.brut_force.UserKNN import UserKNN
from Lib.LSH_models.HashFunction import HashFunction
from Lib.LSH_models.LSHSigMatrix import LSHSigMatrix
from Lib.HelpFunction import check_precision_user_knn
from DataDbgetParse import get_and_preprocess_data, stop_stopwatch, start_stopwatch
from Lib.WriteFileCVS import WriteFileCSV

# Parsing arguments from terminal
arguments = parse_arguments_for_program(args=need_parse_argument(parser=argparse.ArgumentParser("LSH")))

# Preprocess and split data
preprocess_base_data, test_users, test_users_id = get_and_preprocess_data(arguments=arguments)

# Create KNN model for find the K nearest users over all users in model.
brut_force_model = UserKNN(data=preprocess_base_data)
reference_result_user = {}
sum_of_time = 0
count_of_run = 0
# Test to find k users for all users in test set by brute-force model.
for test_user in test_users:
    time_brute_force = start_stopwatch()
    reference_result_user[test_user] = brut_force_model.find_k_users(user=test_users[test_user], k=arguments["k"])
    time_brute_force = stop_stopwatch(time_brute_force)
    arguments["logp"].p("Time to fink k users brute force: ", format(time_brute_force, '.2f'), " s", print_level=3)
    sum_of_time += time_brute_force
    count_of_run += 1
arguments["logp"].p("Average time to find K nearest user: ",
                        format(sum_of_time / count_of_run, '.2f'), " s", print_level=2)
arguments["logp"].p(print_level=3)
reference_time = sum_of_time / count_of_run


# Test UserKNN precision over arguments given in command line.
for j in range(arguments["repeat"]):
    stastistic_file = WriteFileCSV(write_file=arguments["write_file"] + "_LSH", separator=',',
                                   list_of_columns=["time", "precision", "bucket_dim", "repeat", "test_ham_dist", "k"],
                                   sorted=["time"], arguments=arguments)
    for bucket_dimension in range(arguments["dim_reduce_start"],arguments["dim_reduce_end"]):
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
                                format(stop_stopwatch(time_p), '.2f'), " s", print_level=1)
        # Test model for different size of controling buckets buckets.
        for test_hamming_distance_of_buckets in range(arguments["ham_dist_start"], arguments["ham_dist_end"]):
            sum_of_time = 0
            count_of_run = 0
            sum_of_precision = 0
            # Testing to fink k near users using LSH model.
            for test_user in test_users_id:
                time_LSH = start_stopwatch()
                k_users = LSH_model.find_k_users(user=test_users_id[test_user], k=arguments["k"],
                                           max_ham_dist=test_hamming_distance_of_buckets)
                time_LSH = stop_stopwatch(time_LSH)
                arguments["logp"].p("Time to fink k users LSH: ", format(time_LSH, '.3f'), " s", print_level=3)
                sum_of_time += time_LSH
                count_of_run += 1

                # Check precision compare to brutforce model.
                bidict_user_id = preprocess_base_data.get_user_id_dict()
                precision = check_precision_user_knn(reference_list=reference_result_user[bidict_user_id.inv[test_user]],
                                                     check_list=k_users)
                arguments["logp"].p("Precision fink k users LSH to reference model: ",
                                        format(precision, '.2f'), print_level=3)
                arguments["logp"].p(" ", print_level=3)
                sum_of_precision += precision


            arguments["logp"].p("Average time to find K nearest user LSH: ",
                                    format((sum_of_time / count_of_run) / reference_time, '.3f'), "  to BF"," Average precision LSH: ",
                                    format(sum_of_precision / count_of_run, '.2f'), print_level=2)
            # Save results to file
            to_save = {}
            to_save["bucket_dim"] = bucket_dimension
            to_save["test_ham_dist"] = test_hamming_distance_of_buckets
            to_save["repeat"] = j
            to_save["k"] = arguments["k"]
            to_save["time"] = (sum_of_time / count_of_run) / reference_time
            to_save["precision"] = sum_of_precision / count_of_run
            stastistic_file.write_line(dict=to_save)

arguments["logp"].printSUCCESS("Program succeeded. Data stored in files: ",
                               arguments["write_file"],"_LSH" , stastistic_file.get_suffix(), "\n")






