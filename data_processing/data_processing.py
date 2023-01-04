import pandas as pd
from user import PROFESSIONS
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


#save file with codes of specializations
def work_with_file():
    df = pd.read_csv('result.csv')
    res = set()
    for j in range(2447):
        for el in df.iloc[j].specialization.split(', '):
            res.add(el[:-2])
    res = sorted(list(res))
    print(res)

    with open('data_processing/data/specializations2.csv', 'w') as file:
        file.write('\n')
        for el in res:
            file.write(el + '\n')


# make weights of professions by code of specialization
# ФИзика-мат-инф\Гуманитарное\ Биолог-Химия\ Творческое
def profession(df):
    x_ax = [0] * 2447
    y_ax = [0] * 2447
    for j in range(2447):
        for el in df.iloc[j].specialization.split(', '):
            l = len(df.iloc[j].specialization.split(', '))
            if len(el) == 5:
                el = '0' + el
            x_ax[j] += PROFESSIONS[el[:2]][0] / l
            y_ax[j] += PROFESSIONS[el[:2]][1] / l

    df['X'] = x_ax
    df['Y'] = y_ax
    return df


if __name__ == '__main__':
    # make column with code of professions 
    df = pd.read_csv('result.csv')
    new_colum = [''] * 2293
    for j in range(2293):
        for el in df.iloc[j].specialization.split(', '):
            l = len(df.iloc[j].specialization.split(', '))
            if len(el) == 5:
                el = '0' + el
            new_colum[j] += el[:2] + ' '
    df['Prf'] = new_colum

    all_texts = df.Prf.values.tolist()
    count_vect = CountVectorizer()
    matrix_count = count_vect.fit_transform(all_texts).toarray()

    print(matrix_count)
    print(len(df.specialization.values))

    words = [x[0] for x in sorted(count_vect.vocabulary_.items(), key=lambda x: x[1])]
    t = pd.DataFrame(matrix_count, columns=words)
    t2 = pd.concat([df, t], axis=1)
    t2.to_csv('vet-result.csv')

    df2 = profession(df)
    df2.to_csv('data_processing/data/result.csv')

    #plot MIPT universiti on the graph
    plt.scatter(df[df['id'] == 3302].X, df[df['id']== 3302].Y, s=10)
    plt.grid()
    plt.xlim([-3, 3])
    plt.ylim([-3, 3])
    plt.show()
    plt.savefig('data_processing/data/professions.png')


