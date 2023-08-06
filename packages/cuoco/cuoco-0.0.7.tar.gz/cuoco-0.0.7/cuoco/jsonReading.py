import sys

# Check json file for unaccepted values
def checkJSONFormat(json_file):

    accepted_inputForm = ["csv", "parquet", "orc", "txt"]
    accepted_outputForm = ["csv", "parquet", "orc", "txt"]
    accepted_header = ["yes", "none"]
    accepted_numNans = ["drop", "yes", "mean", "mode", "median"]
    accepted_strNans = ["yes", "no"]
    accepted_caps = ["no", "lower", "upper"]
    accepted_balanceData = ["yes", "no"]
    accepted_normalize = ["max_abs", "min_max", "z_score", "no"]
    accepted_balanceMethod = ["random", "smote"]
    #accepted_quotation = ["double", "single", "none"]

    if json_file['input_format'] not in accepted_inputForm:
        print("ERROR in JSON: input_format is not an accepted value")
        sys.exit(1)
    elif json_file['output_format'] not in accepted_outputForm:
        print("ERROR in JSON: output_format is not an accepted value")
        sys.exit(1)
    elif json_file['header'] not in accepted_header:
        print("ERROR in JSON: header is not an accepted value")
        sys.exit(1)
    elif json_file['num_nans'] not in accepted_numNans:
        print("ERROR in JSON: num_nans is not an accepted value")
        sys.exit(1)
    elif json_file['str_nans'] not in accepted_strNans:
        print("ERROR in JSON: str_nans is not an accepted value")
        sys.exit(1)
    elif json_file['caps'] not in accepted_caps:
        print("ERROR in JSON: caps is not an accepted value")
        sys.exit(1)
    elif json_file['normalize_method'] not in accepted_normalize:
        print("ERROR in JSON: normalize_method is not an accepted value")
        sys.exit(1)
