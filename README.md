# Data Analysis of Oscars Nomination and Awards

The Oscars, officially known as the Academy Awards, are one of the most prestigious and highly anticipated events in the world of entertainment. Established by the Academy of Motion Picture Arts and Sciences (AMPAS) in 1929, the Oscars recognize excellence in various categories, including Best Picture, Best Director, Best Actor, Best Actress, and many more. Around 5000 films and 7000 people have been nominated for different categories during its 95-year history. By analyzing the dataset of all the past nominees and awardees of the Academy Awards in conjunction with the popular online media database IMDb, I aim to answer the following questions:

*   Which director/actor/actress has received the most number of nominees?
*   What genre is most popular in each of the "Big Five" category?
*   Is there a correlation between IMDb score/gross revenue and likelihood of winning?

## Code and Resources Used
**Python Version:** 3.9

**Packages:** pandas, matplotlib, scipy, cpi, seaborn

The datasets used in this project were downloaded from Kaggle:
*   The Oscar Award, 1927 - 2023 https://www.kaggle.com/datasets/unanimad/the-oscar-award
*   Movie Industry https://www.kaggle.com/datasets/danielgrijalvas/movies


## Results

### Which director/actor/actress has received the most number of nominees?

The table below shows the top three directors with the most nominations since 1929.

| Directors        | Nominations |
|------------------|-------------|
| William Wyler    | 12          |
| Martin Scoresese | 9           |
| Steven Spielberg | 9           |
| Billy Wilder     | 8           |

The two table below shows the top three actors and actresses with the most nominations since 1929. The award category considers both "Best Actor/Actress" (used from 1929-1976) and "Best Actor/Actress in a Leading Role" (used since 1977).

| Actors            | Nominations |
|-------------------|-------------|
| Spencer Tracy     | 9           |
| Laurence Olivier  | 7           |
| Marlon Brando     | 7           |
| Denzel Washington | 8           |
| Paul Muni         | 6           |

| Actress           | Nominations |
|-------------------|-------------|
| Meryl Streep      | 17          |
| Katharine Hepburn | 11          |
| Bette Davis       | 11          |
| Greer Garson      | 7           |

A modified Gantt chart shows the time period in which these nominations occured. Most of the top nominees were active before 1980s, but there are few that have received their nominations after 1980. Most notably, Greer Garson has received seven nominations in the span of 22 years, which calculates to roughly one nomination every three years!

![alt text](https://github.com/misaki-inoue/oscars/blob/main/timeline.png "Gantt chart of the time between first and last Oscar nomination of the top three directors/actors/actresses")

###  What genre is most popular in each of the "Big Five" category?

The Oscars and IMDb dataset were merged to explore the genre of Oscar nominated films. Although the IMDb dataset only contains films from 1980-2020, the merged dataset contained more than 1000 entries after filtering for the "Big Five" category (Best Actor in a Leading Role, Best Actress in a Leading Role, Best Director, Best Writing, Best Picture).

In all categories, drama was the most popular followed by biography or comedy.

![alt text](https://github.com/misaki-inoue/oscars/blob/main/genre.png "Stacked bar plot of different film genres nominated for the Big Five categories")

###  Is there a correlation between IMDb score/gross revenue and likelihood of winning?

The IMDb dataset contains IMDb score out of 10 and the gross revenue for each film. Therefore, a statistical analysis called Mann-Whitney U test was performed to compare the median IMDb score or gross revenue between nominees and winners. This non-parametric test was chosen to compare two samples of different sizes (2729 nominees vs. 784 winners). The gross revenues in US Dollars were adjusted for inflation using a Python library called `cpi`.

The boxplot below shows that median IMDb score is higher for winners by 0.3 points (_U_ = 1330259.5, _p_ =  1.95<sup>-25</sup>). It also shows that median adjusted gross revenue of winners is $132,857,028 more than the nominees. In conclusion, there is a correlation between higher IMDb score and higher gross revenue of a film with the likelihood of winning a Oscars category.

![alt text](https://github.com/misaki-inoue/oscars/blob/main/score_revenue.png "Box plot on right shows IMDb score nominees and winners. Box plot on left shows adjusted gross revenue of nominees and winners.")
