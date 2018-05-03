# Library for testing Locality-sensitive hashing (LSH) algorithms in recommender systems
The library was created in the frame of a&nbsp;bachelor thesis at the Faculty of Information Technology.
The thesis deals with the recommender systems, especially it deals with the approximation of the k-nearest neighbors algorithm using LSH methods.

The library has been implemented within its practical part and enables parametric testing of various LSH models on different datasets. The library is implemented in Python.

## Requirements
* Python version 3.5 and higher
* Libraries for Python specified in requirements.txt

## Limitations
* The library also tests models for time acceleration, so model testing is not multithreaded.
* Only offline static data from csv files can be loaded, where there are the [userid, itemid, rating] columns.

## Arguments
Arguments are divided into several subgroups depending on which parts are directly relevant.


### Arguments for running a test library
These arguments are not directly related to individual LSH models but are used to set important things when testing models by the library. The arguments are as follows:

* **-i, --inputfile** Required argument that specifies the name of the input data file in csv format.
* **-o, --ouputfile** Required argument that specifies both the output file name and the existing path. If the file does not exist, it will be created. If so, the data is written to the end of the file.
* **-r, --repeat** Optional argument whose default value is set to 1. Argument specifies the number of test repeats concrete model specification. Individual repeats are written to the end of the output file.
* **-t** Optional argument specifying the size of the test set. The size is specified as a&nbsp;percentage of the total number of users in the data. If the argument is not specified, the test set size of 10&nbsp;%&nbsp;will be used.
* **-k** Argument that specifies the number of nearest neighbors in a&nbsp;query. The argument has a&nbsp;slightly different meaning in testing the success rate of the recommendation which I describe separatelly. When testing the precision of k-NN, it specifies the number of nearest neighbors on which the models are tested. If not specified, the basevalue is 10.

### Arguments of the LSH model
The arguments in this section specify the structure of each model, model settings, and how to query the model. The arguments are as follows:

* **-d, -di** These arguments specify the dimension of the projection matrices of the particular model. It is possible to test one model or more models determined by an interval. Individual LSH models with different hash functions are created and tested sequentially. One of the following arguments is always required.
    * **-d** Specifies the matrix dimension for one tested model.
    * **-di** Specifies the interval of matrix dimensions in hash functions. Individual LSH models with hash functions with different dimensions are then sequentially tested and the results are written into files according to the model specifications.
* **-c, -ci** Arguments determining the size of the bucket surrounding area in each query, where the test user was hashed, using the hamming distance of the buckets. Arguments can be specified in two ways and one of the following is always required.
    * **-c** Specifies one particular size of the surrounding area to be used when evaluating LSH models.
    * **-ci** Specifies the value range of the surrounding area. The model is then tested for each value from interval.
* **-M** Optional argument specifying the number of standard hash functions in the model. Each such hash function is generated from the uniform probability distribution U(-1, 1).
* **-m** Argument specifying parameters for each the hash function created. The text string format is the following for hash functions H: H1 + H2 + ... + Hn, where H can be specified in three different ways:
    * If H is a blank string, a standard hash function is used.
    * H as one value that determines alpha size.
    * H as a&nbsp;pair of values ​​specifies *a,&nbsp;b*&nbsp;for uniform probability distribution U(a, b) when generating a&nbsp;hashing function.
    * If H is a&nbsp;triple value. The first specifies parameters *a*&nbsp;and *b*&nbsp;for uniform distribution, and the third determines alpha.

### Special arguments during testing of the recommendation 
Some of the arguments in this section have different behaviors, or are only given when testing the recommended success rate:

* **-k** This argument when testing the recommendation's success rate determines the upper limit of the tested k. The k&nbsp;values form the exponential series 1, 2, 4, 8, ... The argument is optional and its default value is set to 8196.
* **-n** It is an optional argument that specifies the number of recommended items in the top-n recommendation. Default value is 5.
* **-compare** This switch specifies whether to test the brute force reference model on the same test set to compare acceleration and success.

### Framework implementation arguments
These arguments are not directly related to LSH testing, but are useful for running a library and generating some results. Arguments are optional and the following:

* **-buckets** The argument specifies whether csv files will be generated with user partitions between individual buckets in each hash function. Each bucket also lists the average value of the item's popularity between 0&nbsp;and&nbsp;1.
* **-terminal**  Argument that can be used for debugging, data control, and runtime testing. When entering the frame argument, the following data is written to the terminal according to the specified value.

    There are four levels of printing information. If the argument value is not specified, it is informed only of the successful end of the run. If the *basic* parameter is specified, only the dataset data and the end of the test are printed. The next level specified by *info* prints detailed information about the dataset, creating models and results for each LSH model. The third level is debugging specified by *debug*. This setting prints the maximum amount of runtime information.
* **-log** Argument used to create a library log. As the first value, it accepts the name of the file with the existing path to which the log will be logged. The second one can specify the level of log just as with the previous (-teminal) argument, except that the information is logged with time to the file, and one of three options is required.


## Examples
There are avaible bash scripts (KNNTest.sh, RecommenderTest.sh) to start testing, in which only parameters of LSH can be modified. The test can be also run directly. Here are some basic examples of tests for starting it directly.

* Example of k-NN algorithm precision testing

```bash
python3 src//RunKnnPrecision.py -i "ratings.csv" -o "test.csv" -d 10 -c 0 -m 0.0 -M 1 -log logs/test.log info 
```

* Example of testing recommendation (measures of success are recall and catalog coverage)

```bash
python3 src//RunRecommenderPrecision.py -i "ratings.csv" -o "test.csv" -k 20000 -di 9 11 -c 1 -m 0 -M 1 -terminal debug
```