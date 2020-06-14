import re
import os
import csv


SRC_PATH = '../../code-quality-benchmark/src/'

results = []

selected_metric_output_path = 'signs-metric/signs_metric_results.csv'


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


def calc_metric(file_content):
    file_content = re.sub(r'\s', '', file_content)
    file_content = re.sub(r'\n', '', file_content)
    return len(file_content)


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


def set_human_assessment(file, line, file_name, current_search):
    is_after = re.search(r'after', line)
    is_better = re.search(r'Better', file_name)
    if is_after and is_better:
        current_search['human_assessment'] = 1
    file.readline()  # class name
    file_content = file.read()
    metric = calc_metric(file_content)
    if is_after:
        current_search['metric_after'] = metric
    else:
        current_search['metric_before'] = metric


def read_file(file_path, file_name, current_search):
    with open(file_path, 'r', encoding='utf8') as file:
        line = file.readline()
        original_file_name = re.search(r'\d{8}.txt', line).group(0)
        current_search['file_name'] = original_file_name
        set_human_assessment(file, file.readline(), file_name, current_search)


list_all_files()
convert_to_csv_and_save()
