#Example usage:
# python plot_log_data.py model_additional_wavs_1/

import sys
from matplotlib import pyplot as plt

train_metrics = {'loss':[], 'train-TER':[], 'train-WER':[], 'val.lst-TER':[], 'val.lst-WER':[], 'val.lst-loss':[]}
test_metrics = {'WER':[], 'TER':[], 'total WER':[], 'total TER':[]}

# Train log
f_train = open(sys.argv[1] + '/001_log', 'r')

for line in f_train.readlines():
    line_list = line.split("|")

    for metric in line_list:
        metric = metric.split()
        key_m = metric[0][:-1]
        try:
            value_m = float(metric[1])
            train_metrics[key_m].append(value_m)
        except (KeyError, ValueError):
            continue
f_train.close()

# Test log
f_test = open(sys.argv[1] + '/001_test_log', 'r')

for line in f_test.readlines():
    if not str(line).startswith('['):
        continue
    line_list = line.split(",")
    for l in line_list:
        key_m = l.split(":")[0][1:]
        if l.split(":")[1].endswith('%'):
            value_m = float(l.split(":")[1][:-1])
        try:
            test_metrics[key_m].append(value_m)
        except KeyError:
            continue

f_test.close()

fig_cnt = 1

def plot_metrics(metrics, add_title='', graph_color='blue'):
    global fig_cnt
    for i, key in enumerate(metrics):
        #plt.figure(i+1)
        plt.figure(fig_cnt)
        plt.plot(metrics[key], color=graph_color)

        plt.ylabel(key)
        plt.xlabel('iteration')
        plt.title(key + add_title)

        fig_cnt += 1

plot_metrics(train_metrics, ' (training)')
plot_metrics(test_metrics, ' (testing)', 'green')

plt.show()
