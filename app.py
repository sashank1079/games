import streamlit as st
import pandas as pd
from random import randint

# Add the TEAM_CONFERENCES dictionary right after imports
TEAM_CONFERENCES = {
    # Eastern Conference
    'MIL': 'East', 'BOS': 'East', 'PHI': 'East', 'CLE': 'East', 'NYK': 'East',
    'BKN': 'East', 'MIA': 'East', 'ATL': 'East', 'TOR': 'East', 'CHI': 'East',
    'IND': 'East', 'WAS': 'East', 'ORL': 'East', 'CHA': 'East', 'DET': 'East',
    # Western Conference
    'DEN': 'West', 'MEM': 'West', 'SAC': 'West', 'PHX': 'West', 'LAC': 'West',
    'GSW': 'West', 'LAL': 'West', 'MIN': 'West', 'NOP': 'West', 'OKC': 'West',
    'POR': 'West', 'UTA': 'West', 'DAL': 'West', 'HOU': 'West', 'SAS': 'West'
}

# Set page config
st.set_page_config(
    page_title="NBA Player Guessing Game",
    page_icon="🏀",
    layout="centered"
)

# Initialize session state
if 'target_player' not in st.session_state:
    st.session_state.target_player = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 6
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'guesses' not in st.session_state:
    st.session_state.guesses = []

# Load and process players data
@st.cache_data
def load_players():
    players_df = pd.read_csv('players.txt', header=None, 
                            names=['name', 'team', 'position', 'height', 'weight'])
    return players_df

def reset_game():
    players_df = load_players()
    st.session_state.target_player = players_df.iloc[randint(0, len(players_df)-1)]
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.guesses = []

def compare_height(guess_height, target_height):
    if guess_height == target_height:
        return "🟢"
    
    def height_to_inches(h):
        ft, inch = map(int, h.split('-'))
        return ft * 12 + inch
    
    diff = abs(height_to_inches(guess_height) - height_to_inches(target_height))
    if diff <= 2:
        return "🟡"
    return "⚪"

def compare_weight(guess_weight, target_weight):
    if guess_weight == target_weight:
        return "🟢"
    if abs(guess_weight - target_weight) <= 15:
        return "🟡"
    return "⚪"

def compare_position(guess_pos, target_pos):
    if guess_pos == target_pos:
        return "🟢"
    guards = ['PG', 'SG']
    forwards = ['SF', 'PF']
    if (guess_pos in guards and target_pos in guards) or \
       (guess_pos in forwards and target_pos in forwards):
        return "🟡"
    return "⚪"

def compare_team(guess_team, target_team):
    if guess_team == target_team:
        return "🟢"
    # Check if teams are in the same conference
    if TEAM_CONFERENCES.get(guess_team) == TEAM_CONFERENCES.get(target_team):
        return "🟡"
    return "⚪"

# Title and Instructions
st.title("🏀 NBA Player Guessing Game")

with st.expander("How to Play", expanded=True):
    st.markdown("""
    ### Rules:
    1. Try to guess the NBA player in 6 attempts
    2. After each guess, you'll get feedback on five attributes
    3. Type the player's name exactly (case insensitive)
    
    ### Color Coding:
    - 🟢 Green: Exact match
    - 🟡 Yellow: Close match
    - ⚪ No color: Not a match
    
    ### Feedback Guide:
    - **Team**: 
        - 🟢 Same team
        - 🟡 Same conference
    - **Position**: 
        - 🟢 Same position (e.g., both PG)
        - 🟡 Similar position (PG/SG or SF/PF)
    - **Height**: 
        - 🟢 Exact same height
        - 🟡 Within 2 inches
    - **Weight**:
        - 🟢 Exact same weight
        - 🟡 Within 15 pounds
    """)

# Load players
players_df = load_players()

# Initialize game if needed
if st.session_state.target_player is None:
    reset_game()

# Create a new game button
if st.button("New Game"):
    reset_game()

# Player input and guessing
if not st.session_state.game_over:
    guess_name = st.text_input(
        f"Guess {st.session_state.attempts + 1}/6:",
        key=f"guess_{st.session_state.attempts}",
        placeholder="Type player name..."
    )

    if guess_name:
        # Find the player in the database
        player_match = players_df[players_df['name'].str.lower() == guess_name.lower()]
        
        if len(player_match) == 0:
            st.error("Oops! That player isn't in our database. Try again! 🤔")
        else:
            guess = player_match.iloc[0]
            target = st.session_state.target_player
            
            # Create feedback
            feedback = {
                'Name': '✓' if guess['name'] == target['name'] else '✗',
                'Team': compare_team(guess['team'], target['team']),
                'Position': compare_position(guess['position'], target['position']),
                'Height': compare_height(guess['height'], target['height']),
                'Weight': compare_weight(guess['weight'], target['weight'])
            }
            
            st.session_state.guesses.append((guess, feedback))
            st.session_state.attempts += 1
            
            # Check win/loss conditions before rerun
            if guess['name'].lower() == target['name'].lower():
                st.session_state.game_over = True
                st.success(f"🎉 Slam Dunk! You guessed the player in {st.session_state.attempts} attempts!")
                st.balloons()
            elif st.session_state.attempts >= st.session_state.max_attempts:
                st.session_state.game_over = True
                st.error(f"Game Over! The player was {target['name']}. Better luck next time! 🏀")
            
            # Only rerun if the game isn't over
            if not st.session_state.game_over:
                st.rerun()

# Display guess history
if st.session_state.guesses:
    st.markdown("### Guess History")
    for i, (guess, feedback) in enumerate(st.session_state.guesses, 1):
        with st.container():
            cols = st.columns(5)
            cols[0].markdown(f"**Name**: {guess['name']} {feedback['Name']}")
            cols[1].markdown(f"**Team**: {guess['team']} {feedback['Team']}")
            cols[2].markdown(f"**Position**: {guess['position']} {feedback['Position']}")
            cols[3].markdown(f"**Height**: {guess['height']} {feedback['Height']}")
            cols[4].markdown(f"**Weight**: {guess['weight']} {feedback['Weight']}")
            st.divider()

# Debug info (comment out in production)
if st.session_state.target_player is not None and st.checkbox("Show Answer (Debug)"):
    st.write("Target Player:", st.session_state.target_player['name'])

# Add footer with custom CSS
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: grey;
    text-align: center;
    padding: 10px;
    font-size: 12px;
}
</style>
<div class="footer">
    <p>Developed by Sashank Machiraju | <a href="https://github.com/sashank1079" target="_blank">GitHub</a> | 2024</p>
    <p>Keep ballin' and guessin'! 🏀</p>
</div>
""", unsafe_allow_html=True) 