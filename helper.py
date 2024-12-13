import re
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]

    # Total words
    words = []
    for message in df['message']:
        words.extend(message.split())  # Split into words and extend the list

    # Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Fetch number of links shared (URLs)
    links = []
    for message in df['message']:  # Correct column name here to 'message'
        # Extract URLs from the message
        links.extend(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    # Get the top 5 most active users
    x = df['user'].value_counts().head()

    # Calculate percentage of messages per user and round the values
    df_percentage = (df['user'].value_counts() / df.shape[0] * 100).round(2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}
    )

    return x, df_percentage

def most_common_words(selected_user, df):
    try:
        with open('hinglish1.txt', 'r') as f:
            stop_words = f.read().splitlines()  # Read and split lines
    except FileNotFoundError:
        print("Error: 'hinglish1.txt' not found. Please ensure the file exists.")
        return None

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>/n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_counts = Counter(emojis)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Convert the 'date' column to datetime (if not already)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Group by year, month, and month number, then count messages
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a time column combining month and year
    timeline['time'] = timeline['month'].astype(str) + '-' + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):
     if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

     daily_timeline = df.groupby('only_date').count()['message'].reset_index()
     return daily_timeline

def week_activity_map(selected_user, df):
     if selected_user != 'Overall':
         df = df[df['user'] == selected_user]
     return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
     if selected_user != 'Overall':
         df = df[df['user'] == selected_user]
     return df['month'].value_counts()

def activity_heatmap(selected_user, df):
     if selected_user != 'Overall':
         df = df[df['user'] == selected_user]
     user_heatmap = df.pivot_table(index='day_name',  values='message', aggfunc='count').fillna(0)
     return user_heatmap
