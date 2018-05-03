import math as ma
from DataDbgetParse import stop_stopwatch, start_stopwatch
import Constants as const

""" Test recommendation over given k nearest neighbours, save recommended items for given k and good hits for one user."""
def test_one_k(k_nearest, k, model, recommendation_user_recall, user, number_of_recommendation, test_item, test_c_user, map_k_recommended_items ):
    if k not in recommendation_user_recall:
        recommendation_user_recall[k] = {}
    if user not in recommendation_user_recall[k]:
        recommendation_user_recall[k][user] = 0
    if k not in map_k_recommended_items:
        map_k_recommended_items[k] = {}

    recommendation = model.fink_n_recommendation_from_near_users(user=test_c_user,
                                                                 k_users=k_nearest,
                                                                 n=number_of_recommendation)
    recommend_items = [item[0] for item in recommendation]
    # Save recommended items to maps for coverage.
    for recommend_item in recommend_items:
        map_k_recommended_items[k][recommend_item] = True
    # Count ++ if omitted item is in recommendation.
    if test_item in recommend_items:
        recommendation_user_recall[k][user] += 1

""" Test one user over number of missed items. 
For each miss item find the max k nearest neighbours and recommendation test for each selected k.
K is select exponencially."""
def test_one_user(user_items, model, arguments, user, recommendation_user_recall, map_k_recommended_items, time_meter, test_ham_dist=0):
    number_of_test = len(user_items)
    tested_items = 0
    arguments["logp"].p("Test user with: ", number_of_test, " items", print_level=3)
    if (len(user_items) > 1):
        for test_item in user_items:
            # Delete one item from list.
            test_c_user = user_items.copy()
            del test_c_user[test_item]

            time_p = start_stopwatch()
            # Find the max k nearest users to one user.
            k_nearest = model.find_k_users(user=test_c_user, k=arguments["k"], max_ham_dist=test_ham_dist)
            time_meter.save_time(stop_stopwatch(time_p))

            # Go over k what is wanted. Now go for exponencial values.
            # TO DO: can i go over k by specific step?
            for k in range(ma.ceil(ma.log(arguments["k"],2))+1):
                test_one_k(k_nearest[:arguments["k"]] if 2**k > arguments["k"] else k_nearest[:2**k],
                           arguments["k"] if 2**k > arguments["k"] else 2**k,
                           model=model, recommendation_user_recall=recommendation_user_recall, user=user,
                           number_of_recommendation=arguments["number_of_recommendation"],
                           test_item=test_item, test_c_user=test_c_user, map_k_recommended_items=map_k_recommended_items)
            tested_items += 1
            if tested_items >= const.MAX_TESTED_MISSING_ITEMS_FOR_ONE_USER:
                break

    # Divided number of hits by number of test to get percentage recall for one user.
    arguments["logp"].p("It was test only: ", tested_items, " items", print_level=4)
    change_recall_to_percentage(recommendation_user_recall=recommendation_user_recall, number_of_test=tested_items, user=user)

""" Count of good recommendations for every k is divided by number of tests on only one user what was tested."""
def change_recall_to_percentage(recommendation_user_recall, number_of_test, user):
    for k in recommendation_user_recall:
        recommendation_user_recall[k][user] = recommendation_user_recall[k][user] / number_of_test