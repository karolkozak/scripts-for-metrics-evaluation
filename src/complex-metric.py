import csv

CHECKSTYLE_CYCLOMATIC_OUTPUT_PATH = 'checkstyle/cyclomatic_metric_results.csv'
CHECKSTYLE_NPATH_OUTPUT_PATH = 'checkstyle/npath_metric_results.csv'
CHECKSTYLE_NCSS_OUTPUT_PATH = 'checkstyle/ncss_metric_results.csv'
SINGS_METRIC_OUTPUT_PATH = 'signs-metric/signs_metric_results.csv'
LOC_METRIC_OUTPUT_PATH = 'loc-metric/loc_metric_results.csv'

CC_RESULTS = []
NCSS_RESULTS = []
NPATH_RESULTS = []
SIGNS_RESULTS = []
LOC_RESULTS = []


def get_clean_result_object():
    return {
        "file_name": '',
        "human_assessment": 0,
        "metric_before": 0,
        "metric_after": 0,
        "metric_correct": 0,
        "metric_bad": 0
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
        result_object["metric_correct"] = row[4]
        result_object["metric_bad"] = row[5]
        results_array.append(result_object)
    metric_results_file.close()


WE_1 = 0
WE_2 = 0
WEIGHT_1 = 0
WEIGHT_2 = 0
WEIGHT_3 = 0
def calc_weights():
    global WEIGHT_1
    global WEIGHT_2
    global WEIGHT_3
    global WE_1
    global WE_2
    sum_SIGNS_before = 0
    sum_SINGS_after = 0
    sum_NCSS_before = 0
    sum_NCSS_after = 0
    sum_LOC_before = 0
    sum_LOC_after = 0
    for i in range(len(CC_RESULTS)):
        sum_SIGNS_before += int(SIGNS_RESULTS[i]["metric_before"])
        sum_SINGS_after += int(SIGNS_RESULTS[i]["metric_after"])
        sum_LOC_before += int(LOC_RESULTS[i]["metric_before"])
        sum_LOC_after += int(LOC_RESULTS[i]["metric_after"])
        sum_NCSS_before += int(NCSS_RESULTS[i]["metric_before"])
        sum_NCSS_after += int(NCSS_RESULTS[i]["metric_after"])
    delta_SIGNS = abs(sum_SINGS_after - sum_SIGNS_before) / sum_SIGNS_before
    delta_LOC = abs(sum_LOC_after - sum_LOC_before) / sum_LOC_before
    delta_NCSS = abs(sum_NCSS_after - sum_NCSS_before) / sum_NCSS_before
    print("Delta SIGNS: ", delta_SIGNS)
    print("Delta LOC: ", delta_LOC)
    print("Delta NCSS: ", delta_NCSS)

    WE_1 = delta_LOC/(delta_LOC + delta_NCSS)
    WE_2 = delta_NCSS/(delta_LOC + delta_NCSS)
    print("alfa SIGNS", WE_1)
    print("alfa NCSS", WE_2)
    calc_complex_metric(LOC_RESULTS, NCSS_RESULTS, len(SIGNS_RESULTS), "smart weighted", metric_weighted)

    WE_1 = delta_SIGNS/(delta_SIGNS + delta_NCSS)
    WE_2 = delta_NCSS/(delta_SIGNS + delta_NCSS)
    print("alfa SIGNS", WE_1)
    print("alfa NCSS", WE_2)
    calc_complex_metric(SIGNS_RESULTS, NCSS_RESULTS, len(SIGNS_RESULTS), "smart weighted", metric_weighted)

    WE_1 = delta_LOC/(delta_LOC + delta_NCSS)
    WE_2 = delta_NCSS/(delta_LOC + delta_NCSS)
    print("alfa SIGNS", WE_1)
    print("alfa NCSS", WE_2)
    calc_complex_metric(LOC_RESULTS, NCSS_RESULTS, len(SIGNS_RESULTS), "smart weighted", metric_weighted)

    WEIGHT_1 = delta_SIGNS/(delta_SIGNS + delta_NCSS + delta_LOC)
    WEIGHT_2 = delta_LOC/(delta_SIGNS + delta_NCSS + delta_LOC)
    WEIGHT_3 = delta_NCSS/(delta_SIGNS + delta_NCSS + delta_LOC)
    print("alfa SIGNS 3m", delta_SIGNS/(delta_SIGNS + delta_NCSS + delta_LOC))
    print("alfa LOC 3m", delta_LOC/(delta_SIGNS + delta_NCSS + delta_LOC))
    print("alfa NCSS 3m", delta_NCSS/(delta_SIGNS + delta_NCSS + delta_LOC))
    calc_complex_metric_3m(SIGNS_RESULTS, LOC_RESULTS, NCSS_RESULTS, len(NCSS_RESULTS), "smart weighted 3m", metric_weighted_3m)


def check_metric_sum():
    result = 0
    for i in range(len(CC_RESULTS)):
        if CC_RESULTS[i]["human_assessment"] == '1' and CC_RESULTS[i]["metric_correct"] == '1':
            result += 1
        elif CC_RESULTS[i]["human_assessment"] == '0' and CC_RESULTS[i]["metric_bad"] == '1':
            result += 1
    print(result)


def calc_complex_metric(metric_one, metric_two, results_len, complex_name, func):
    complex_result = 0
    for i in range(results_len):
        complex_before = func(int(metric_one[i]["metric_before"]), int(metric_two[i]["metric_before"]))
        complex_after = func(int(metric_one[i]["metric_after"]), int(metric_two[i]["metric_after"]))
        before_better = complex_after > complex_before
        after_better = complex_after < complex_before
        if metric_one[i]["human_assessment"] == '1' and after_better is True:
            complex_result += 1
        elif metric_one[i]["human_assessment"] == '0' and before_better is True:
            complex_result += 1
    print(complex_name, " matches human (%): ", complex_result * 100 / results_len)


def calc_complex_result_metric(metric_one, metric_two, results_len, complex_name, func):
    complex_result = 0
    for i in range(results_len):
        complex_one = func(int(metric_one[i]["metric_correct"]), int(metric_two[i]["metric_correct"]))
        if metric_one[i]["human_assessment"] == '1' and complex_one is False:
            complex_result += 1
    print(complex_name, " matches human (%): ", complex_result * 100 / results_len)


def calc_complex_metric_3m(metric_one, metric_two, metric_three, results_len, complex_name, func):
    complex_result = 0
    for i in range(results_len):
        complex_before = func(int(metric_one[i]["metric_before"]), int(metric_two[i]["metric_before"]), int(metric_three[i]["metric_before"]))
        complex_after = func(int(metric_one[i]["metric_after"]), int(metric_two[i]["metric_after"]), int(metric_three[i]["metric_after"]))
        before_better = complex_after > complex_before
        after_better = complex_after < complex_before
        if metric_one[i]["human_assessment"] == '1' and after_better is True:
            complex_result += 1
        elif metric_one[i]["human_assessment"] == '0' and before_better is True:
            complex_result += 1
    print(complex_name, " matches human (%): ", complex_result * 100 / results_len)


def metric_sum(val_1, val_2):
    return val_1 + val_2


def metric_sum_3m(val_1, val_2, val_3):
    return val_1 + val_2 + val_3


# WE_1 = 0.5
# WE_2 = 0.5
def metric_weighted(val_1, val_2):
    return WE_1 * val_1 + WE_2 * val_2


# WEIGHT_1 = 0.7
# WEIGHT_2 = 0.3
# WEIGHT_3 = 0.3
def metric_weighted_3m(val_1, val_2, val_3):
    return WEIGHT_1 * val_1 + WEIGHT_2 * val_2 + WEIGHT_3 * val_3


def metric_and_not(val_1, val_2):
    val_1_truth = val_1 == 1
    val_2_truth = val_2 == 1
    return val_1_truth and val_2_truth


def metric_xor(val_1, val_2):
    val_1_truth = val_1 == 1
    val_2_truth = val_2 == 1
    return (val_1_truth or val_2_truth) and not (val_1_truth and val_2_truth)


read_file(CHECKSTYLE_CYCLOMATIC_OUTPUT_PATH, CC_RESULTS)
read_file(CHECKSTYLE_NCSS_OUTPUT_PATH, NCSS_RESULTS)
read_file(CHECKSTYLE_NPATH_OUTPUT_PATH, NPATH_RESULTS)
read_file(SINGS_METRIC_OUTPUT_PATH, SIGNS_RESULTS)
read_file(LOC_METRIC_OUTPUT_PATH, LOC_RESULTS)

# Smart weighted metrics
calc_weights()

examples_length = len(CC_RESULTS)
print("Number of examples: ", examples_length)
calc_complex_metric(CC_RESULTS, NPATH_RESULTS, examples_length, "'CC + N_PATH'", metric_sum)
calc_complex_metric(CC_RESULTS, NCSS_RESULTS, examples_length, "'CC + NCSS'", metric_sum)
calc_complex_metric(CC_RESULTS, LOC_RESULTS, examples_length, "'CC + LOC'", metric_sum)
calc_complex_metric(CC_RESULTS, SIGNS_RESULTS, examples_length, "'CC + SIGNS'", metric_sum)
calc_complex_metric(NPATH_RESULTS, NCSS_RESULTS, examples_length, "'N_PATH + NCSS'", metric_sum)
calc_complex_metric(NPATH_RESULTS, LOC_RESULTS, examples_length, "'N_PATH + LOC'", metric_sum)
calc_complex_metric(NPATH_RESULTS, SIGNS_RESULTS, examples_length, "'N_PATH + SIGNS'", metric_sum)
calc_complex_metric(NCSS_RESULTS, LOC_RESULTS, examples_length, "'NCSS + LOC'", metric_sum)
calc_complex_metric(NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'NCSS + SIGNS'", metric_sum)
calc_complex_metric(LOC_RESULTS, SIGNS_RESULTS, examples_length, "'LOC + SIGNS'", metric_sum)
print("Sum of three metrics")
calc_complex_metric_3m(CC_RESULTS, NPATH_RESULTS, NCSS_RESULTS, examples_length, "'CC + N_PATH + NCSS'", metric_sum_3m)
calc_complex_metric_3m(CC_RESULTS, NPATH_RESULTS, LOC_RESULTS, examples_length, "'CC + N_PATH + LOC'", metric_sum_3m)
calc_complex_metric_3m(CC_RESULTS, NPATH_RESULTS, SIGNS_RESULTS, examples_length, "'CC + N_PATH + SIGNS'", metric_sum_3m)
calc_complex_metric_3m(CC_RESULTS, NCSS_RESULTS, LOC_RESULTS, examples_length, "'CC + NCSS + LOC'", metric_sum_3m)
calc_complex_metric_3m(CC_RESULTS, NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'CC + NCSS + SIGNS'", metric_sum_3m)
calc_complex_metric_3m(CC_RESULTS, LOC_RESULTS, SIGNS_RESULTS, examples_length, "'CC + LOC + SIGNS'", metric_sum_3m)
calc_complex_metric_3m(NPATH_RESULTS, NCSS_RESULTS, LOC_RESULTS, examples_length, "'N_PATH + NCSS + LOC'", metric_sum_3m)
calc_complex_metric_3m(NPATH_RESULTS, NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'N_PATH + NCSS + SIGNS'", metric_sum_3m)
calc_complex_metric_3m(NCSS_RESULTS, LOC_RESULTS, SIGNS_RESULTS, examples_length, "'NCSS + LOC + SIGNS'", metric_sum_3m)
print("Weighted complex metric")
calc_complex_metric(CC_RESULTS, NPATH_RESULTS, examples_length, "'W_1 * CC + W_2 * N_PATH'", metric_weighted)
calc_complex_metric(CC_RESULTS, NCSS_RESULTS, examples_length, "'W_1 * CC + W_2 * NCSS'", metric_weighted)
calc_complex_metric(CC_RESULTS, LOC_RESULTS, examples_length, "'W_1 * CC + W_2 * LOC'", metric_weighted)
calc_complex_metric(CC_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * CC + W_2 * SIGNS'", metric_weighted)
calc_complex_metric(NPATH_RESULTS, NCSS_RESULTS, examples_length, "'W_1 * N_PATH + W_2 * NCSS'", metric_weighted)
calc_complex_metric(NPATH_RESULTS, LOC_RESULTS, examples_length, "'W_1 * N_PATH + W_2 * LOC'", metric_weighted)
calc_complex_metric(NPATH_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * N_PATH + W_2 * SIGNS'", metric_weighted)
calc_complex_metric(NCSS_RESULTS, LOC_RESULTS, examples_length, "'W_1 * NCSS + W_2 * LOC'", metric_weighted)
calc_complex_metric(NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * NCSS + W_2 * SIGNS'", metric_weighted)
calc_complex_metric(LOC_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * LOC + W_2 * SIGNS'", metric_weighted)

print("Weighted of three metrics")
calc_complex_metric_3m(CC_RESULTS, NPATH_RESULTS, NCSS_RESULTS, examples_length, "'W_1 * CC + W_2 * N_PATH + W_3 * NCSS'", metric_weighted_3m)
calc_complex_metric_3m(CC_RESULTS, NPATH_RESULTS, LOC_RESULTS, examples_length, "'W_1 * CC + W_2 * N_PATH + W_3 * LOC'", metric_weighted_3m)
calc_complex_metric_3m(CC_RESULTS, NPATH_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * CC + W_2 * N_PATH + W_3 * SIGNS'", metric_weighted_3m)
calc_complex_metric_3m(CC_RESULTS, NCSS_RESULTS, LOC_RESULTS, examples_length, "'W_1 * CC + W_2 * NCSS + W_3 * LOC'", metric_weighted_3m)
calc_complex_metric_3m(CC_RESULTS, NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * CC + W_2 * NCSS + W_3 * SIGNS'", metric_weighted_3m)
calc_complex_metric_3m(CC_RESULTS, LOC_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * CC + W_2 * LOC + W_3 * SIGNS'", metric_weighted_3m)
calc_complex_metric_3m(NPATH_RESULTS, NCSS_RESULTS, LOC_RESULTS, examples_length, "'W_1 * N_PATH + W_2 * NCSS + W_3 * LOC'", metric_weighted_3m)
calc_complex_metric_3m(NPATH_RESULTS, NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * N_PATH + W_2 * NCSS + W_3 * SIGNS'", metric_weighted_3m)
calc_complex_metric_3m(NCSS_RESULTS, LOC_RESULTS, SIGNS_RESULTS, examples_length, "'W_1 * NCSS + W_2 * LOC + W_3 * SIGNS'", metric_weighted_3m)

print("Complex")
calc_complex_result_metric(SIGNS_RESULTS, CC_RESULTS, examples_length, "'SIGNS_CORRECT && CC_BAD'", metric_and_not)
calc_complex_result_metric(SIGNS_RESULTS, NCSS_RESULTS, examples_length, "'SIGNS_CORRECT && NCSS_BAD'", metric_and_not)
calc_complex_result_metric(SIGNS_RESULTS, NPATH_RESULTS, examples_length, "'SIGNS_CORRECT && NPATH_BAD'", metric_and_not)
calc_complex_result_metric(LOC_RESULTS, CC_RESULTS, examples_length, "'LOC_CORRECT && CC_BAD'", metric_and_not)
calc_complex_result_metric(LOC_RESULTS, NCSS_RESULTS, examples_length, "'LOC_CORRECT && NCSS_BAD'", metric_and_not)
calc_complex_result_metric(LOC_RESULTS, NPATH_RESULTS, examples_length, "'LOC__CORRECT && NPATH_BAD'", metric_and_not)

print("Xor")
calc_complex_result_metric(CC_RESULTS, NPATH_RESULTS, examples_length, "'!(CC xor N_PATH)'", metric_xor)
calc_complex_result_metric(CC_RESULTS, NCSS_RESULTS, examples_length, "'!(CC xor NCSS'", metric_xor)
calc_complex_result_metric(CC_RESULTS, LOC_RESULTS, examples_length, "'!(CC xor LOC'", metric_xor)
calc_complex_result_metric(CC_RESULTS, SIGNS_RESULTS, examples_length, "'!(CC xor SIGNS'", metric_xor)
calc_complex_result_metric(NPATH_RESULTS, NCSS_RESULTS, examples_length, "'!(N_PATH xor NCSS'", metric_xor)
calc_complex_result_metric(NPATH_RESULTS, LOC_RESULTS, examples_length, "'!(N_PATH xor LOC'", metric_xor)
calc_complex_result_metric(NPATH_RESULTS, SIGNS_RESULTS, examples_length, "'!(N_PATH xor SIGNS'", metric_xor)
calc_complex_result_metric(NCSS_RESULTS, LOC_RESULTS, examples_length, "'!(NCSS xor LOC'", metric_xor)
calc_complex_result_metric(NCSS_RESULTS, SIGNS_RESULTS, examples_length, "'!(NCSS xor SIGNS'", metric_xor)
calc_complex_result_metric(LOC_RESULTS, SIGNS_RESULTS, examples_length, "'!(LOC xor SIGNS'", metric_xor)
