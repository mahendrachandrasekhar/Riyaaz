import streamlit as st
import streamlit_ext as ste
import pandas as pd
from datetime import datetime
import mainRiyaaz
#st.image("Sujaan.png", caption=None, width=500, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
st.set_page_config(page_title='Daily Riyaaz')

instrument = ""
currTime = datetime.now()

outFileSuffix = currTime.strftime("%Y%m%d%w%H%M%S%f")
tab1, tab2, tab3, tab4 = st.tabs(["Main", "Notations", "How To Use","Feedback"])
with tab1:
    with st.form(key='my_form'):
        cols1 = st.columns(4)
        for i, col1 in enumerate(cols1):
           if i == 0:
               inputRaag = col1.selectbox('Select the Thaat/Raaga',('Asavari','Bilawal','Bhairav','Bhairavi','Kalyan','Khamaj-Thaat','Kafi','Marva','Poorvi','Todi','AhirBhairav','Bhimpalasi','Bhoopali','Bhupeshwari','Bihag','Charukeshi','Keerwani','Khamaj','Malkauns','Rageshree','Shivranjini','Vibhas','Yaman'),index=1,key="inputRaag")
           elif i == 1:
               inputPitch = col1.selectbox('Select the Pitch',('A','A#','B','C','C#','D','D#','E','F','F#','G','G#'),index=4,key="inputPitch")
           elif i == 2:
               speed = col1.selectbox('Select the Speed',('64th','32nd','16th','eighth','quarter','half'),index=4,key="speed")
           elif i == 3:
               instrument = col1.selectbox('Select the Instrument',('Reed Organ','Harmonica','Harp','Voice','Koto','Shenai','Violin','Sitar','Cello','Ukulele','Guitar'),index=0,key="instrument")
            
        cols2 = st.columns(1)
        for i, col2 in enumerate(cols2):
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
    st.write('For Ideas & Suggestions, Contact: Mahendra Chandrasekhar, mahendracc@hotmail.com')
    #st.text('Follow Sujaan Music: https://www.facebook.com/sujaanmusic/')

###Formatting Options
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

########
if submitted:
    with st.spinner("Wait for it don't click Submit again..."):
        mainRiyaaz.run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)
        audio_file = open(outFileSuffix+'.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        txtOutput = pd.read_csv(outFileSuffix+".csv",header=None)
        ste.download_button("Download notations as CSV", txtOutput.to_csv().encode('utf-8'), "Notations.csv")
        csv = txtOutput.to_csv().encode('utf-8')
        for pattern in txtOutput[0]:
            st.write(pattern)

    mainRiyaaz.cleanupFile(outFileSuffix)         
