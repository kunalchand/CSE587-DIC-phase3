import streamlit as st
import os
import pickle
import sqlite3
import pandas as pd

# Intallation Guide
# First install Python in the system
# Put files in a project folder
# Go inside project folder
# pip install streamlit
# pip install scikit-learn
# pip install pysqlite3
# git bash or open cmd in the same directory
# streamlit run app.py

def warning():
    st.warning("Game already exists!")
    st.session_state.flag = 'none'

def success():
    st.success("Game added successfully!")
    st.session_state.flag = 'none'

def warning_game_deletion():
    st.warning("Please select some games to delete!")
    st.session_state.flag = 'none'

def success_game_deletion():
    st.success("Game and its reviews successfully deleted!")
    st.session_state.flag = 'none'

def warning_review_deletion():
    st.warning("Please select some reviews to delete!")
    st.session_state.flag = 'none'

def success_review_deletion():
    st.success("Reviews successfully deleted!")
    st.session_state.flag = 'none'

def table_setup():
    if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='games'").fetchone():
        c.execute("CREATE TABLE games (id INTEGER PRIMARY KEY, game_name TEXT, game_rank REAL)")
        c.execute("INSERT INTO games (game_name, game_rank) VALUES (?, ?)", ('Game A', 0.5))
        c.execute("INSERT INTO games (game_name, game_rank) VALUES (?, ?)", ('Game B', 1))
        c.execute("INSERT INTO games (game_name, game_rank) VALUES (?, ?)", ('Game C', 0))
        conn.commit()

    if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'").fetchone():
        c.execute("CREATE TABLE reviews (id INTEGER PRIMARY KEY, game_name TEXT, game_review TEXT, game_review_prediction TEXT)")
        c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", ('Game A', 'This game is amazing!', 'Positive'))
        c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", ('Game A', 'Bad Game', 'Negative'))
        c.execute("INSERT INTO reviews (game_name, game_review, game_review_prediction) VALUES (?, ?, ?)", ('Game B', 'Insane Game', 'Positive'))
        conn.commit()

def display_games():
    c.execute("SELECT * FROM games")
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Rank'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Games")
    
    # Display Table
    table_html = df.to_html(escape=False, index=False)
    table_html = table_html.replace('<table', '<table style="width:100%;"')
    st.write(table_html, unsafe_allow_html=True)

    st.markdown("""
        <style>
            table td {
                text-align: center;
            }
            table th {
                text-align: center;
                background-color: #996600;
            }
        </style>
    """, unsafe_allow_html=True)

def display_reviews():
    c.execute("SELECT * FROM reviews")
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Review', 'Game Review Prediction'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Reviews")
    
    # Display Table
    table_html = df.to_html(escape=False, index=False)
    table_html = table_html.replace('<table', '<table style="width:100%;"')
    st.write(table_html, unsafe_allow_html=True)

    st.markdown("""
        <style>
            table td {
                text-align: center;
            }
            table th {
                text-align: center;
                background-color: #996600;
            }
        </style>
    """, unsafe_allow_html=True)

def display_games_adv():
    c.execute("SELECT * FROM games")
    data = c.fetchall()
    
    # Degine headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Rank'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Games Adv")
    
    # Define a list of options
    options = []
    
    for row in data:
        options.append(st.checkbox("GAME NAME ----------------------- [ {} ]\n\nGAME RANK ----------------------- [ {} ]".format(*row[1:])))

    # Define an empty list to hold the selected options
    selected_options = []
    for i in range(len(options)):
        if options[i]:
            selected_options.append(data[i][0])

    if st.button("Delete Selected Games"):
        if(len(selected_options) > 0):
            selected_ids = ','.join(map(str, selected_options))

            # Delete from reviews
            c.execute(f"SELECT game_name FROM games WHERE id IN ({selected_ids})")
            game_names = c.fetchall()
            for game_name in game_names:
                c.execute("DELETE FROM reviews WHERE game_name = ?", game_name)
                conn.commit()
            
            # Delete from games
            c.execute(f"DELETE FROM games WHERE id IN ({selected_ids})")
            conn.commit()

            st.session_state.flag = 'delete_game_success'

            st.session_state.page = 'admin'
            st.experimental_rerun()

        else:
            st.session_state.flag = 'delete_game_warning'
    
    
    if st.session_state.flag == 'delete_game_success':
        success_game_deletion()
    elif st.session_state.flag == 'delete_game_warning':
        warning_game_deletion()
    
    new_game = st.text_input("Enter the name of new game:")
    if st.button("Add New Game"):
        if new_game == '':
            st.warning("Please enter a game name to add")
            st.session_state.flag = 'none'
        else:
            c.execute("SELECT COUNT(*) FROM games WHERE game_name=?", (new_game,))
            if c.fetchone()[0] > 0:
                # Game already exists
                st.session_state.flag = 'add_game_warning'
            else:
                # Insert new game
                c.execute("INSERT INTO games (game_name, game_rank) VALUES (?, ?)", (new_game,0))
                conn.commit()
                st.session_state.flag = 'add_game_success'

            st.session_state.page = 'admin'
            st.experimental_rerun()

    if st.session_state.flag == 'add_game_warning':
        warning()
    elif st.session_state.flag == 'add_game_success':
        success()

def display_reviews_adv():
    c.execute("SELECT * FROM reviews")
    data = c.fetchall()

    # Define headers
    df = pd.DataFrame(data, columns=['ID', 'Game Name', 'Game Review', 'Game Review Prediction'])
    df = df.set_index('ID')
    df.index.name = None

    st.write("### Reviews Adv")

    # Define a list of options
    options = []
    
    for row in data:
        options.append(st.checkbox("GAME NAME ----------------------- [ {} ]\n\nGAME REVIEW -------------------- [ {} ]\n\nGAME REVIEW PREDICTION --- [ {} ]".format(*row[1:])))

    # Define an empty list to hold the selected options
    selected_options = []
    for i in range(len(options)):
        if options[i]:
            selected_options.append(data[i][0])

    if st.button("Delete Selected Reviews"):
        if(len(selected_options) > 0):
            selected_ids = ','.join(map(str, selected_options))
            c.execute(f"DELETE FROM reviews WHERE id IN ({selected_ids})")
            conn.commit()
        
            st.session_state.flag = 'delete_review_success'

            st.session_state.page = 'admin'
            st.experimental_rerun()

        else:
            st.session_state.flag = 'delete_review_warning'
    
    if st.session_state.flag == 'delete_review_success':
        success_review_deletion()
    elif st.session_state.flag == 'delete_review_warning':
        warning_review_deletion()

def home_page():
    st.title("Game Review App")

    # Add buttons to select user type
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Admin", key='admin'):
                st.session_state.page = 'admin'
                st.experimental_rerun() 
        with col2:
            if st.button("Tester", key='tester'):
                st.session_state.page = 'tester'
                st.experimental_rerun()
        with col3:
            if st.button("Client", key='client'):
                st.session_state.page = 'client'
                st.experimental_rerun()   

def admin_page():
    # Add a home button to go back to the main page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun() 

    st.title("Admin Page")
    
    st.markdown("---")
    display_games_adv()
    st.markdown("---")
    display_reviews_adv()

def tester_page():
    # Add a home button to go back to the main page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun() 

    st.title("Tester Page")

    # Add an input field for the tester to enter text review
    review = st.text_input("Enter your review:")

    # Add a button to trigger the analysis
    if st.button("Analyze"):
        # Use the loaded model to predict the sentiment of the input review
        file_name = open("vectorizer.pkl", "rb")
        vectorizer = pickle.load(file_name)
        prediction = model.predict(vectorizer.transform([review]))

        # Display the predicted sentiment
        if prediction[0] == 'Positive':
            st.write("The review is Positive.")
        elif prediction[0] == 'Negative':
            st.write("The review is Negative.")
    
    display_reviews()

def client_page():
    # Add a home button to go back to the main page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.experimental_rerun() 

    st.title("Client Page")

if __name__ == '__main__':
    # Reload on any code changes
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Load the pre-trained model
    file_name = open("knn.pkl", "rb")
    model = pickle.load(file_name)

    # Database setup
    conn = sqlite3.connect('game_review_database.db')
    c = conn.cursor()

    # Table setup
    table_setup()

    # Initialize the page state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # Initialize the flag state
    if 'flag' not in st.session_state:
        st.session_state.flag = 'none'

    # Execute the appropriate page function based on the current page
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'admin':
        admin_page()
    elif st.session_state.page == 'tester':
        tester_page()
    elif st.session_state.page == 'client':
        client_page()
    
    