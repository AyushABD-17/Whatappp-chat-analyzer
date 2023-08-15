import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title('welcome whatsapp message analayzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    select_user=st.sidebar.selectbox('Show analysis wrt',user_list)

    if st.sidebar.button("Analysis"):

        num_messages,words,num_media_message,links=helper.fetch_data(select_user,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        
        with col2:
            st.header("Total words")
            st.title(words)
        
        with col3:
            st.header("Media Message")
            st.title(num_media_message)

        with col4:
            st.header("Links Shared")
            st.title(len(links))
        
    if select_user == 'Overall':
        st.title('Most Busy user')
        x,new_df = helper.most_busy_user(df)
        fig , ax = plt.subplots()
        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    #  word cloud
    st.title('Word Cloud')
    df_wc = helper.create_wordcloud(select_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most common wordshelp used :-
    st.title("Most common words used")
    most_commonwords_df = helper.most_commonwords(select_user,df)

    

    fig,ax = plt.subplots()

    ax.barh(most_commonwords_df[0],most_commonwords_df[1])
    plt.xticks(rotation='vertical')

    st.title('Most commmon words')
    st.pyplot(fig)


    #  emoji analysis:
    emoji_df = helper.emoji_helper(select_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1],labels=emoji_df[0])
        st.pyplot(fig)
    
    # timeline:

    timeline = helper.monthly_timeline(select_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    