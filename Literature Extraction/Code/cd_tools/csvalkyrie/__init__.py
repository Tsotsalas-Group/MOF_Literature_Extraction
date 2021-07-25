import os
import csv
import cd_tools

lgrd = cd_tools.lgrd


def add_colum(csv_loca, add_posi, colum_title, colum_cont):
    csv_loca_temp = csv_loca[:csv_loca.rfind(".csv")] + "_temp.csv"
    with open(csv_loca) as inf, open(csv_loca_temp, 'w') as outf:
        reader = csv.reader(inf, delimiter=',')
        writer = csv.writer(outf, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        title_line = 1
        colum_cont_len = 0
        for line in reader:
            if title_line == 1 and colum_title != '':
                line.insert(add_posi, colum_title)
                title_line = 0
            else:
                if isinstance(colum_cont, (str, int, float)):
                    line.insert(add_posi, colum_cont)
                elif isinstance(colum_cont, (list, tuple)):
                    line.insert(add_posi, colum_cont[colum_cont_len % len(colum_cont)])
                    colum_cont_len = colum_cont_len + 1
            writer.writerow(line)
    os.remove(csv_loca)
    os.rename(csv_loca_temp, csv_loca)


def del_colum(csv_loca, del_posi):
    csv_loca_temp = csv_loca[:csv_loca.rfind(".csv")] + "_temp.csv"
    try:
        with open(csv_loca) as inf, open(csv_loca_temp, 'w') as outf:
            reader = csv.reader(inf, delimiter=',')
            writer = csv.writer(outf, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            title_line = 1
            for line in reader:
                if title_line == 1:
                    assert del_posi <= len(line), 'del_posi is too large'
                    line = line[:del_posi] + line[del_posi + 1:]
                    title_line = 0
                else:
                    line = line[:del_posi] + line[del_posi + 1:]
                writer.writerow(line)
    except AssertionError as err:
        lgrd.error(err)
        os.remove(csv_loca_temp)
    else:
        os.remove(csv_loca)
        os.rename(csv_loca_temp, csv_loca)


def change_state(csv_loca, title_sign_numb, row_numb, change_cont):
    csv_location_temp = csv_loca[:csv_loca.rfind(".csv")] + "_temp.csv"
    with open(csv_loca) as inf, open(csv_location_temp, 'w') as outf:
        reader = csv.reader(inf, delimiter=',')
        writer = csv.writer(outf, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        title = 0
        row = 0
        for line in reader:

            if not isinstance(title_sign_numb, int):
                if title == 0:
                    targ_colum = line.index(str(title_sign_numb))
                    title = 1
            else:
                targ_colum = int(title_sign_numb)

            if row == row_numb:
                line[targ_colum] = str(change_cont)
                writer.writerow(line)
            else:
                writer.writerow(line)
            row += 1
    os.remove(csv_loca)
    os.rename(csv_location_temp, csv_loca)


def item_reader(csv_loca, title_sign_numb, row_numb):
    with open(csv_loca) as inf:
        reader = csv.reader(inf, delimiter=',')

        title = 0
        row = 0
        for line in reader:

            if not isinstance(title_sign_numb, int):
                if title == 0:
                    targ_colum = line.index(str(title_sign_numb))
                    title = 1
            else:
                targ_colum = int(title_sign_numb)

            if row == row_numb:
                return [True, line[targ_colum]]
            elif row > row_numb:
                return [False, 'stop']
            row += 1
        return [False, 'stop']


def title_finder(csv_loca, title_cont):
    with open(csv_loca) as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            try:
                assert isinstance(title_cont, str), 'title_cont inside sv_title_finder should be str'
                title_posi = line.index(title_cont)
            except AssertionError as err:
                lgrd.error(err)
                return [False, None]
            except ValueError:
                return [False, None]
            else:
                return [True, title_posi]


def row_count(csv_loca):
    with open(csv_loca) as inf:
        reader = csv.reader(inf, delimiter=',')
        i = 0
        for line in reader:
            i += 1
        return i


def copy_new(orig_csv_loca, noe_csv_loca, colums):
    with open(orig_csv_loca) as inf, open(noe_csv_loca, 'w') as outf:
        reader = csv.reader(inf, delimiter=',')
        writer = csv.writer(outf, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for line in reader:
            noe_line = []
            for colum in colums:
                noe_line.append(line[int(colum)])
            writer.writerow(noe_line)
