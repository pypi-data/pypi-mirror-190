# Count number of nans
def countNans(df):
    nan_count = df.isna().sum().sum()
    return nan_count


def showStats(original_df, actual_df):
    # NANS
    print("Count of NANS in the raw dataset:")
    print(countNans(original_df))

    print(" ")
    print("***********")
    print(" ")

    # Removed rows
    print("Number of removed rows:")
    print(len(original_df) - len(actual_df))

    print(" ")
    print("***********")
    print(" ")



def writeDF(df, route, name, output_format):
    if output_format == "csv" or output_format == "txt":
        df.to_csv(route + name + "." + output_format, index=False)
    elif output_format == "orc":
        df.to_orc(route + name + "." + output_format, index=False)
    elif output_format == "parquet":
        df.to_parquet(route + name + "." + output_format, index=False)
