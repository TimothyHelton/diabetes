#!/usr/bin/env python

import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os
import shutil


def create_file(new_file, new_header):
    """ Method will create a new file
    """
    f = open(new_file, 'w')
    f.write(new_header)
    f.close()


def text_data():
    """ Method will collect all formatting regarding data files
    """
    file_list = ['a1c.dat', 'carb_log.dat', 'food_index.dat', 'glucose.dat',
                 'insulin.dat', 'supplies.dat', 'weight.dat']

    class_list = ['A1c', 'Carb', 'Food', 'Glucose', 'Insulin', 'Supplies',
                  'Weight']

    title_list = ['Hemoglobin A1c Log', 'Carbohydrate Log', 'Food Index',
                  'Blood Glucose Log', 'Insulin Log', 'Supplies List',
                  'Weight Log']

    header_list = [['# Date', 'A1C'],
                   ['# Date', 'Meal', 'Carbohydrates'],
                   ['#Name', 'Unit of Measure', 'Standard Quantity',
                    'Carbohydrates'],
                   ['# Date', 'Time', 'Glucose Level', 'Meal'],
                   ['# Date', 'Time', 'Insulin', 'Type'],
                   ['# Item', 'Description', 'Unit of Measure',
                    'Quantity Per Month', 'Price Per Month (USD)'],
                   ['# Date', 'Weight']]

    header_list = ['\t'.join(x) for x in header_list]

    meal_list = ['[B]reakfast', '[M]orning Snack', '[L]unch',
                 '[A]fternoon Snack', '[D]inner', '[E]vening Snack']

    prompt_list = [['Enter Date (Year/Month/Day):\t',
                   'Enter A1c Value:\t'],
                  ['Enter Date (Year/Month/Day):\t',
                   'Enter Meal (' + ' '.join(meal_list) + '):\t',
                   'Number of Net Carbohydrates (grams):\t'],
                  ['Enter Food Name:\t',
                   'Enter Unit of Measure:\t',
                   'Enter Standard Quantity:\t',
                   'Enter Carbohydrates (grams):\t',
                   'Enter Dietary Fiber (grams):\t'],
                  ['Enter Date (Year/Month/Day):\t',
                   'Enter 24 Hour Clock Time (HH:MM):\t',
                   'Enter Glucose Level (mg/dl):\t',
                   'Enter Meal (' + ' '.join(meal_list) + '):\t',
                   'Did you take insulin at this time? ([Y]es/[N]o)\t',
                   'Enter Insulin Dose (Units):\t'],
                  ['Enter Date (Year/Month/Day):\t',
                   'Enter 24 Hour Clock Time (HH:MM):\t',
                   'Enter Insulin (Units):\t',
                   'Enter Insulin Type ([BA]sal/[BO]lus:\t'],
                  ['Enter Item:\t',
                   'Enter Description:\t',
                   'Enter Unit of Measure:\t',
                   'Enter Quantity Per Month:\t',
                   'Enter Price Per Month (USD):\t'],
                  ['Enter Date (Year/Month/Day):\t',
                   'Enter Weight (pounds):\t']]

    short_cut_dict = {'b': 'breakfast', 'm': 'morning_snack', 'l': 'lunch',
                      'a': 'afternoon_snack', 'd': 'dinner',
                      'e': 'evening_snack', 'ba': 'basal', 'bo': 'bolus',
                      'y': 'yes', 'n': 'no'}

    master_list = zip(file_list, class_list, title_list, header_list,
                      prompt_list)

    selection_dict = {'e': ' '}
    for (file_name, class_name, title, header, prompts) in master_list:
        if not os.path.exists(file_name):
            create_file(file_name, header)
        selection_dict[file_name[0]] = [file_name, prompts]

    return [master_list, short_cut_dict, selection_dict, file_list]


def read_file(input_file):
    """ Method will read data file and return lines
    """
    f_in = open(input_file, 'rb')
    lines = f_in.readlines()[1:]
    f_in.close()

    return lines


def return_date(date):
    """ Method will store text data as a Date
    """
    (y, m, d) = date.split('/')
    (y, m, d) = [int(x) for x in (y, m, d)]

    return datetime.datetime(y, m, d, 0, 0)


def return_date_time(date, time):
    """ Method will store text data as a Date & Time
    """
    (y, mon, d) = date.split('/')
    (h, m) = time.split(':')
    (y, mon, d, h, m) = [int(x) for x in (y, mon, d, h, m)]

    return datetime.datetime(y, mon, d, h, m)


def update_prompt(sel_dict):
    """ Method will process the input provided by user
    """
    file_prompt = raw_input('\nEnter the data file you would like to update:'
                            '\n([A]1c Log, [C]arbohydrate Log, [F]ood Index, '
                            '[G]lucose Log, [I]nsulin Log, [S]upply List, '
                            '[W]eight Log or [E]scape):\t').lower()
    try:
        update_file = sel_dict[file_prompt[0]]
    except KeyError:
        print('\n\n******* Unexpected Input!!! *******\n'
              'Please select a file to update from the provided list\n')
        update_file = ' '
        update_prompt(sel_dict)

    return update_file


def prompt_user(short_dict, sel_dict):
    """ Gather inputs from the user
    """
    add_prompt = raw_input('\nWould you like to add new data?'
                           '\n([Y]es/[N]o):\t').lower()
    # Prompt user for inputs and save entries to the appropriate file
    while add_prompt != 'n':
        update_select = update_prompt(sel_dict)

        update_list = []
        if update_select != ' ':
            for entry in update_select[1]:
                print '\n'
                update_list.append(raw_input(entry).lower())
                update_list = [short_dict[x] if x in short_dict.keys()
                               else x for x in update_list]
            update_file = open(update_select[0], 'a')
            update_file.write('\n')
            update_file.write('\t\t'.join(update_list))
            update_file.close()
        else:
            add_prompt = 'n'

        add_prompt2 = 'y'
        if add_prompt != 'n':
            add_prompt2 = raw_input('\nWould you like to add more new data?'
                                    '\n([Y]es/[N]o):\t').lower()
            print '\n'
        if add_prompt == 'n' or add_prompt2 == 'n':
            add_prompt = 'n'


def load_data(name_file, class_name, status_str):
    """ Method will read input file
    """
    f_in = read_file(name_file)
    data = []
    print('*******\nReading ' + status_str + ' File\n*******\n')
    for load_line in f_in:
        instance = eval(class_name + '(*load_line.split())')

        try:
            data.append(instance)
        except AttributeError:
            continue

    return [data]


class A1c:
    """ Class to generate instances of A1c measurements
    """
    def __init__(self, a1c_date, a1c_value):
        self.date = return_date(a1c_date)
        self.value = a1c_value

    def __str__(self):
        return ('Date:' + '\t'*3 + str(self.date) + '\n' +
                'Hemoglobin A1c:\t' + self.value + '\n' +
                'eAG:' + '\t'*3 + self.calc_e_ag() + '\n')

    def calc_e_ag(self):
        """ Method will calculate average glucose from A1c measurement in
            units of mg/dl
        """
        e_ag = str((28.7*float(self.value)) - 46.7)

        return e_ag


class Carb:
    """ Class to generate instances of meal carbohydrate
    """
    def __init__(self, carb_date, carb_meal, carbohydrates):
        self.date = carb_date
        self.meal = carb_meal
        self.value = carbohydrates

    def __str__(self):
        return ('Date:' + '\t'*3 + str(self.meal_time()) + '\n' +
                'Meal:' + '\t'*3 + self.meal + '\n' +
                'Carbohydrates:\t' + self.value + ' grams\n')
    
    def meal_time(self):
        """ Method will assign standard times to meals
        """
        meal_dict = {'breakfast': '6:30', 'morning_snack': '9:00',
                     'lunch': '12:00', 'afternoon_snack': '15:00',
                     'dinner': '18:30', 'evening_snack': '20:00'}

        return return_date_time(self.date, meal_dict[self.meal])


class Food:
    """ Class to generate instances of food measurements
    """
    def __init__(self, food_name, unit_of_measure, standard_quantity,
                 total_carbohydrates, dietary_fiber):
        self.name = food_name
        self.uom = unit_of_measure
        self.std_qty = standard_quantity
        self.tot_carbs = total_carbohydrates
        self.fiber = dietary_fiber

    def __str__(self):
        return ('Name of Food:' + '\t'*2 + self.name + '\n' +
                'Unit of Measure:' + '\t'*2 + self.uom + '\n' +
                'Standard Quantity:' + '\t'*2 + self.std_qty + '\n' +
                'Total Carbohydrates:' + '\t' + self.tot_carbs + '\n' +
                'Dietary Fibers:' + '\t'*2 + self.fiber + '\n' +
                'Net Carbohydrates:' + '\t'*2 + self.net_carb() + '\n')

    def net_carb(self):
        if self.fiber >= 5:
            net_carbs = self.tot_carbs - self.fiber
        else:
            net_carbs = self.tot_carbs

        return net_carbs


class Glucose:
    """ Class to generate instances of glucose measurements
    """
    def __init__(self, glu_date, glu_time, glu_value, glu_meal):
        self.date = return_date_time(glu_date, glu_time)
        self.value = glu_value
        self.meal = glu_meal

    def __str__(self):
        return ('Date:' + '\t'*3 + str(self.date) + '\n' +
                'Glucose Level:' + '\t'*1 + self.value + '\n' +
                'Meal:' + '\t'*3 + self.meal + '\n')


class Insulin:
    """ Class to generate instances of insulin measurements
    """
    def __init__(self, ins_date, ins_time, ins_value, ins_type):
        self.date = return_date_time(ins_date, ins_time)
        self.value = ins_value
        self.type = ins_type

    def __str__(self):
        return ('Date:' + '\t'*4 + str(self.date) + '\n' +
                'Insulin Dose:' + '\t'*2 + self.value + '\n' +
                'Insulin Type:' + '\t'*2 + self.type + '\n')


class Supplies:
    """ Class to generate instances of supplies
    """
    def __init__(self, supplies_item, supplies_description, unit_of_measure,
                 quantity_per_month, price_per_month):
        self.item = supplies_item
        self.description = supplies_description
        self.uom = unit_of_measure
        self.qty_mon = quantity_per_month
        self.price = price_per_month

    def __str__(self):
        return ('Item:' + '\t'*4 + self.item.split() + '\n' +
                'Description:' + '\t'*3 + self.description.split() + '\n' +
                'Unit of Measure:' + '\t'*2 + self.uom + '\n' +
                'Quantity Per Month:' + '\t'*2 + self.qty_mon + '\n' +
                'Price Per Month:' + '\t'*2 + self.price)


class Weight:
    """ Class to generate instances of weight measurements
    """
    def __init__(self, weight_date, weight_value):
        self.date = return_date(weight_date)
        self.value = weight_value

    def __str__(self):
        return ('Date:' + '\t'*2 + str(self.date) + '\n' +
                'Weight:' + '\t'*2 + self.value + '\n')


def plot_gen(data):
    """ Create plots
    """
    title_size = 16
    label_size = 12
    figure_size = (15, 9.5)
    rgb_yellow = (1, 1, 0)
    rgb_green = (0, 1, 0)

    # Plot A1c and Blood Glucose
    x1a = []
    y1a = []
    for obj in data['a1c.dat'][0]:
        x1a.append(obj.date)
        y1a.append(float(obj.calc_e_ag()))
    
    x1b = []
    y1b = []
    for obj in data['glucose.dat'][0]:
        x1b.append(obj.date)
        y1b.append(int(obj.value))

    fig1, ax1 = plt.subplots(1, 1, facecolor='white', figsize=figure_size)
    fig1.canvas.set_window_title('Total Blood Glucose History')
    ax1.plot(x1a, y1a, '-b^', linewidth=2, markersize=5,
             label='eAG (Hemoglobin A1c)')
    ax1.plot(x1b, y1b, '-ro', linewidth=2, markersize=5,
             label='Blood Glucose')

    x1_box = [x1a[0], x1a[0], x1b[-1], x1b[-1]]
    ax1.fill(x1_box, [50, 80, 80, 50], facecolor=rgb_yellow, alpha=0.2)
    ax1.fill(x1_box, [80, 120, 120, 80], facecolor=rgb_green, alpha=0.2)
    ax1.fill(x1_box, [120, 150, 150, 120], facecolor=rgb_yellow, alpha=0.2)

    ax1.set_title('Blood Glucose vs Time\n', fontsize=title_size,
                  fontweight='bold')
    ax1.legend(loc='upper right')

    ax1.set_xlabel('Date\n', fontsize=label_size, fontweight='bold')
    ax1.set_ylabel('Glucose Level [mg/dl]\n', fontsize=label_size,
                   fontweight='bold')
    ax1.set_ylim([25, max(y1b) - max(y1b) % 10 + 20])
    plt.grid(True)
    fig1.autofmt_xdate()
    plt.tight_layout()
    # plt.show()
    plt.savefig('eAG_BG_Total.png')
    plt.close(fig1)

    # Subplot Recent Glucose and Insulin

    # TODO Add daily average markers for blood glucose
    # TODO Create pie chart of time in target zone, secondary zone, and out of zone
    prior_month = datetime.date.today() + relativedelta(months=-1)
    x2a = []
    y2a = []
    for obj in data['glucose.dat'][0]:
        if obj.date.date() >= prior_month:
            x2a.append(obj.date)
            y2a.append(int(obj.value))

    insulin_tot = {}
    insulin_bolus = {}
    for obj in data['insulin.dat'][0]:
        if obj.date.date() in insulin_tot.keys() \
                and obj.date.date() >= prior_month:
            if 'bolus' in obj.type:
                insulin_bolus[obj.date.date()] += int(obj.value)
            insulin_tot[obj.date.date()] += int(obj.value)
        elif obj.date.date() >= prior_month:
            if 'bolus' in obj.type:
                insulin_bolus[obj.date.date()] = int(obj.value)
            insulin_tot[obj.date.date()] = int(obj.value)

    x2b = sorted(insulin_tot.keys())
    y2b_tot = [insulin_tot[x] for x in x2b]
    y2b_bolus = [insulin_bolus[x] for x in x2b]
    y2b_basal = [insulin_tot[x] - insulin_bolus[x] for x in x2b]

    fig2 = plt.figure(facecolor='white', figsize=figure_size)
    fig2.canvas.set_window_title('Previous Month Blood Glucose Levels')

    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
    ax1.plot(x2a, y2a, '-ro', linewidth=2, markersize=5)

    box_begin = x2a[0] + relativedelta(days=-1)
    x2_box = [box_begin, box_begin, x2a[-1], x2a[-1]]
    ax1.fill(x2_box, [50, 80, 80, 50], facecolor=rgb_yellow, alpha=0.2)
    ax1.fill(x2_box, [80, 120, 120, 80], facecolor=rgb_green, alpha=0.2)
    ax1.fill(x2_box, [120, 150, 150, 120], facecolor=rgb_yellow, alpha=0.2)

    ax1.set_title('Blood Glucose vs Time (Recent Month)\n',
                  fontsize=title_size, fontweight='bold')
    ax1.set_ylabel('Glucose Level [mg/dl]\n', fontsize=label_size,
                   fontweight='bold')
    ax1.set_ylim([25, max(y2a) - max(y2a) % 10 + 20])
    ax1.grid(True)

    ax2 = plt.subplot2grid((4, 1), (3, 0), sharex=ax1)
    ax2.plot(x2b, y2b_tot, '-mD', linewidth=2, markersize=5, label='Total')
    ax2.plot(x2b, y2b_bolus, '-g^', linewidth=2, markersize=5, label='Bolus')
    ax2.plot(x2b, y2b_basal, '-bs', linewidth=2, markersize=5, label='Basal')
    ax2.set_title('Insulin vs Time (Recent Month)\n',
                  fontsize=title_size, fontweight='bold')
    ax2.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    ax2.set_ylabel('Units [1/100 ml]\n', fontsize=label_size,
                   fontweight='bold')
    ax2.set_ylim([0, max(y2b_tot) - max(y2b_tot) % 5 + 5])
    ax2.grid(True)

    plt.xlabel('\nDate', fontsize=label_size, fontweight='bold')
    fig2.autofmt_xdate()
    fig2.subplots_adjust(hspace=1, bottom=0.14, right=0.84)
    # plt.show()
    plt.savefig('BG_Insulin_Month.png')
    plt.close(fig2)


def backup(save_list):
    """ Create a backup for each of the data files
    """
    backup_prompt = raw_input('Would you like to save a backup copy of the '
                              'data files? ([Y]es/[N]:\t').lower()
    if backup_prompt == 'y':
        if not os.path.exists('backup_data_files'):
            os.mkdir('backup_data_files')
        print '\n*******'
        for save_file in save_list:
            shutil.copy2(save_file, 'backup_data_files')
            print('Saved Data File:' + save_file)
        print '*******\n'


def main():
    """ Method will call other methods to execute script
    """
    [m_list, short_dic, sel_dic, file_list] = text_data()

    prompt_user(short_dic, sel_dic)

    # data_dict['file_name'] = [[.str], [.date], [.value]]
    data_dict = {}
    
    # Load Data
    for (file_name, class_name, title, header, prompts) in m_list:
        try:
            data_dict[file_name] = (load_data(file_name, class_name, title))
        except TypeError:
            continue

    # Create Plots
    plot_gen(data_dict)
    
    # Backup Files
    backup(file_list)

if __name__ == '__main__':
    main()