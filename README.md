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


# Part II - Bayesian Inference and Simulation
## Win Rate Distribution
We assume that each battle outcome is independent and identically distributed (I believe that this is not a valid assumption, but we will test how plausible this assumption), we also assume a uniform distribution of the win rate, and we try to infer the win rate posterior distribution under the assumption of a Bernoulli likelihood.

Prior:

$$ p(\alpha) \sim \text{Uniform}(0,1) $$

Likelihood:

$$ p(\text{win}|\alpha) \sim \text{Bernoulli}(\alpha)$$

Win rate trace plot:

![Win Rate Trace](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/trace_win.png?raw=true)

Posterior distribution of win rate:

![Win Rate Posterior](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/posterior_win_pct.png?raw=true)



## Trophy Change Distribution
How much trophies do we expect to win/lose after each battle? to answer this we model the observed trophy change (27, 29, 29, 30, .., 33) as a Catenary distribution with a Drichlet prior, for both the positive and negative change.

Prior:

$$ p_+ \sim \text{Dirichlet} ([1, \dots, 1]) $$

$$ p_- \sim \text{Dirichlet} ([1, \dots, 1]) $$


Likelihood:

$$\text{Trophy}_+ \sim \text{Categorical} (p_+) $$

$$\text{Trophy}_- \sim \text{Categorical} (p_-) $$


Trace plots for $\text{Trophy}_+$ and $\text{Trophy}_-$:

![Positive Trophy Change Trace](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/trace_tropy_pos.png?raw=true)

![Negative Trophy Change Trace](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/trace_trophy_neg.png?raw=true)

Distribution plot of positive and negative trophy change at posterior mean values:
![Trophy change Posterior](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/trophy_change_dist.png?raw=true)

For me the game was on average more rewarding than it was punishing. I was able to win more trophies than I lost, mode of positive trophy change is 30 while for negative trophy change it's 27, so despite the low win rate, the game on average is rewarding.

## How valid is the assumption that battle outcomes are independent?
I don't think each battle outcome is independent, but if we proceeded anyway to assume that, and given the data we have, is this a valid assumption?
In order to test this we define a Test statistic as the number of switches between wins and defeats.

![Tests](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/tests.png?raw=true)


## Simulate random walk battles, since season start
![Random Walk](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/random_walk.png?raw=true)


## Predict season ending trophy, based on half season battles

Linear regression model parameters trace plot:
![Linear Regression Model Trace](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/linear_regression.png?raw=true)

![HDI Plot](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/linear_regression_hdi.png?raw=true)

![Prediction vs Observed](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/linear_regression_prediction.png?raw=true)


## Testing the probability of a particular observed losing streak
![Lose Streak](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/lose_streak.png?raw=true)

![Lose Streak vs random walk](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/lose_streak_random-walk.png?raw=true)

![Lose Streak Test](https://raw.githubusercontent.com/eigenemara/cr-analysis/main/images/lose_streak_test.png?raw=true)
