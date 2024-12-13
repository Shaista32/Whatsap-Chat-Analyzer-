import re
import pandas as pd


def preprocess(data):
    pattern = r"(\d{2}/\d{2}/\d{4}),\s(\d{1,2}:\d{2}\s[apAP][mM])\s-\s"

    # Split data into messages
    messages = re.split(pattern, data)[1:]

    # Extract date-time and messages
    try:
        dates = [f"{messages[i]} {messages[i + 1]}" for i in range(0, len(messages), 3)]
        user_messages = [messages[i + 2] for i in range(0, len(messages), 3)]
    except IndexError:
        return pd.DataFrame()  # Return empty DataFrame if error occurs

    # Create DataFrame
    df = pd.DataFrame({'date': dates, 'user_message': user_messages})

    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %I:%M %p', errors='coerce')

    # Split user and message
    users, messages = [], []
    for message in df['user_message']:
        entry = re.split(r'([\w\s\+\-\(\)]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:
            users.append('group notification')
            messages.append(message.strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional columns
    df['only_date']= df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    #Generate time periods+_
    #period = []
    #for hour in df['hour']:
      #  if hour == 23:
          #  period.append(f"{hour}-00")
        #elif hour == 0:
          #  period.append("00-1")
        #else:
         #   period.append(f"{hour}-{hour + 1}")


    #df['period'] = period


    return df