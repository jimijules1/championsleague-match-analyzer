#%%
import pandas as pd
import matplotlib.pyplot as plt

#%%

# Load the data from the provided Excel file
file_path = 'data/2016_2017-champion.xlsx'
data = pd.read_excel(file_path)

#%%

# Display the first few rows of the dataframe and the column names to understand its structure
data.head(), data.columns

#%%
# Rename columns if necessary and confirm column names for goals
data.rename(columns=lambda x: x.strip(), inplace=True)  # Stripping any trailing spaces from column names

# Calculate home and away wins
# A home win is when home goals are greater than away goals, and vice versa for an away win
home_wins = data[data['homegoal'] > data['awaygoals']]['hometeam'].value_counts()
away_wins = data[data['awaygoals'] > data['homegoal']]['awayteam'].value_counts()

# Combine the data into a single DataFrame for visualization
win_counts = pd.DataFrame({'Home Wins': home_wins, 'Away Wins': away_wins}).fillna(0).astype(int)

# Preview the combined data
win_counts.head()

#%%

# Create a bar chart to display the home and away wins for each team
win_counts.plot(kind='bar', figsize=(14, 7), color=['skyblue', 'lightgreen'])
plt.title('Number of Home and Away Wins by Team')
plt.xlabel('Team')
plt.ylabel('Number of Wins')
plt.legend(['Home Wins', 'Away Wins'])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the plot
plt.show()

#%%