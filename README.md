# Clash Royale Season 35 Analysis

This is a data analysis for my Clash Royale Season 35 battles, as a log bait player (except for one X-Bow battle by mistake). The goals of the current analysis are:

**Part I: Exploratory Data Analysis**:
- Explore patterns of win/defeat and investigate my own win rate of the current season.
- Investigate the trophy change distribution (+ve/-ve) after each battle.
- Explore patterns of win/defeat streaks.
- Finding out the most common cards in my opponents decks.

**Part II: Inference**:
- Build a Bayesian model to infer distributions for: win rate, positive trophy change and negative trophy change.
- Simulate random walk battles to compare actual progression vs. the simulated battles.
- Test a particular observed lose streak and calculate the probability of its occurence by simulating a random battle walks.
- Build a simple Bayesian linear regression model to predice the season ending trophies.

# Part I: Exploratory Data Analysis
In `data.csv` we have 474 battles, with the following summary statistics:
```
Season Starting Trophies = 5609 trophies
Season Ending Trophies = 6168 trophies
Overall Observed Win rate = 51.27%
Total Trophy Change since season start = 650 trophies
Total number of battles = 474 battles
Active playing days = 32 days
Avg. rate of trophy increase = 20.31 trophies/day
``` 

![Battle Results Bar Chart](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/battle_results_bar.png?raw=true)

![Battle Results Time Series](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/battle_results_time_series.png?raw=true)

![Streak Length Bar Chart](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/streak_length_bar.png?raw=true)

![Opponents Common Cards](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/most_common_cards.png?raw=true)

