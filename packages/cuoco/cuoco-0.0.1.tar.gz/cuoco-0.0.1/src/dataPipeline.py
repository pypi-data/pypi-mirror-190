import json
import jsonReading
import dataCleaning
import dataModeling
import dataPresentation


def readJson(dataFile, jsonFile):
    # VARIABLES
    global dataDF

    # DATA FILE READING
    json_opener = open(jsonFile)
    json_file = json.load(json_opener)
    input_data_type = json_file['input_format']
    jsonReading.checkJSONFormat(json_file)
    # Get the data in pandas df format
    original_dataDF = dataCleaning.readFile(input_data_type, dataFile, json_file['separator'], json_file['header'])
    original_dataDF.columns = original_dataDF.columns.str.strip().str.replace('"', '')
    for col in original_dataDF:
        if original_dataDF.dtypes[col] == "object":
            original_dataDF[col] = original_dataDF[col].str.replace('"', '')
    # -----------------------------------------------------

    # CLEANING

    # ** NANs ***
    # Numeric NANS
    if json_file['num_nans'] != "yes":
        dataDF = dataCleaning.numNans(original_dataDF, json_file['num_nans'])
    # String NANS
    if json_file['str_nans'] == "no":
        dataDF = dataCleaning.strNans(original_dataDF)

    # ** WHITES ***
    dataDF = dataCleaning.removeWhites(dataDF)

    # ** CAPS ***
    if json_file['caps'] != "no":
        dataDF = dataCleaning.caps(dataDF, json_file['caps'])

    # ** QUOTES ***
    #dataDF = dataCleaning.quotes(dataDF, json_file['str_quotation'])

    # -----------------------------------------------------

    # MODELING
    if json_file['normalize'] != "":
        for col in json_file['normalize']:
            dataDF = dataModeling.normalize(col, dataDF, json_file['normalize_method'])

    # OverSampling
    #if json_file['balance_data'] == "yes":
    #    dataDF = dataModeling.oversampling(dataDF, json_file['balance_params']['balance_method'],
    #                                       json_file['balance_params']['y_col'])


    # -----------------------------------------------------

    # PRESENTATION

    # NANS
    print("Count of NANS in the raw dataset:")
    print(dataPresentation.countNans(original_dataDF))
    #dataDF = dataDF.drop(columns=dataDF.columns[0], axis=1, inplace=True)
    dataPresentation.writeDF(dataDF, json_file['new_file_route'], json_file['new_fileName'], json_file['output_format'])
