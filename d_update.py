#!/usr/bin/env python


def update():
    date = ['2014/05/14']
    carb = ['42', '7', '36', '14', '36', '2']
    glucose = [['9:37', '80', '-'],
               ['14:05', '131', '-'],
               ['22:03', '115', '-']]
    insulin_fast = [['6:40', '2'],
                    ['12:05', '2'],
                    ['18:40', '2']]
    insulin_slow = [['0:00', '15']]
    weight = [['171']]

    carb_name = ['breakfast', 'morning_snack', 'lunch', 'afternoon_snack',
                 'dinner', 'evening_snack']
    carb_log = []
    for i in range(6):
        carb_log.append([carb_name[i], carb[i]])
    insulin = [x + ['bolus'] for x in insulin_fast] + \
              [x + ['basal'] for x in insulin_slow]

    update_list = ['carb_log', 'glucose', 'insulin', 'weight']
    for f in update_list:
        for level in eval(f):
            if '' in level:
                update_list.remove(f)

    for data_file in update_list:
        f_in = open(data_file + '.dat', 'a')
        for item in eval(data_file):
            f_in.write('\n' + '\t'.join(date + item))
        f_in.close()
        print('Updated File:\t' + data_file + '.dat')


def main():
    update()

if __name__ == '__main__':
    main()