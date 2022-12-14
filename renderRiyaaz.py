from operator import mod
from ssl import SSLSession
import streamlit as st
import streamlit_ext as ste
import gsheetData
import pandas as pd
from datetime import datetime
from streamlit.web.server.websocket_headers import _get_websocket_headers
import mainRiyaaz

st.set_page_config(page_title='Daily Riyaaz')
st.image("Banner.png", caption=None, width=500, use_column_width=True, clamp=False, channels="RGB", output_format="auto")

instrument = ""
currTime = datetime.now()

RaagaList = gsheetData.get_gsheet("RaagaList")
SpeedList = gsheetData.get_gsheet("SpeedList")
PitchList = gsheetData.get_gsheet("PitchList")
InstrumentList = gsheetData.get_gsheet("InstrumentList")
Message = gsheetData.get_gsheet("Message")

headers = _get_websocket_headers()
try:
    st.error('Welcome ' + headers.get('X-Ms-Client-Principal-Name') +'. '+ Message.get("Message")[0])
    gsheetData.set_gsheet("ActivityLog",[str(currTime),headers.get('X-Ms-Client-Principal-Name')])
except (KeyError, TypeError):
    st.error("Not Logged in." +'. '+ Message.get("Message")[0])
    gsheetData.set_gsheet("ActivityLog",[str(currTime),headers.get('Sec-Websocket-Key')])

outFileSuffix = currTime.strftime("%Y%m%d%w%H%M%S%f")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Main", "Notations", "How To Use","Feedback","Instrument Samples"])
with tab1:
    with st.form(key='my_form'):
        cols1 = st.columns(4)
        for i, col1 in enumerate(cols1):
           if i == 0:
               inputRaag = col1.selectbox('Thaat/Raaga',RaagaList,index=1,key="inputRaag")
           elif i == 1:
               inputPitch = col1.selectbox('Pitch',PitchList,index=4,key="inputPitch")
           elif i == 2:
               speed = col1.selectbox('Speed',SpeedList,index=3,key="speed")
           elif i == 3:
               instrument = col1.selectbox('Instrument',InstrumentList,index=0,key="instrument")


        cols2 = st.columns(1)
        for i, col2 in enumerate(cols2):
            if i == 0:
                col2.markdown('#### _Pick Pre-Defined Patterns_')

        cols3 = st.columns(2)
        for i, col in enumerate(cols3):
           if i == 0:
               includeAarohAvaroh = col.checkbox('Aaroh/Avaroh', key='includeAarohAvaroh',value=True)
               includeBasicPattern3 = col.checkbox('Increasing Note E.g. S, SRS, SRGRS...', key='includeBasicPattern3',value=False)
           elif i == 1:
               includeBasicPattern2 = col.checkbox('1st Note Fixed E.g. SS, SR, SG, ...', key='includeBasicPattern2',value=False)
               includeBasicPaltas   = col.checkbox('Some Built-in Notations', key='includeBasicPaltas',value=False)
               includeLibraryPaltas = col.checkbox('Palta Patterns from our in-built library.', key='includeLibraryPaltas',value=False)
        
        cols4 = st.columns(1)
        for i, col4 in enumerate(cols4):
           inputPattern = col4.text_area("Generate your own Palta Patterns", value="", height=None, max_chars=None, key="inputPattern")
           col4.markdown('#### _Merukhand_')
        cols5 = st.columns(2)
        for i, col5 in enumerate(cols5):
           if i == 0:
               includeMerukhand = col5.checkbox('Include Merukhand', key='includeMerukhand',value=False)
           if i == 1:
               merukhandPattern = col5.text_input("Merukhand Pattern (or leave blank for default)", key="merukhandPattern")
    
    
        submitted = st.form_submit_button('Submit')
with tab2:
    st.image("Notations.png", caption=None, width=400, clamp=False, channels="RGB", output_format="auto")
with tab3:
    st.image("HowToUseTheApplication.png", caption=None, width=500, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
with tab4:
    with st.form(key='feedback'):
        st.error('For Ideas & Suggestions, Contact: Mahendra Chandrasekhar, mahendracc@hotmail.com, or enter your feedback below')
        email = st.text_input("Your Name/Email",key="email")
        feedback = st.text_area("Your Feedback", value="", height=None, max_chars=None, key="feedback")
        #st.text('Follow Sujaan Music: https://www.facebook.com/sujaanmusic/')
        feedback_given = st.form_submit_button('Send Feedback')
with tab5:
        cols6 = st.columns(2)
        myLen = len(InstrumentList["InstrumentName"])
        for i, col6 in enumerate(cols6):
            if i == 0:
                currLen = 0
                for myinstrument in InstrumentList["InstrumentName"]:
                    if currLen%2 == 0:
                        col6.write(myinstrument)
                        r_audio_file = open("InstrumentSamples/"+myinstrument+'.mp3', 'rb')
                        r_audio_bytes = r_audio_file.read()
                        col6.audio(r_audio_bytes, format='audio/mp3')
                    currLen +=1
            if i == 1:
                currLen = 0
                for myinstrument in InstrumentList["InstrumentName"]:
                    if currLen%2 == 1:
                        col6.write(myinstrument)
                        r_audio_file = open("InstrumentSamples/"+myinstrument+'.mp3', 'rb')
                        r_audio_bytes = r_audio_file.read()
                        col6.audio(r_audio_bytes, format='audio/mp3')
                    currLen +=1

###Formatting Options
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if feedback_given:
    if len(email) < 3 and len(feedback) < 4:
        st.write("No Text Entered or text too small")
    else:
        gsheetData.set_gsheet("Feedback",[email,feedback])
        st.write("Thank you for your feedback")


########
if submitted:
    with st.spinner("Wait for it don't click Submit again. Meanwhile you can put in your feedback in the Feedback Tab..."):
        mainRiyaaz.run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)
        audio_file = open(outFileSuffix+'.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        txtOutput = open(outFileSuffix+".csv","r")
        ste.download_button("Download notations as TXT", txtOutput.read(), "Notations.txt")
        txtOutput.close()

        txtOutput = open(outFileSuffix+".csv","r")
        for pattern in txtOutput.readlines():
            st.write(pattern)
        txtOutput.close()

    mainRiyaaz.cleanupFile(outFileSuffix)         
