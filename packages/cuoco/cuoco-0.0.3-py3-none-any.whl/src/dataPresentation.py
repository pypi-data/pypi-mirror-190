
# Count number of nans
def countNans(df):
    nan_count = df.isna().sum().sum()
    return nan_count


def writeDF(df, route, name, output_format):
    if output_format == "csv" or output_format == "txt":
        df.to_csv(route + name + "." + output_format, index=False)
    elif output_format == "orc":
        df.to_orc(route + name + "." + output_format, index=False)
    elif output_format == "parquet":
        df.to_parquet(route + name + "." + output_format, index=False)
