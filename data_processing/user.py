import pandas as pd


class User():
    def __init__(self):
        self.interest = None
        self.city = None
        self.df = pd.read_csv('vet-result.csv')
        self.req = None

    def set_interest(self, interest):
        self.interest = interest

    def set_city(self, city):
        self.city = city

    def calculate_interest(self, math, ph, inf, bio, ch, soc, his, lang, geo, pe, creative):
        try:
            math = abs(int(math) % 4)
            ph = abs(int(ph) % 4)
            inf = abs(int(inf) % 4)
            bio = abs(int(bio) % 4)
            ch = abs(int(ch) % 4)
            soc = abs(int(soc) % 4)
            his = abs(int(his) % 4)
            lang = abs(int(lang) % 4)
            geo = abs(int(geo) % 4)
            pe = abs(int(pe) % 4)
            creative = abs(int(creative) % 4)
        except:
            math, ph, inf, bio, ch, soc, his, lang, geo, pe, creative = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        # x_ax = (3*(math + ph + inf + geo) - 1.5*2*(soc - his - lang))
        # y_ax = (4*(bio + ch + geo) - 1.5*3*(pe+creative))
        interest = [(math + ph + inf + geo) / 4.0, (soc + his + lang) / 3.0, (bio + ch + geo) / 3.0,
                    0.8 * (pe + creative) / 2.0]

        if interest[0] == max((interest)):
            self.interest = 'exact'

        elif interest[1] == max((interest)):
            self.interest = 'humanities'

        elif interest[2] == max((interest)):
            self.interest = 'natural'

        elif interest[3] == max((interest)):
            self.interest = 'creative'

    def calculate_professions(self):
        result = []

        with open('number-profession.txt', 'r', encoding='utf-8') as file:
            table = {}
            file.read
            for line in file:
                s = line[:-1].split(';')
                table[s[0]] = [s[1], s[2]]
                # if(s[1] == 'Математика и механика'):
                #  table['01'] = 'Математика и механика'

        for number in parameters[self.interest]:
            result.append([number, table[number]])
        return result

    def get_data(self, x):
        filt = [x[0]] * 59
        for i in range(len(x)):
            filt[i] = x[i]
        t2 = self.df
        g = t2[
            (t2[filt[0]] != 0) | (t2[filt[1]] != 0) | (t2[filt[2]] != 0) | (t2[filt[3]] != 0) | (t2[filt[4]] != 0) | (
                        t2[filt[5]] != 0) | (t2[filt[6]] != 0) | (t2[filt[7]] != 0) | (t2[filt[8]] != 0) | (
                        t2[filt[9]] != 0) | (t2[filt[10]] != 0) | (t2[filt[11]] != 0) | (t2[filt[12]] != 0) | (
                        t2[filt[13]] != 0) | (t2[filt[14]] != 0) | (t2[filt[15]] != 0) | (t2[filt[16]] != 0) | (
                        t2[filt[17]] != 0) | (t2[filt[19]] != 0) | (t2[filt[20]] != 0) |
            (t2[filt[21]] != 0) | (t2[filt[22]] != 0) | (t2[filt[23]] != 0) | (t2[filt[24]] != 0) | (
                        t2[filt[25]] != 0) | (t2[filt[26]] != 0) | (t2[filt[27]] != 0) | (t2[filt[29]] != 0) | (
                        t2[filt[30]] != 0) | (t2[filt[28]] != 0) | (t2[filt[31]] != 0) | (t2[filt[32]] != 0) | (
                        t2[filt[33]] != 0) | (t2[filt[34]] != 0) | (t2[filt[35]] != 0) | (t2[filt[36]] != 0) | (
                        t2[filt[37]] != 0) | (t2[filt[38]] != 0) | (t2[filt[39]] != 0) |
            (t2[filt[10]] != 0) | (t2[filt[41]] != 0) | (t2[filt[42]] != 0) | (t2[filt[43]] != 0) | (
                        t2[filt[44]] != 0) | (t2[filt[45]] != 0) | (t2[filt[46]] != 0) | (t2[filt[47]] != 0) | (
                        t2[filt[48]] != 0) | (t2[filt[49]] != 0) | (t2[filt[50]] != 0) | (t2[filt[51]] != 0) | (
                        t2[filt[52]] != 0) | (t2[filt[53]] != 0) | (t2[filt[54]] != 0) | (t2[filt[55]] != 0) | (
                        t2[filt[56]] != 0) | (t2[filt[57]] != 0) | (t2[filt[58]] != 0) | (t2[filt[19]] != 0)]

        self.req = g
        return list(set(g['Населённый пункт:'].values))[1:]

    def get_result(self):
        self.req = self.req[(self.req['Населённый пункт:'] == self.city)]

        if self.interest == 'exact':
            self.req = self.req.sort_values(by='X', ascending=False)
        elif self.interest == 'humanities':
            self.req = self.req.sort_values(by='X', ascending=True)

        if self.interest == 'natural':
            self.req = self.req.sort_values(by='Y', ascending=False)
        elif self.interest == 'creative':
            self.req = self.req.sort_values(by='Y', ascending=True)

        with open('text.txt', 'r', encoding='utf-8') as file:
            file.read
            table = {}
            for line in file:
                s = line[:-1].split(', ')
                table[s[0]] = s[1]

        profession = []
        names = []
        addresses = []
        for j in range(len(self.req)):
            s2 = []
            for el in list(set(self.req.iloc[j]['specialization'].split(', '))):
                if el in table.keys():
                    s2.append(table[el])
            profession.append(s2)
            # profession.append(self.req.iloc[j]['specialization'].replace("'", '').split(', '))
            names.append([self.req.iloc[j]['Название']])
            addresses.append([self.req.iloc[j]['Регион:']])

        result = {
            'name': names,
            'city': addresses,
            'specialization': profession
        }
        return result

    def get_interest(self):
        return self.interest

    def reset_user(self):
        self.interest = None
        self.city = None
        self.df = pd.read_csv('vet-result.csv')
        self.req = None


parameters = {
    'exact': ['01', '02', '03', '05', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '20', '21', '22',
              '23', '24', '25', '26', '27', '28', '29', '56', '57', '38'],
    'natural': ['04', '05', '06', '12', '18', '19', '21', '29', '30', '31', '32', '33', '34', '35', '36', ],
    'humanities': ['37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48'],
    'creative': ['49', '50', '51', '52', '53', '54', '55']
}

# ФИзика-мат-инф\Гуманитарное Биолог-Химия\ Творческое
PROFESSIONS = {
    '01': [3, 0],
    '02': [2, 2],
    '03': [3, 1],
    '04': [0, 3],
    '05': [2, 2],
    '06': [0, 3],
    '07': [2, -1],
    '08': [2, 0],
    '09': [3, 0],
    '10': [3, 0],
    '11': [3, 1],
    '12': [3, 2],
    '13': [3, 0],
    '14': [3, 0],
    '15': [3, 1],
    '16': [3, 0],
    '17': [3, 0],
    '18': [1, 3],
    '19': [0, 3],
    '20': [2, 0.5],
    '21': [2, 2],
    '22': [1, 1],
    '23': [2, 0],
    '24': [3, 0],
    '25': [2, 0],
    '26': [2, 0],
    '27': [2, 0],
    '28': [3, 2], '29': [1, 1], '30': [0, 3], '31': [0, 3], '32': [0, 3], '33': [0, 3], '34': [0, 3], '35': [1, 3],  '36': [-1, 3],
    '37': [-2, 0],  '38': [1, 0],  '39': [-1, -1],  '40': [-3, 0],  '41': [-2, 0], '42': [-2, 0], '43': [-3, -1],  '44': [-3, 0],
    '45': [-3, 0],  '46': [-3, 0],  '47': [-3, 0],  '48': [-2, 0],  '49': [-1, -3],  '50': [-2, 0],   '51': [-2, 0],   '52': [0, -3],
    '53': [0, -3],  '54': [0, -3],   '55': [1, -1],   '56': [1, 0],   '57': [1, 0],   '58': [0, 0],   '65': [1, 0]

}