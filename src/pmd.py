import subprocess
import re
import os
import csv


CYCLOMATIC_PATH = './pmd/config/cyclomatic.xml'
NPATH_COMPLEXITY_PATH = './pmd/config/npath_complexity.xml'
NCSS_PATH = './pmd/config/ncss.xml'

CYCLOMATIC_REGEX = r' has a cyclomatic complexity of \d*'
NPATH_COMPLEXITY_REGEX = r'has an NPath complexity of \d*'
NCSS_REGEX = r'has a NCSS line count of \d*'

CYCLOMATIC_OUTPUT_PATH = 'pmd\cyclomatic_metric_results.csv'
NPATH_OUTPUT_PATH = 'pmd/npath_metric_results.csv'
NCSS_OUTPUT_PATH = 'pmd/ncss_metric_results.csv'

SRC_PATH = '../../code-quality-benchmark/src/'

results = []

selected_metric_path = ''
selected_metric_regex = ''
selected_metric_output_path = ''


def get_clean_result_object():
    return {
        "file_name": '',
        "human_assessment": 0,
        "metric_before": 0,
        "metric_after": 0,
        "metric_correct": 0,
        "metric_bad": 0,
        "metric_same": 0
    }


def calc_metric_with_checkstyle(file_name):
    command = 'pmd.bat -d ' + ' ' + SRC_PATH + file_name + ' -R ' + selected_metric_path + ' -f textcolor'
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    o, e = proc.communicate()
    metric_result = re.findall(selected_metric_regex, o.decode('ascii'))
    if len(metric_result) == 0:
        return '0'
    result_in_array = metric_result[0].split(' ')
    return result_in_array[len(result_in_array) - 1]


def process_result(single_result):
    single_result['metric_correct'] = 1 if single_result['metric_before'] > single_result['metric_after'] else 0
    single_result['metric_bad'] = 1 if single_result['metric_before'] < single_result['metric_after'] else 0
    single_result['metric_same'] = 1 if single_result['metric_before'] == single_result['metric_after'] else 0


def convert_to_csv_and_save():
    metric_results_file = open(selected_metric_output_path, 'w', newline='')
    csvwriter = csv.writer(metric_results_file)
    csvwriter.writerow(results[0].keys())
    print(results)
    for single_result in results:
        csvwriter.writerow(single_result.values())
    metric_results_file.close()


def list_all_files():
    for r, d, f in os.walk(SRC_PATH):
        counter = 0
        current_search = get_clean_result_object()
        for file in f:
            if counter == 2:
                counter = 0
                process_result(current_search)
                results.append(current_search)
                # print(current_search)
                current_search = get_clean_result_object()
            counter += 1
            read_file(SRC_PATH + file, file, current_search)
        process_result(current_search)
        results.append(current_search)


def set_human_assessment(line, file_name, current_search):
    is_after = re.search(r'after', line)
    is_better = re.search(r'Better', file_name)
    if is_after and is_better:
        current_search['human_assessment'] = 1
    metric = calc_metric_with_checkstyle(file_name)
    if is_after:
        current_search['metric_after'] = metric
    else:
        current_search['metric_before'] = metric


def read_file(file_path, file_name, current_search):
    with open(file_path, 'r', encoding='utf8') as file:
        line = file.readline()
        original_file_name = re.search(r'\d{8}.txt', line).group(0)
        current_search['file_name'] = original_file_name
        set_human_assessment(file.readline(), file_name, current_search)


def set_selected_paths(metric):
    global selected_metric_path
    global selected_metric_regex
    global selected_metric_output_path
    if metric == 'CC':
        selected_metric_path = CYCLOMATIC_PATH
        selected_metric_regex = CYCLOMATIC_REGEX
        selected_metric_output_path = CYCLOMATIC_OUTPUT_PATH
    if metric == 'NPATH':
        selected_metric_path = NPATH_COMPLEXITY_PATH
        selected_metric_regex = NPATH_COMPLEXITY_REGEX
        selected_metric_output_path = NPATH_OUTPUT_PATH
    if metric == 'NCSS':
        selected_metric_path = NCSS_PATH
        selected_metric_regex = NCSS_REGEX
        selected_metric_output_path = NCSS_OUTPUT_PATH


set_selected_paths('NPATH')
list_all_files()
convert_to_csv_and_save()
