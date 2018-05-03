from abc import ABC, abstractmethod
"""Abstract class for KNN algorithms of LSH"""
class KNN(ABC):

    @abstractmethod
    def __init__(self, hash_function, arguments):
        pass

    @abstractmethod
    def find_k_users(self, user, k, max_ham_dist = 0):
        pass

    """Method compute recomendations from given dict of k near users."""
    @abstractmethod
    def fink_n_recommendation_from_near_users(self, user, k_users, n):
        pass

    """Method first find k nearest neighbour and then compute recomendations."""
    @abstractmethod
    def find_n_recommendation(self, user, k, n, max_ham_dist = 0):
        pass
