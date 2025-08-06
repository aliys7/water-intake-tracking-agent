import streamlit as st
import pandas as pd
from datetime import datetime
from scripts.agent import WaterIntakeAgent
from scripts.database import log_intake, get_intake_history

if 'tracker_started' not in st.session_state:
    st.session_state.tracker_started = False

# Welcome Message
if not st.session_state.tracker_started:
    st.title("Welcome to the Water Intake Tracker!")
    st.markdown(""" 
    Track your daily hydration with the help of an AI agent.
    Log your intake, get smart feedback, and stay hydrated!
    """)
    
    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()
    
else:
    st.title("Water Intake Tracking Agent")

    # Sidebar: Intake Input
    st.sidebar.header('Log Your Water Intake')
    user_id = st.sidebar.text_input('User ID', value='user_7')
    intake_ml = st.sidebar.number_input('Water Intake (ml)', min_value=0, step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id, intake_ml)
            st.success(f'Logged {intake_ml}ml for {user_id}')
            
            history = get_intake_history(user_id)
            daily_total = history[-1]['total_ml'] if history else intake_ml
            
            agent = WaterIntakeAgent()
            feedback = agent.analyze_intake(daily_total)
            st.info(f'Agent Feedback: {feedback}')
        
    # Divider
    st.markdown('---')

    # History Section
    st.header("Intake History")

    if user_id:
        history = get_intake_history(user_id)
        
        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No intake history found for this user.")