import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import packetcounter
import statistics
from scipy.stats import norm
from scipy.optimize import curve_fit
from numpy import exp, loadtxt, pi, sqrt

# Nazwy plików
file_names = ['hamming_7_4_score.csv', 'crc_score.csv', 'hamming_15_11_score.csv', 'triple_bits_score.csv']

# Nazwy kolumn
column_names = packetcounter.PacketCounter.get_column_name()


# Funkcja tworząca histogramy
def d_histogram():
    hist_names = ['hist_well_sent.png', 'hist_repaired.png', 'hist_unrepaired.png', 'hist_undetected.png']
    for column, hist, i in zip(column_names, hist_names, range(len(column_names))):
        pd.DataFrame({'crc': pd.read_csv(file_names[0])[column], '7_4': pd.read_csv(file_names[1])[column],
                      '15_11': pd.read_csv(file_names[2])[column], 'triple': pd.read_csv(file_names[3])[column]})\
          .hist(grid=False, alpha=0.5)
        plt.suptitle(column)
        plt.savefig(hist)
        plt.clf()


def gaussian(x, a, x0 ,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


def fitfit():
    data = pd.read_csv('hamming_7_4_score.csv')['Well sent']
    counts = data.value_counts()
    indexes = counts.index
    indexes_array = indexes.to_numpy()
    x = indexes_array
    counts_array = counts.to_numpy()
    y = counts_array
    mean = sum(x*y)/sum(y)
    sigma = np.sqrt(sum(y*(x - mean)**2)/sum(y))

    popt, pcov = curve_fit(gaussian, x, y, p0=[max(y), mean, sigma])

    plt.plot(x, y, 'o', label='data')
    x = np.sort(x)
    plt.plot(x, gaussian(x, *popt), 'r', label='fit')
    plt.legend()
    plt.show()


# Funkcja dopasowania
def fit_function():
    hist_names = ['hist_well_sent.png', 'hist_repaired.png', 'hist_unrepaired.png', 'hist_undetected.png']
    for column, hist in zip(column_names, hist_names):
        for file in file_names:
            # Generate some data for this demonstration.
            data = pd.read_csv(file)[column]

            # Fit a normal distribution to the data:
            mu, std = norm.fit(data)

            # Plot the histogram.
            plt.hist(data, bins=25, density=True, alpha=0.6, color='g')

            # Plot the PDF.
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mu, std)
            plt.plot(x, p, 'k', linewidth=2)
            title = "%s: %s\nFit results: mu = %.2f,  std = %.2f" % (file, column, mu, std)
            plt.title(title)
            plt.savefig(file + hist)
            plt.clf()


# Funkcja wyznaczająca średnią z każdej cechy każdego kodu
def avg_all():
    filestab = []
    for file in file_names:
        data = pd.read_csv(file)
        avg = []
        for column in column_names:
            avg.append(data[column].mean())
        filestab.append(avg)
    return filestab


# Funkcja wyznaczająca odchylenie standardowe z każdej cechy każdego kodu
def sddev_all():
    filestab = []
    for file in file_names:
        data = pd.read_csv(file)
        sddev = []
        for column in column_names:
            sddev.append(statistics.pstdev(data[column]))
        filestab.append(sddev)
    return filestab


#  Statystyka pięcopunktowa
#  Five-number summary
def fivenum_all():
    for file in file_names:
        data = pd.read_csv(file)
        print(file)
        for column in column_names:
            print(column, ": ", np.percentile(data[column], [0, 25, 50, 75, 100], interpolation='midpoint'))
        print()


#Funkcja tworząca wykresy pudełkowe
def d_boxplot():
    box_names = ['box_well_sent.png', 'box_repaired.png', 'box_unrepaired.png', 'box_undetected.png']
    for column, box in zip(column_names, box_names):
        box_plot = pd.DataFrame({'7_4': pd.read_csv(file_names[0])[column], 'crc': pd.read_csv(file_names[1])[column],
                      '15_11': pd.read_csv(file_names[2])[column], 'triple': pd.read_csv(file_names[3])[column]})
        box_plot.boxplot()
        plt.suptitle(column)
        plt.savefig(box)
        plt.clf()



#Funkcja tworząca wykresy pudełkowe
def d_boxplot4():
    data = []
    for file in file_names:
        data.append([sum(elts) for elts in zip(pd.read_csv(file)[column_names[0]], pd.read_csv(file)[column_names[1]])])

    box_plot = pd.DataFrame({'7_4': data[0], 'crc': data[1], 'triple': data[3]})
    box_plot.boxplot()
    plt.suptitle('Good packets')
    plt.savefig('box_well_sent.png')
    plt.clf()

    data.clear()
    for file in file_names:
        data.append([sum(elts) for elts in zip(pd.read_csv(file)[column_names[2]], pd.read_csv(file)[column_names[3]])])

    box_plot = pd.DataFrame({'7_4': data[0], 'crc': data[1], 'triple': data[3]})
    box_plot.boxplot()
    plt.suptitle('Bad packets')
    plt.savefig('box_bad_sent.png')
    plt.clf()


#Funkcja tworząca wykresy pudełkowe
def d_boxplot11():
    data = []
    for file in file_names:
        data.append([sum(elts) for elts in zip(pd.read_csv(file)[column_names[0]], pd.read_csv(file)[column_names[1]])])

    box_plot = pd.DataFrame({'crc': data[1], '15_11': data[2], 'triple': data[3]})
    box_plot.boxplot()
    plt.suptitle('Good packets')
    plt.savefig('box_well_sent.png')
    plt.clf()

    data.clear()
    for file in file_names:
        data.append([sum(elts) for elts in zip(pd.read_csv(file)[column_names[2]], pd.read_csv(file)[column_names[3]])])

    box_plot = pd.DataFrame({'7_4': data[0], 'crc': data[1], 'triple': data[3]})
    box_plot.boxplot()
    plt.suptitle('Bad packets')
    plt.savefig('box_bad_sent.png')
    plt.clf()
