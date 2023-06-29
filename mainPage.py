# import libraries
import streamlit as st
import tkinter as tk
from tkinter import filedialog
from backend import run_all
import os

os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
os.environ['DISPLAY']=':1.0'    # tell X clients to use our virtual DISPLAY :1.0.

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

# printed output declaration
st.session_state["console_output"] = ""

# T A B S
tab1, tab2, tab3 = st.tabs(["Main Page", "Given Inputs", "Outputs"])


with tab1:
    # Folder picker button
    st.title('Nu Macro')
    
    # drop downs 
    
    # CLIENT NAME
    Options1 =[ "NoSelect","ACOSTA","AHOLD","ALBERTSONS","ALLEGIANCE","AMAZON","AWG","BASHAS","BIG Y","BJ'S","CARDINAL HEALTH","CHEWY","CIRCLE K","CUB",
    "CVS","DECA","DELHAIZE","DOLLAR GENERAL","FAMILY DOLLAR","GETGO","GIANT EAGLE","GNC","HYVEE","KROGER","LOWES","MEIJER","MEIJER CONVENIENCE","PET SUPERMARKET","PETCO","PETSMART","PRICE CHOPPER","PUBLIX","RALEYS","RITE AID", "SALLY BEAUTY","SAMS","SAVE A LOT","SAVEMART",
    "TARGET","UNFI","UNICORN","US PET SUPPLIES","US SMART AND FINAL","US SPARTANNASH","US WEIS","WAKEFERN","WALGREENS","WALMART","WEGMANS","WHOLEFOODS"]
    st.session_state["selected_option_client_name"] = st.selectbox("CLIENT NAME", Options1)
    
    # FREQUENCY
    Options2 =["No Select","WEEKLY","MONTHLY"]
    st.session_state["selected_option_frequency"] = st.selectbox("FREQUENCY", Options2)
    
    # CURRENT WEEK
    Options3 =[ "NoSelect","WK01","WK02","WK03","WK04","WK05","WK06","WK07","WK08","WK09","WK10","WK11","WK12","WK13","WK14","WK15","WK16","WK17","WK18","WK19","WK20","WK21","WK22","WK23","WK24","WK25","WK26","WK27","WK28","WK29","WK30","WK31","WK32","WK33","WK34","WK35","WK36","WK37","WK38","WK39","WK40","WK41","WK42","WK43","WK44","WK45","WK46","WK47","WK48","WK49","WK50","WK51","WK52"]
    st.session_state["selected_option_curr_week"] = st.selectbox("CURRENT WEEK", Options3)
    
    
    # PREVIOUS WEEK FOLDER PATH
    st.write('PREVIOUS WEEK FOLDER PATH:')
    clicked1 = st.button('Folder Picker 1')
    if clicked1:
        
        dirname1 = st.text_input('Selected folder1:', filedialog.askdirectory(master=root))
        st.session_state["folder1"] = str(dirname1)
    # CURRENT WEEK FOLDER PATH
    st.write('CURRENT WEEK FOLDER PATH:')
    clicked2 = st.button('Folder Picker 2')
    if clicked2:
        
        dirname2 = st.text_input('Selected folder2:', filedialog.askdirectory(master=root))
        st.session_state["folder2"] = str(dirname2)
    # path to write output file
    st.write('PATH TO WRITE OUTPUT FILE:')
    clicked3 = st.button('Folder Picker For OutputFile')
    if clicked3:
        
        dirname3 = st.text_input('Selected folder3:', filedialog.askdirectory(master=root))
        st.session_state["output_path"] = str(dirname3)
    
    
    
    Submit_btn = st.button("SUBMIT")
    if Submit_btn:
        list_of_file_1 = os.listdir(st.session_state["folder1"])
        list_of_file_2 = os.listdir(st.session_state["folder2"])
        if list_of_file_1 == list_of_file_2:
            run_all(st.session_state["folder1"],
                    st.session_state["folder2"],
                    st.session_state["output_path"],
                    st.session_state["selected_option_client_name"],
                    st.session_state["selected_option_frequency"],
                    st.session_state["selected_option_curr_week"])
            #----------------------------------
            # getting the printed values
            # Create a custom stream to capture console output
            import sys
            from io import StringIO
            stdout = sys.stdout
            string_io = StringIO()
            sys.stdout = string_io
            # Reset the standard output
            sys.stdout = stdout
            # Retrieve the captured console output
            st.session_state["console_output"] = string_io.getvalue()
            st.code(st.session_state["console_output"])
            # Display the console output in Streamlit
            #----------------------------------------
            st.success('Output File Uploaed successfully!', icon="✅")
            st.balloons()
        else:
            st.warning('File Names are not equal')
            st.stop()
with tab2:
    st.write(st.session_state)
    
with tab3:
    st.code(st.session_state["console_output"])


