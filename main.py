#%% load libraries
import pandas as pd
import matplotlib.pyplot as plt


#%% load data
# Load the matches sheet file to see the sheet names and preview the data
file_path = 'data/UEFA Champions League 2016-2022 Data.xlsx'
excel_data = pd.ExcelFile(file_path)

matches_data = pd.read_excel(excel_data, sheet_name='matches')
matches_data.head()


#%%

#  function to calculate the win for home and away teams
def match_outcome(row):
    if row['HOME_TEAM_SCORE'] > row['AWAY_TEAM_SCORE']:
        return row['HOME_TEAM'], 'home_win'
    elif row['AWAY_TEAM_SCORE'] > row['HOME_TEAM_SCORE']:
        return row['AWAY_TEAM'], 'away_win'
    else:
        return None, None  # For draws or ties


# Apply the function to each match
matches_data['WINNER'], matches_data['WIN_TYPE'] = zip(*matches_data.apply(match_outcome, axis=1))

# Count wins for each team as home and away
home_wins = matches_data[matches_data['WIN_TYPE'] == 'home_win']['HOME_TEAM'].value_counts()
away_wins = matches_data[matches_data['WIN_TYPE'] == 'away_win']['AWAY_TEAM'].value_counts()

# Combine the counts to get total wins for each team
total_wins = home_wins.add(away_wins, fill_value=0).astype(int)

# Calculate total matches played by each team at home and away
total_home_matches = matches_data['HOME_TEAM'].value_counts()
total_away_matches = matches_data['AWAY_TEAM'].value_counts()

# Calculate winning chances (total wins divided by total matches)
winning_chance_home = (home_wins / total_home_matches * 100).round(2)
winning_chance_away = (away_wins / total_away_matches * 100).round(2)

#%%

# Display sorted top teams by winning chance at home (only where data is available)
sorted_winning_chance_home = winning_chance_home.dropna().sort_values(ascending=False)
sorted_winning_chance_away = winning_chance_away.dropna().sort_values(ascending=False)


# Select the top 10 teams for home and away winning chance
top_10_home = sorted_winning_chance_home.head(10)
top_10_away = sorted_winning_chance_away.loc[top_10_home.index].fillna(0)  # Match the same teams for away, fill missing with 0


# Create a combined bar plot for home and away performances of the top 10 teams

fig, ax = plt.subplots(figsize=(10, 6))

# Calculate positions for the groups
indices = range(len(top_10_home))
bar_width = 0.35

# Home performance bars
home_bars = ax.bar(indices, top_10_home, bar_width, label='Home Win %', color='blue')

# Away performance bars
away_bars = ax.bar([i + bar_width for i in indices], top_10_away, bar_width, label='Away Win %', color='green')

# Labeling and aesthetics
ax.set_xlabel('Teams')
ax.set_ylabel('Winning Chance (%)')
ax.set_title('Top 10 Teams by Home and Away Winning Chances')
ax.set_xticks([i + bar_width / 2 for i in indices])
ax.set_xticklabels(top_10_home.index, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()


#%%

# Select the top 10 teams for away and then match the same teams for home winning chance
top_10_away_only = sorted_winning_chance_away.head(10)
top_10_home_for_top_away = sorted_winning_chance_home.loc[top_10_away_only.index].fillna(0)  # Match the same teams for home, fill missing with 0

# Create a combined bar plot for home and away performances for the top performing away teams
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate positions for the groups
indices_away = range(len(top_10_away_only))
bar_width_away = 0.35

# Home performance bars
home_bars_away = ax.bar(indices_away, top_10_home_for_top_away, bar_width_away, label='Home Win %', color='blue')

# Away performance bars
away_bars_away = ax.bar([i + bar_width_away for i in indices_away], top_10_away_only, bar_width_away, label='Away Win %', color='green')

# Labeling and aesthetics
ax.set_xlabel('Teams')
ax.set_ylabel('Winning Chance (%)')
ax.set_title('Top 10 Teams by Away Winning Chances and Their Home Performance')
ax.set_xticks([i + bar_width_away / 2 for i in indices_away])
ax.set_xticklabels(top_10_away_only.index, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()

#%% Show total wins
# Calculate total wins by combining home and away wins
total_combined_wins = home_wins.add(away_wins, fill_value=0).sort_values(ascending=False).head(10)

# Create a plot for total combined wins
fig, ax = plt.subplots(figsize=(10, 6))

# Bar plot for total combined wins
ax.bar(total_combined_wins.index, total_combined_wins, color='purple', label='Total Wins (Home + Away)')

# Labeling and aesthetics
ax.set_xlabel('Teams')
ax.set_ylabel('Total Wins')
ax.set_title('Top 10 Teams by Total Wins (Home and Away Combined)')
ax.set_xticklabels(total_combined_wins.index, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()

#%%

# Load the "goals" sheet to analyze its content and structure
goals_data = pd.read_excel(excel_data, sheet_name='goals')
goals_data.head()

# Merge the goals data with matches data to get home and away team info
goal_details = goals_data.merge(matches_data[['MATCH_ID', 'HOME_TEAM', 'AWAY_TEAM']], on='MATCH_ID', how='left')

# Calculate goals scored by home and away teams
home_goals = goal_details.groupby('HOME_TEAM')['GOAL_ID'].count()
away_goals = goal_details.groupby('AWAY_TEAM')['GOAL_ID'].count()

# Combine the counts to get total goals for each team
total_goals = home_goals.add(away_goals, fill_value=0).astype(int).sort_values(ascending=False)

# Display the total, home, and away goals for each team
total_goals, home_goals.sort_values(ascending=False), away_goals.sort_values(ascending=False)


#%%

# Select the top 10 teams for home and away goals
top_10_home_goals = home_goals.sort_values(ascending=False).head(10)
top_10_away_goals_for_top_home = away_goals.loc[top_10_home_goals.index].fillna(0)  # Match the same teams for away goals

# Select the top 10 teams for away goals
top_10_away_goals = away_goals.sort_values(ascending=False).head(10)
top_10_home_goals_for_top_away = home_goals.loc[top_10_away_goals.index].fillna(0)  # Match the same teams for home goals

# Create two subplots for home and away goals comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Plot for home goals with corresponding away goals
indices_home = range(len(top_10_home_goals))
bar_width = 0.35
home_goals_bars = ax1.bar(indices_home, top_10_home_goals, bar_width, label='Home Goals', color='blue')
away_goals_bars_home = ax1.bar([i + bar_width for i in indices_home], top_10_away_goals_for_top_home, bar_width, label='Away Goals', color='green')
ax1.set_title('Top 10 Teams by Home Goals and Corresponding Away Goals')
ax1.set_xticks([i + bar_width / 2 for i in indices_home])
ax1.set_xticklabels(top_10_home_goals.index, rotation=45, ha="right")
ax1.set_ylabel('Number of Goals')
ax1.legend()

# Plot for away goals with corresponding home goals
indices_away = range(len(top_10_away_goals))
away_goals_bars = ax2.bar(indices_away, top_10_away_goals, bar_width, label='Away Goals', color='green')
home_goals_bars_away = ax2.bar([i + bar_width for i in indices_away], top_10_home_goals_for_top_away, bar_width, label='Home Goals', color='blue')
ax2.set_title('Top 10 Teams by Away Goals and Corresponding Home Goals')
ax2.set_xticks([i + bar_width / 2 for i in indices_away])
ax2.set_xticklabels(top_10_away_goals.index, rotation=45, ha="right")
ax2.set_ylabel('Number of Goals')
ax2.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()


#%%

# Add win flags for home and away wins
matches_data['HOME_WIN'] = matches_data['HOME_TEAM_SCORE'] > matches_data['AWAY_TEAM_SCORE']
matches_data['AWAY_WIN'] = matches_data['AWAY_TEAM_SCORE'] > matches_data['HOME_TEAM_SCORE']

# Separate matches into those with and without attendance
matches_with_attendance = matches_data[matches_data['ATTENDANCE'] > 0]
matches_without_attendance = matches_data[matches_data['ATTENDANCE'] == 0]

# Calculate win rates for matches with attendance
home_wins_with = matches_with_attendance.groupby('HOME_TEAM')['HOME_WIN'].mean()
away_wins_with = matches_with_attendance.groupby('AWAY_TEAM')['AWAY_WIN'].mean()
total_wins_with = home_wins_with.add(away_wins_with, fill_value=0) / 2

# Calculate win rates for matches without attendance
home_wins_without = matches_without_attendance.groupby('HOME_TEAM')['HOME_WIN'].mean()
away_wins_without = matches_without_attendance.groupby('AWAY_TEAM')['AWAY_WIN'].mean()
total_wins_without = home_wins_without.add(away_wins_without, fill_value=0) / 2

# Calculate differences in win rates (with attendance - without attendance)
win_rate_difference = total_wins_with.subtract(total_wins_without, fill_value=0).sort_values(ascending=False)

win_rate_difference.head(10)


#%%

# 1. Analyzing home Performance of teams in 2020-2021 where this team had more than 1 match with 0 spectators.
# 2. Analyzing the home performance of these teams in other years where these teams had spectators.
# 3. Comparing the performance. Sorting according to biggest differences in terms where teams with spectators played significantly better. Show in a bar chart their winning percentage without spectators and with spectators (sorted accordingf to biggest difference). include only teams which also have appearances in both 2020-2021 and other years.

matches_data['HOME_WIN'] = matches_data['HOME_TEAM_SCORE'] > matches_data['AWAY_TEAM_SCORE']
matches_data['AWAY_WIN'] = matches_data['AWAY_TEAM_SCORE'] > matches_data['HOME_TEAM_SCORE']

# Filter matches for the 2020-2021 season with zero spectators
matches_2020_2021_no_spectators = matches_data[(matches_data['SEASON'] == '2020-2021') & (matches_data['ATTENDANCE'] == 0)]

# Count the number of home matches played by each team in 2020-2021 with no spectators
home_matches_no_spectators_count = matches_2020_2021_no_spectators['HOME_TEAM'].value_counts()

# Filter teams that played more than one home match without spectators in 2020-2021
teams_more_than_one_no_spectators = home_matches_no_spectators_count[home_matches_no_spectators_count > 1].index

# Filter these specific matches
matches_2020_2021_no_spectators_filtered = matches_2020_2021_no_spectators[matches_2020_2021_no_spectators['HOME_TEAM'].isin(teams_more_than_one_no_spectators)]

# Calculate win rates for these teams in 2020-2021 with no spectators
win_rates_2020_2021_no_spectators = matches_2020_2021_no_spectators_filtered.groupby('HOME_TEAM')['HOME_WIN'].mean()

# Filter matches for other years where teams had spectators
matches_other_years_with_spectators = matches_data[(matches_data['SEASON'] != '2020-2021') & (matches_data['ATTENDANCE'] > 0) & (matches_data['HOME_TEAM'].isin(teams_more_than_one_no_spectators))]

# Calculate win rates for these teams in other years with spectators
win_rates_other_years_with_spectators = matches_other_years_with_spectators.groupby('HOME_TEAM')['HOME_WIN'].mean()

# Combine the two series into a dataframe
win_rate_comparison = pd.DataFrame({
    'Without Spectators (2020-2021)': win_rates_2020_2021_no_spectators,
    'With Spectators (Other Years)': win_rates_other_years_with_spectators
}).dropna()  # Drop any team not appearing in both scenarios

# Calculate the difference in win rates (spectators - no spectators)
win_rate_comparison['Difference'] = win_rate_comparison['With Spectators (Other Years)'] - win_rate_comparison['Without Spectators (2020-2021)']
win_rate_comparison_sorted = win_rate_comparison.sort_values('Difference', ascending=False)

win_rate_comparison_sorted.head(10)

# Create a bar chart to visualize the win rate comparison
fig, ax = plt.subplots(figsize=(12, 8))

# Define indices for bar positions
indices = range(len(win_rate_comparison_sorted))

# Plot bars for win rates without and with spectators
ax.bar(indices, win_rate_comparison_sorted['Without Spectators (2020-2021)'], width=0.4, label='Without Spectators (2020-2021)', color='red', align='center')
ax.bar([i + 0.4 for i in indices], win_rate_comparison_sorted['With Spectators (Other Years)'], width=0.4, label='With Spectators (Other Years)', color='green', align='center')

# Labeling and aesthetics
ax.set_xlabel('Teams')
ax.set_ylabel('Winning Percentage')
ax.set_title('Home Performance Comparison: With vs. Without Spectators')
ax.set_xticks([i + 0.2 for i in indices])
ax.set_xticklabels(win_rate_comparison_sorted.index, rotation=45, ha="right")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()

#%%