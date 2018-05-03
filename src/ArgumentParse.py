LOG_FILE = "log.log"
""" Class for print on terminal or log."""
from Lib.LoggingPrint import LoggingPrint

""" Specific arguments of framework."""
def need_parse_argument(parser, recommender_precision = 0):
    argtest = parser.add_argument_group('arguments for running the test algorithm')
    argtest.add_argument('-i', '--inputfile', required=True, dest='s', metavar='SCHEMA',
                        help='Specific data schema in data in dbconfig.yaml.')
    argtest.add_argument('-o', '--outputfile', required=True, dest='f', metavar='FILE',
                        help='File with path to write statistic.')
    argtest.add_argument('-r', '--repeat', type=int, default=1, dest='r',
                        help='Number of repeating with this configuration with another random model. '
                             'Use another hash function for creating buckets with users.')
    argtest.add_argument('-t', type=float, default=0,
                        help='Size of testing set of users in percent. Default is 10 percent.')

    if recommender_precision == 1:
        argrecmodel = parser.add_argument_group('special arguments for testing recommendations')
        argrecmodel.add_argument('-k', type=int, default=9000,
                             help='Maximum k in testing recommendation. Values are from 1 to this specific. Default 8192.')
        argrecmodel.add_argument('-n', type=int, default=5,
                        help='Number of recommender items to check if tested is in. Default is 5.')
        argrecmodel.add_argument('-compare', action='store_true', help='If is this switch defined. Results will be compare to brute force user knn.')

    else:
        argtest.add_argument('-k', type=int, default=10,
                             help='Number of neighbour in User KNN algorithm. Default is 10.')





    argmodel = parser.add_argument_group('arguments for creating the LSH model')
    group = argmodel.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', type=int, metavar='DIM',
                       help='Dimension of reduction. Number of bucket is 2^dim_reduction.')
    group.add_argument('-di', type=int, nargs=2, metavar=('DIM_start','DIM_end'),
                       help='Interval test dimension of reduction. Test all dimension from first argument to second.')
    group = argmodel.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', type=int, metavar='HAM',
                       help='Max hamming distance for searching similar bucket. In this specification will be test one given.')
    group.add_argument('-ci', type=int, nargs=2, metavar=('HAM_start', 'HAM_end'),
                       help='Max hamming distance for searching similar bucket. In this specification will be test from first argument to second.')
    argmodel.add_argument('-M', type=int, default=0, help='Number of standart hash function. Default is 0')
    argmodel.add_argument('-m', nargs='+', required=True, metavar='MATRIXs_STRING',
                        help='Specific hash function separately. Type as values separately by +. '
                             'When is nothing between will be use default. '
                             'If one value is use as alfa, two values as min and max in hash function. '
                             'And tree values for specific min, max, alfa.')




    argrealiz = parser.add_argument_group('arguments for debugging and printing information')
    argrealiz.add_argument("-buckets", action='store_true', help='If this switch defined will be prints models with histograms '
                                                 'of users in buckets' )
    argrealiz.add_argument("-terminal", default = "no", const = "basic",
                        nargs='?', metavar='LEVEL',
                        help='Specific print to terminal. Without parametr basic info. '
                                                                     'With "info" print info of running algorithm. '
                                                                     'With "debug" print all info to terminal. ')
    argrealiz.add_argument('-log', default = ('log.log','basic'), nargs=2, metavar=('LOGFILE','LEVEL'),
                        help='Specific logging. First argument is logfile. Without parametr is use log.log. '
                                'Second parametr is level of log. '
                                'With "basic" print some info about data.'
                                'With "info" print info of running algorithm. '
                                'With "debug" print all info to logfile. ')




    return parser.parse_args()

""" Parse and check arguments."""
def parse_arguments_for_program(args, recommender_precision = 0):
    arguments = {}
    if args.buckets:
        arguments["hist"] = True
    else:
        arguments["hist"] = False

    arguments["logfile"] = args.log[0]
    if args.log[1] == "basic" or args.log[1] == "info" or args.log[1] == "debug":
        arguments["log"] = args.log[1]
    else:
        arguments["log"] = "no"

    if args.terminal == "basic" or args.terminal == "info" or args.terminal == "debug":
        arguments["print_level"] = args.terminal
    else:
        arguments["print_level"] = "no"

    if args.M < 0:
        arguments["standart_hash"] = 0
    else:
        arguments["standart_hash"] = args.M

    arguments["write_file"] = args.f
    arguments["infile"] = args.s
    arguments["size_of_test_set"] = args.t
    if args.k <= 0:
        arguments["k"] = 1
    else:
        arguments["k"] = args.k

    if args.r <= 0:
        arguments["repeat"] = 1
    else:
        arguments["repeat"] = args.r

    if args.d:
        arguments["dim_reduce_start"] = args.d
        arguments["dim_reduce_end"] = args.d+1
    if args.di:
        arguments["dim_reduce_start"] = args.di[0]
        arguments["dim_reduce_end"] = args.di[1]
    if args.c == 0 or args.c:
        arguments["ham_dist_start"] = args.c
        arguments["ham_dist_end"] = args.c + 1
    if args.ci:
        arguments["ham_dist_start"] = args.ci[0]
        arguments["ham_dist_end"] = args.ci[1]
    try:
        arguments["logp"] = LoggingPrint(print_level=arguments["print_level"], log=arguments["log"], log_file=arguments["logfile"])
    except:
        arguments["logp"] = LoggingPrint(print_level=arguments["print_level"], log=arguments["log"],
                                         log_file=LOG_FILE)
    check_dimension_values(arguments)
    if recommender_precision == 1:
        arguments["number_of_recommendation"] = args.n
        if args.compare:
            arguments["compare"] = True
        else:
            arguments["compare"] = False

    matrixs = []
    status = 0
    read = []
    for i in args.m:
        try:
            read.append(float(i))
            status += 1
        except ValueError:
            matrixs.append(read_one_hash_function(status, read, arguments=arguments))
            status = 0
            read = []
    matrixs.append(read_one_hash_function(status, read, arguments=arguments))
    arguments["hash"] = matrixs
    return arguments

def check_dimension_values(arguments):
    if arguments["dim_reduce_start"] <= 0 or arguments["dim_reduce_end"] <= arguments["dim_reduce_start"]:
        arguments["logp"].printERROR("ERROR: No run bad value of dimension specification -d or -di")
        exit(1)
    if arguments["ham_dist_start"] < 0 or arguments["ham_dist_end"] <= arguments["ham_dist_start"]:
        arguments["logp"].printERROR("ERROR: No run bad value of testing near buckets -c or -ci")
        exit(1)

""" Parse read values of hash functions from command line."""
def read_one_hash_function(read_status, read, arguments):
    one_matrix = {}
    if read_status == 0:
        return one_matrix
    elif read_status == 1:
        one_matrix["alfa"] = read[0]
    elif read_status == 2:
        one_matrix["min"] = read[0]
        one_matrix["max"] = read[1]
    elif read_status == 3:
        one_matrix["min"] = read[0]
        one_matrix["max"] = read[1]
        one_matrix["alfa"] = read[2]
    else:
        arguments["logp"].printERROR("ERROR: Cant parse hash function. Type as values separately by +. "
              "When is nothing between is use default. "
              "If one value is use as alfa, two values as min and max in hash function. "
              "And tree values for specific min, max, alfa.")
    return one_matrix
