import csv


CHECKSTYLE_CYCLOMATIC_OUTPUT_PATH = 'checkstyle/cyclomatic_metric_results.csv'
CHECKSTYLE_NPATH_OUTPUT_PATH = 'checkstyle/npath_metric_results.csv'
CHECKSTYLE_NCSS_OUTPUT_PATH = 'checkstyle/ncss_metric_results.csv'
SINGS_METRIC_OUTPUT_PATH = 'signs-metric/signs_metric_results.csv'
LOC_METRIC_OUTPUT_PATH = 'loc-metric/loc_metric_results.csv'

CC_RESULTS = []
NCSS_RESULTS = []
NPATH_RESULTS = []
SIGNS_RESULTS =[]
LOC_RESULTS =[]

CC_THRESHOLD = 2
NPATH_THRESHOLD = 2
NCSS_THRESHOLD = 3
SIGNS_THRESHOLD = 100
LOC_THRESHOLD = 6


def get_clean_result_object():
    return {
        "file_name": '',
        "human_assessment": 0,
        "metric_before": 0,
        "metric_after": 0
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
        result_object["metric_before"] = row[2]
        result_object["metric_after"] = row[3]
        results_array.append(result_object)
    metric_results_file.close()


def check_metric_with_threshold(metric_results, metric_name, threshold):
    correctness = 0
    for i in range(len(metric_results)):
        if int(metric_results[i]["metric_after"]) < threshold and metric_results[i]["human_assessment"] == '1':
            correctness += 1
        if int(metric_results[i]["metric_before"]) < threshold and metric_results[i]["human_assessment"] == '0':
            correctness += 1
    print(metric_name, " matches human: ", correctness)


read_file(CHECKSTYLE_CYCLOMATIC_OUTPUT_PATH, CC_RESULTS)
read_file(CHECKSTYLE_NCSS_OUTPUT_PATH, NCSS_RESULTS)
read_file(CHECKSTYLE_NPATH_OUTPUT_PATH, NPATH_RESULTS)
read_file(SINGS_METRIC_OUTPUT_PATH, SIGNS_RESULTS)
read_file(LOC_METRIC_OUTPUT_PATH, LOC_RESULTS)

check_metric_with_threshold(CC_RESULTS, 'CC', CC_THRESHOLD)
check_metric_with_threshold(NPATH_RESULTS, 'N_PATH', NPATH_THRESHOLD)
check_metric_with_threshold(NCSS_RESULTS, 'NCSS', NCSS_THRESHOLD)
check_metric_with_threshold(SIGNS_RESULTS, 'SIGNS', SIGNS_THRESHOLD)
check_metric_with_threshold(LOC_RESULTS, 'LOC', LOC_THRESHOLD)
