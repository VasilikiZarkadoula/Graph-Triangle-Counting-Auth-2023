import warnings

# available graphs
ASTROPH = 1
GRQC = 2
EMAILCORE = 3
TOY_UNDIRECTED = 4
TOY_DIRECTED = 5
AVAILABLE_DATASETS = {ASTROPH, GRQC, EMAILCORE, TOY_UNDIRECTED, TOY_DIRECTED}

# available algorithms
BRUTE_FORCE = "Brute Force"
NODE_ITERATOR = "Node Iterator"
COMPACT_FORWARD = "Compact Forward"
TRIEST = "Triest"
DOULION = "Doulion"


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def toString(self):
        [print(key, value) for key, value in self.items()]
        print()


def validate_args(args):
    # missing parameters
    if args.get('graph_name', None) is None:
        args.graph_name = None
        warnings.warn("\nRequired parameter args.graph_name is missing.", stacklevel=2)
    if args.get('selected_algorithm', None) is None:
        args.selected_algorithm = None
        warnings.warn("\nRequired parameter args.selected_algorithm is missing.", stacklevel=2)
    if args.get('with_doulion', None) is None:
        args.with_doulion = False
        warnings.warn("\nOptional parameter args.with_doulion is missing. Setting its value to False...", stacklevel=2)
    if args.get('plotApproximate', None) is None:
        args.plotApproximate = False
        warnings.warn("\nOptional parameter args.plotApproximate is missing. Setting its value to False...", stacklevel=2)

    # dataset
    if args.graph_name not in AVAILABLE_DATASETS:
        raise SystemExit(f"Unknown dataset {args.graph_name}.\nChange args.graph_name value (it should be a variable).\n"
                        f"See available datasets at utils.py.")

    # selected algorithms
    if args.selected_algorithm not in {BRUTE_FORCE, NODE_ITERATOR, COMPACT_FORWARD, TRIEST}:
        raise SystemExit(f"Unknown triangle counting algorithms.\nSet args.selected_algorithm to one of "
                        f"\nthe following variables: BRUTE_FORCE, NODE_ITERATOR, COMPACT_FORWARD or TRIEST.")

    # doulion and triest
    if args.with_doulion and args.selected_algorithm == TRIEST:
        args.with_doulion = False
        warnings.warn(f"\nargs.with_doulion == True and args.selected_algorithm == TRIEST."
                      f"\nThese algorithms are incompatible. Setting args.with_doulion to False...", stacklevel=2)

    # p
    if args.with_doulion and not args.plotApproximate:
        p = args.get('p', None)
        if p is None or type(p) not in {int, float}:
            args.plotApproximate = True
            warnings.warn(f"\nargs.with_doulion == True and args.plotApproximate == False"
                          f"\nbut args.p = {p} invalid. Setting args.plotApproximate to True...", stacklevel=2)

    # memory size
    if args.selected_algorithm == TRIEST and not args.plotApproximate:
        memorySize = args.get('memorySize', None)
        if isinstance(memorySize, float):
            args.memorySize = int(memorySize)
            warnings.warn(f"\nargs.memorySize should be an integer. Setting its value to int(args.memorySize)...", stacklevel=2)

        elif memorySize is None or not isinstance(memorySize, int):
            args.plotApproximate = True
            warnings.warn(f"\nargs.selected_algorithm == TRIEST and args.plotApproximate == False"
                          f"\nbut args.memorySize = {memorySize} invalid. Setting args.plotApproximate to True...", stacklevel=2)

    # plot non-approximate algorithm
    if args.plotApproximate and (args.selected_algorithm != TRIEST or not args.with_doulion):
        args.plotApproximate = False
        warnings.warn(f"\nargs.plotApproximate == True but args.selected_algorithm = {args.selected_algorithm} "
                      f"is an exact algorithm."
                      f"\nSetting args.plotApproximate to False...",
                      stacklevel=2)


def graph_picker(graph_name):
    if graph_name == ASTROPH:
        # undirected https://snap.stanford.edu/data/ca-AstroPh.html
        graph_path = "graphs/CA-AstroPh.txt"
        numOfTriangles = 1351441
        is_directed = False

    elif graph_name == GRQC:
        graph_path = "graphs/CA-GrQc.txt"
        numOfTriangles = 48260
        is_directed = False

    elif graph_name == EMAILCORE:
        # directed https://snap.stanford.edu/data/email-Eu-core.html
        graph_path = "graphs/email-Eu-core.txt"
        numOfTriangles = 105461
        is_directed = True

    elif graph_name == TOY_UNDIRECTED:
        graph_path = "graphs/toy_example_3_triangles.txt"
        numOfTriangles = 3
        is_directed = False

    elif graph_name == TOY_DIRECTED:
        graph_path = "graphs/toy_example_directed.txt"
        numOfTriangles = 2
        is_directed = True

    else:
        raise Exception("Unknown dataset")

    return graph_path, is_directed, numOfTriangles


