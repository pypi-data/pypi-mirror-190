from imblearn.over_sampling import RandomOverSampler


# Function for data normalization
def normalize(col, df, method):
    if method == "max_bas":
        df[col] = df[col] / df[col].abs().max()
    elif method == "min_max":
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    elif method == "z_score":
        df[col] = (df[col] - df[col].mean()) / df[col].std()

    return df


# Function to manage oversampling method
def oversampling(df, method, ycol):
    if method == "random":
        df = randomOverSampling(df, ycol)
    elif method == "smote":
        df = SMOTE(df, ycol)
    return df


# Perform random oversampling of the dataframe
def randomOverSampling(df, ycol):
    oversampler = RandomOverSampler(sampling_strategy='minority')
    X = df.loc[:, df.columns != ycol]
    Y = df[ycol]

    return df


# Perform SMOTE in the dataframe
def SMOTE(df, ycol):
    return df
