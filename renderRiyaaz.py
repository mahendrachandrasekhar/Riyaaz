from operator import mod
from ssl import SSLSession
import streamlit as st
import streamlit_ext as ste
import requests
import gsheetData
#import os
#import pathlib

import pandas as pd
from datetime import datetime
import mainRiyaaz

st.set_page_config(page_title='Daily Riyaaz')
st.image("Riyaaz.png", caption=None, width=500, use_column_width=True, clamp=False, channels="RGB", output_format="auto")

instrument = ""
currTime = datetime.now()

RaagaList = gsheetData.get_gsheet("RaagaList")
SpeedList = gsheetData.get_gsheet("SpeedList")
PitchList = gsheetData.get_gsheet("PitchList")
InstrumentList = gsheetData.get_gsheet("InstrumentList")
Message = gsheetData.get_gsheet("Message")
#print(pathlib.Path(__file__).stem)
#session = requests.Session()
a = [{"access_token":"ya29.a0Aa4xrXPikdEQhogFcjcKAHu0enZFhidrPvFd5et273BAOsY8p4eYTfWUi13_TOB0U5VWZ9lQGKB5J2KpFMxjGQbpKuBcEAckdQEAWJzKlydWr4QYRNjGr0mZS5RGIgsteUgw49IUhJMhgLJSZlCNrCeZuX2XaCgYKATASARMSFQEjDvL9Jt4yAOtAySCw3ysf03d5DQ0163","expires_on":"2022-10-29T10:19:11.2503730Z","id_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc3Y2MwZWY0YzcxODFjZjRjMGRjZWY3YjYwYWUyOGNjOTAyMmM3NmIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1NDkxMzA4NDM0ODQtaDY5cHFlc2s0bmltazQ3N2d0Zmp2ZGxoY2IycWVuOWkuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1NDkxMzA4NDM0ODQtaDY5cHFlc2s0bmltazQ3N2d0Zmp2ZGxoY2IycWVuOWkuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE3MzQxNDk4MTQ4MjYwMjUzNTEiLCJlbWFpbCI6InNoaXZnYW5nYTNjaHNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiI5N1VrZmVwcVRLYlFnR2UtRHZldEpRIiwibmFtZSI6IlNoaXYgR2FuZ2EgMyBDSFMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUxtNXd1M3NWbHFXUUg0bzFjMElUaC1WQm1sOW1JM3o4TEhBT2xSd2tLdWI9czk2LWMiLCJnaXZlbl9uYW1lIjoiU2hpdiBHYW5nYSAzIiwiZmFtaWx5X25hbWUiOiJDSFMiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTY2NzAzNTE1MiwiZXhwIjoxNjY3MDM4NzUyfQ.sluv9AiKw_7-Ep0DK7B6NpwYw-jA0yhCyPzE-yTKhuEh1X6UFZxUACUr11dlB3YxMQgOEuEZl7msJ3gfnyU8FLxHLdcCYsHb0K-AT3o9Db2VyOumurvesuCXvx8_beh2IfIYUC6EcHObVWy3a7phjLIpyuIxXzcgxPOv9I5VMnNsaOig36DkGKjxOed_yvPWQnw6v9yYKa3r8fduYMAnMfLO-lYfWHPhOhNXK6LBffLcrKNZ79OSKv-n8TF7DoKGJXuyk90iLa_XnbMFhfA5BuqT3UwZMP1ThZQYe8IQGT14S8VAJnMxxtU7ItS-xr4sV5qQQKzeBzua7SjztnTcsQ","provider_name":"google","user_claims":[{"typ":"iss","val":"https:\/\/accounts.google.com"},{"typ":"azp","val":"549130843484-h69pqesk4nimk477gtfjvdlhcb2qen9i.apps.googleusercontent.com"},{"typ":"aud","val":"549130843484-h69pqesk4nimk477gtfjvdlhcb2qen9i.apps.googleusercontent.com"},{"typ":"http:\/\/schemas.xmlsoap.org\/ws\/2005\/05\/identity\/claims\/nameidentifier","val":"111734149814826025351"},{"typ":"http:\/\/schemas.xmlsoap.org\/ws\/2005\/05\/identity\/claims\/emailaddress","val":"shivganga3chs@gmail.com"},{"typ":"email_verified","val":"true"},{"typ":"at_hash","val":"97UkfepqTKbQgGe-DvetJQ"},{"typ":"name","val":"Shiv Ganga 3 CHS"},{"typ":"picture","val":"https:\/\/lh3.googleusercontent.com\/a\/ALm5wu3sVlqWQH4o1c0ITh-VBml9mI3z8LHAOlRwkKub=s96-c"},{"typ":"http:\/\/schemas.xmlsoap.org\/ws\/2005\/05\/identity\/claims\/givenname","val":"Shiv Ganga 3"},{"typ":"http:\/\/schemas.xmlsoap.org\/ws\/2005\/05\/identity\/claims\/surname","val":"CHS"},{"typ":"locale","val":"en"},{"typ":"iat","val":"1667035152"},{"typ":"exp","val":"1667038752"}],"user_id":"shivganga3chs@gmail.com"}]
session = requests.get("https://riyaaz.azurewebsites.net/.auth/me")
#session = requests.get("https://github.com/streamlit/streamlit/issues/798")
st.write(session.content)
#gsheetData.set_gsheet("Feedback",str(session.content.,'UTF-8'))
#RaagaList = pd.read_csv("Data-RaagaList.csv")
#SpeedList = pd.read_csv("Data-SpeedList.csv")
#PitchList = pd.read_csv("Data-PitchList.csv")
#InstrumentList = pd.read_csv("Data-InstrumentList.csv")
#BannerMessage = 

##st.error("The site will be taken down soon..If you would like to keep it up, please leave your feedback in the Feedback tab. f there is enough of a demand, we will continue to support the site.")
st.error(Message.get("Message")[0])
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
