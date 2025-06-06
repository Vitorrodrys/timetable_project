from solver.input_parser import create_parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)# run the corresponding method of solver or excel reader (according to which one user has selected)
