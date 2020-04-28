from collections import OrderedDict
from collections import Counter
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as mfm
import matplotlib.ticker as ticker
from scipy.stats import pearsonr


mpl.rcParams['axes.spines.left'] = True
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.bottom'] = True
mpl.rcParams['axes.linewidth'] = 2

font_path = "‪C:\\Users\\BB\\Desktop\\HINDI.ttf"
font_path = font_path.lstrip('\u202a')
prop = mfm.FontProperties(fname=font_path)

# Font for the graph title.
cs_font = {'fontname': 'monospace'}

curse_words = []
count = 0
count_time = []
count_time_ = []
count_dict = OrderedDict()
kaaleen = []
# IMDb Ratings
ratings = [8.7, 8.4, 7.9, 8.3, 8.4, 8.3, 8.8, 8.7, 9.0]
# Subtitle Files
files = ["E1S1.srt", "E2S1.srt", "E3S1.srt", "E4S1.srt", "E5S1.srt", "E6S1.srt", "E7S1.srt", "E8S1.srt", "E9S1.srt"]

with open("curse.txt") as curse:
    for line in curse:
        line = line.replace('\n', '')
        curse_words.append(line)

for i in range(0, len(files)):
    with open(files[i]) as subtitle:
        lines = []
        for line in subtitle:
            for word in line.split():
                # Removing punctuation and converting to lowercase for better use.
                word = word.lower()
                word = re.sub(r'[^\w\s]', '', word)
                if word == 'kaaleen':
                    kaaleen.append(i)
                if word in curse_words:
                    count += 1
                    if word not in count_dict:
                        count_dict[word] = 1
                    else:
                        count_dict[word] += 1

    count_time.append(count)

# Finds curse count per episode, earlier it appended the total sum count.
for i in range(0,len(count_time)):
    if i > 0:
        count_time_.append(count_time[i] - count_time[i-1])
    if i == 0:
        count_time_.append(count_time[0])

# print(len(kaaleen))
ls = list(zip(Counter(kaaleen).keys(), Counter(kaaleen).values()))
# print(ls)
# print(count)
# 268 curse words total.
# Kaaleen word used most times in 2nd episode while the total being 52 times throughout the season.
c = Counter(count_dict)
print(c.most_common(10))
corr, _ = pearsonr(count_time_, ratings)
print('Pearsons correlation: %.3f' % corr)
# Pearsons Correlation 0.309 between curse count and IMDb Rating.


def graph():

    tick_spacing = 0.2
    x = len(count_time_)
    x = np.linspace(1, x, x)
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(x, count_time_, label='Curse Words count')
    ax1.set_ylabel('Number of Curse Words')
    ax1.legend(loc='best',frameon=False,shadow=True)
    ax3 = ax1.twinx()
    plt.title('Mirzapur', **cs_font, fontweight='bold')
    ax2 = fig.add_subplot(212)
    ax2.set_xlabel('Episodes')
    ax2.plot(x, ratings, '--', color='red', alpha=0.8, label='IMDb Rating')
    ax2.legend(loc='best',frameon=False)
    ax2.set_ylabel('IMDb Rating')
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # To plot the bar chart. Tells how relative the most cursed word is used compared with other words.
    x_values = [3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5]
    y_values = [13, 14, 21, 54, 24, 33, 14, 17]
    ax3.bar(x_values, y_values, alpha=0.2)
    ax3.set_yticks([])
    # Most used word was Motherfucker.
    ax1.text(3.8, 40, 'मादरचोद', fontproperties=prop,fontsize=9)
    # Change limits of bar chart to make it fit better.
    ax3.set_ylim(0, 80)
    plt.savefig('Mirzapur.png',dpi=300,bb0x_inches='tight')
    plt.show()


graph()


