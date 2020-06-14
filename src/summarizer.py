import csv


CHECKSTYLE_CYCLOMATIC_OUTPUT_PATH = 'checkstyle/cyclomatic_metric_results.csv'
CHECKSTYLE_NPATH_OUTPUT_PATH = 'checkstyle/npath_metric_results.csv'
CHECKSTYLE_NCSS_OUTPUT_PATH = 'checkstyle/ncss_metric_results.csv'
SINGS_METRIC_OUTPUT_PATH = 'signs-metric/signs_metric_results.csv'
LOC_METRIC_OUTPUT_PATH = 'loc-metric/loc_metric_results.csv'

CHECKSTYLE_ANALYZED_OUTPUT_PATH = 'checkstyle/analyzed.csv'

CHECKSTYLE_OWN_OUTPUT_PATH = 'analyzed.csv'

PMD_CYCLOMATIC_OUTPUT_PATH = 'pmd/cyclomatic_metric_results.csv'
PMD_NPATH_OUTPUT_PATH = 'pmd/npath_metric_results.csv'
PMD_NCSS_OUTPUT_PATH = 'pmd/ncss_metric_results.csv'

PMD_ANALYZED_OUTPUT_PATH = 'pmd/analyzed.csv'

CC_RESULTS = []
NCSS_RESULTS = []
NPATH_RESULTS = []
SIGNS_RESULTS =[]
LOC_RESULTS =[]


def get_clean_result_object():
    return {
        "file_name": '',
        "human_assessment": 0,
        "metric_correct": 0,
        "metric_bad": 0,
        "metric_same": 0
    }


def get_clean_analyzer_object():
    return {
        "file_name": '',
        "human_assessment": 0,
        "CC": 0,
        "N_PATH": 0,
        "NCSS": 0,
        "SIGNS": 0,
        "LOC": 0,
        "metric_full_agreement": 0,
        "CC+N_PATH": '',
        "CC+NCSS": '',
        "N_PATH+NCSS": '',
        "CC+SIGNS": '',
        "N_PATH+SIGNS": '',
        "NCSS+SIGNS": '',
        "CC+LOC": '',
        "N_PATH+LOC": '',
        "NCSS+LOC": ''
    }


def read_file(file_path, results_array):
    metric_results_file = open(file_path, 'r', newline='')
    csv_reader = csv.reader(metric_results_file, delimiter=',')
    flag = False
    for row in csv_reader:
        if not flag:
            flag = True
            continue
        result_object = get_clean_result_object()
        result_object["file_name"] = row[0]
        result_object["human_assessment"] = row[1]
        result_object["metric_correct"] = row[4]
        result_object["metric_bad"] = row[5]
        result_object["metric_same"] = row[6]
        results_array.append(result_object)
    metric_results_file.close()


def get_analyzed_value(result_object):
    if result_object["metric_correct"] == '1':
        return 1
    if result_object["metric_bad"] == '1':
        return 0
    if result_object["metric_correct"] == '1':
        return ''


def aggregate_results_and_save():
    output_results = []
    for i in range(len(CC_RESULTS)):
        analyzer_object = get_clean_analyzer_object()
        analyzer_object["file_name"] = CC_RESULTS[i]["file_name"]
        analyzer_object["human_assessment"] = CC_RESULTS[i]["human_assessment"]
        analyzer_object["CC"] = get_analyzed_value(CC_RESULTS[i])
        analyzer_object["N_PATH"] = get_analyzed_value(NPATH_RESULTS[i])
        analyzer_object["NCSS"] = get_analyzed_value(NCSS_RESULTS[i])
        analyzer_object["SIGNS"] = get_analyzed_value(SIGNS_RESULTS[i])
        analyzer_object["LOC"] = get_analyzed_value(LOC_RESULTS[i])
        if analyzer_object["CC"] == analyzer_object["N_PATH"] \
                and analyzer_object["N_PATH"] == analyzer_object["NCSS"]\
                and analyzer_object["NCSS"] == analyzer_object["SIGNS"]\
                and analyzer_object["SIGNS"] == analyzer_object["LOC"]\
                and analyzer_object["LOC"] == int(analyzer_object["human_assessment"]):
            analyzer_object["metric_full_agreement"] = 1
            analyzer_object["CC+N_PATH"] = 1
            analyzer_object["CC+NCSS"] = 1
            analyzer_object["N_PATH+NCSS"] = 1
            analyzer_object["CC+SIGNS"] = 1
            analyzer_object["N_PATH+SIGNS"] = 1
            analyzer_object["NCSS+SIGNS"] = 1
            analyzer_object["CC+LOC"] = 1
            analyzer_object["N_PATH+LOC"] = 1
            analyzer_object["NCSS+LOC"] = 1
        elif analyzer_object["CC"] == analyzer_object["N_PATH"] \
                and analyzer_object["N_PATH"] == int(analyzer_object["human_assessment"]):
            analyzer_object["CC+N_PATH"] = 1
        elif analyzer_object["CC"] == analyzer_object["NCSS"] \
                and analyzer_object["NCSS"] == int(analyzer_object["human_assessment"]):
            analyzer_object["CC+NCSS"] = 1
        elif analyzer_object["N_PATH"] == analyzer_object["NCSS"] \
                and analyzer_object["NCSS"] == int(analyzer_object["human_assessment"]):
            analyzer_object["N_PATH+NCSS"] = 1
        elif analyzer_object["SIGNS"] == analyzer_object["CC"] \
                and analyzer_object["CC"] == int(analyzer_object["human_assessment"]):
            analyzer_object["CC+SIGNS"] = 1
        elif analyzer_object["SIGNS"] == analyzer_object["N_PATH"] \
                and analyzer_object["N_PATH"] == int(analyzer_object["human_assessment"]):
            analyzer_object["N_PATH+SIGNS"] = 1
        elif analyzer_object["SIGNS"] == analyzer_object["NCSS"] \
                and analyzer_object["NCSS"] == int(analyzer_object["human_assessment"]):
            analyzer_object["NCSS+SIGNS"] = 1
        elif analyzer_object["LOC"] == analyzer_object["CC"] \
                and analyzer_object["CC"] == int(analyzer_object["human_assessment"]):
            analyzer_object["CC+LOC"] = 1
        elif analyzer_object["LOC"] == analyzer_object["N_PATH"] \
                and analyzer_object["N_PATH"] == int(analyzer_object["human_assessment"]):
            analyzer_object["N_PATH+LOC"] = 1
        elif analyzer_object["LOC"] == analyzer_object["NCSS"] \
                and analyzer_object["NCSS"] == int(analyzer_object["human_assessment"]):
            analyzer_object["NCSS+LOC"] = 1
        output_results.append(analyzer_object)
    return output_results


def convert_to_csv_and_save(path, results):
    metric_results_file = open(path, 'w', newline='')
    csvwriter = csv.writer(metric_results_file)
    csvwriter.writerow(get_clean_analyzer_object().keys())
    for single_result in results:
        csvwriter.writerow(single_result.values())
    metric_results_file.close()


read_file(CHECKSTYLE_CYCLOMATIC_OUTPUT_PATH, CC_RESULTS)
read_file(CHECKSTYLE_NCSS_OUTPUT_PATH, NCSS_RESULTS)
read_file(CHECKSTYLE_NPATH_OUTPUT_PATH, NPATH_RESULTS)
read_file(SINGS_METRIC_OUTPUT_PATH, SIGNS_RESULTS)
read_file(LOC_METRIC_OUTPUT_PATH, LOC_RESULTS)
# read_file(PMD_CYCLOMATIC_OUTPUT_PATH, CC_RESULTS)
# read_file(PMD_NCSS_OUTPUT_PATH, NCSS_RESULTS)
# read_file(PMD_NPATH_OUTPUT_PATH, NPATH_RESULTS)

analyzed_values = aggregate_results_and_save()

# convert_to_csv_and_save(CHECKSTYLE_ANALYZED_OUTPUT_PATH, analyzed_values)
convert_to_csv_and_save(CHECKSTYLE_OWN_OUTPUT_PATH, analyzed_values)
# convert_to_csv_and_save(PMD_ANALYZED_OUTPUT_PATH, analyzed_values)
