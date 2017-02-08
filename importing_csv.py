import csv

# location of csv file for data-driven testing
FILE_WITH_PARAMS = 'params.csv'


def importing_csv():
    """Auxiliary function:
    Opens 'params.csv' file in this module's dir,
    reads all lines and composes parameters tuple
    in specific pytest format including headers
    and values. Returns this tuple for further
    test function parameterizing
    """
    parameters_list = []
    parameters_header = ("from_currency", "to_currency", "value")
    with open(FILE_WITH_PARAMS, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            parameters_list.append(tuple(row))
    parameters = (parameters_header, parameters_list)
    return parameters

if __name__ == '__main__':
    print(importing_csv())
