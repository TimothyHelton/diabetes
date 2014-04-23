#!/usr/bin/env python


def update():
    date = ['2014/04/22']
    carb = ['42', '14', '47', '14', '33', '2']
    glucose = [['9:05', '93', '-'],
               ['14:48', '107', '-'],
               ['20:42', '126', '-']]
    insulin_fast = [['6:30', '2'],
                    ['12:00', '3'],
                    ['18:30', '2']]
    insulin_slow = [['0:00', '15']]
    weight = [['170']]

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