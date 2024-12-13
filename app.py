
import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# Sidebar Title
st.sidebar.title("🌟 WhatsApp Chat Analyzer 📊")
st.write("Analyze your WhatsApp chats easily and gain insights into your conversations.")


# File Upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Decode uploaded file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the data
    df = preprocessor.preprocess(data)
    # st.dataframe(df)  # Display DataFrame for debugging purposes

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove('group notification')  # Remove system messages
    user_list.sort()
    user_list.insert(0, "Overall")  # Add "Overall" option for stats

    # Sidebar user selection
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetch stats
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top statistic")
        # Display stats in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Display WordCloud
        st.title("Word Cloud")
        if selected_user == 'Overall':  # WordCloud for all users
            text = ' '.join(df['message'])  # Combine all messages into a single string
        else:  # WordCloud for the selected user
            user_df = df[df['user'] == selected_user]
            text = ' '.join(user_df['message'])  # Combine messages of the selected user

        # Generate the WordCloud
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate(text)

        # Plot the WordCloud
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')  # Turn off axis for a cleaner view
        st.pyplot(fig)

     #monthly time line
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

      # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        st.pyplot(fig)
    with col2:
        st.header("Most busy Month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color ='yellow')
        st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



     #Finding the busiest user in the group
    if selected_user == 'Overall':  # Correct case for 'Overall'
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)

            # Plotting the busiest users
            fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size for better readability
            ax.bar(x.index, x.values, color='red')

            # Adding labels and title to the graph
            ax.set_xlabel('Users')
            ax.set_ylabel('Number of Messages')
            ax.set_title('Most Active Users')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=90)

            # Displaying the graph
            st.pyplot(fig)

            # Display the DataFrame for the busiest users
            st.dataframe(new_df)
            most_common_df = helper.most_common_words(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(most_common_df[0],most_common_df[1])
            plt.xticks(rotation=90)
            st.title('Most common words')
            st.pyplot(fig)
            st.dataframe(most_common_df)

            #emoji analysis
            emoji_df = helper.emoji_helper(selected_user,df)
            st.title("Emoji Analysis")
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie( emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)


