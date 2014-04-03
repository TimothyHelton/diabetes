#!/usr/bin/env python


def update():
    date = ['2014/04/02']
    carb = ['42', '7', '45', '14', '45', '2']
    glucose = [['7:36', '110', '-'], ['14:30', '124', '-'],
               ['21:30', '134', '-']]
    insulin_fast = [['5:00', '3'], ['12:00', '3'], ['18:30', '3']]
    insulin_slow = [['0:00', '15']]
    weight = [['169']]

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