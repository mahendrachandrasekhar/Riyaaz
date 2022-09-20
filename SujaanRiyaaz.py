import streamlit as st
import pandas as pd
import Riyaaz
st.image("Sujaan.png", caption=None, width=500, use_column_width=True, clamp=False, channels="RGB", output_format="auto")

instrument = ""
outFileSuffix = "sample"
with st.form(key='my_form'):
    cols1 = st.columns(3)
    for i, col1 in enumerate(cols1):
       if i == 0:
           inputRaag = col1.selectbox('Select the Raaga',('AhirBhairav','Bhairav','Bhairavi','Bhimpalasi','Bhoopali','Bhupeshwari','Bihag','Bilawal','Charukeshi','Keerwani','Khamaj','Malkauns','Rageshree','Shivranjini','Todi','Vibhas','Yaman'),index=8,key="inputRaag")
       elif i == 1:
           inputPitch = col1.selectbox('Select the Pitch',('A','A#','B','C','C#','D','D#','E','F','F#','G','G#'),index=4,key="inputPitch")
       elif i == 2:
           speed = col1.selectbox('Select the Speed',('1024th','512th','256th','128th','64th','32nd','16th','eighth','quarter','half','whole','breve','long','maxima'),index=8,key="speed")
        
    cols2 = st.columns(1)
    for i, col2 in enumerate(cols2):
           col2.subheader("Pick Pre-Defined Patterns", anchor=None)
    cols3 = st.columns(2)
    for i, col in enumerate(cols3):
       if i == 0:
           includeAarohAvaroh = col.checkbox('Aaroh/Avaroh', key='includeAarohAvaroh',value=True)
           includeBasicPattern3 = col.checkbox('Increasing Note E.g. S, SRS, SRGRS...', key='includeBasicPattern3',value=False)
       elif i == 1:
           includeBasicPattern2 = col.checkbox('1st Note Fixed E.g. SS, SR, SG, ...', key='includeBasicPattern2',value=False)
           includeBasicPaltas   = col.checkbox('Some Built-in Notations', key='includeBasicPaltas',value=False)
           includeLibraryPaltas = col.checkbox('Include Palta Patterns from our in-built library.', key='includeLibraryPaltas',value=False)
    
    cols4 = st.columns(1)
    for i, col4 in enumerate(cols4):
       inputPattern = col4.text_area("Generate your own Palta Patterns", value="", height=None, max_chars=None, key="inputPattern")
       col4.subheader("Merukhand", anchor=None)
    cols5 = st.columns(2)
    for i, col5 in enumerate(cols5):
       if i == 0:
           includeMerukhand = col5.checkbox('Include Merukhand', key='includeMerukhand',value=False)
       if i == 1:
           merukhandPattern = col5.text_input("Enter the Merukhand Pattern (or leave blank for default)", key="merukhandPattern")


    submitted = st.form_submit_button('Submit')
    if submitted:
        Riyaaz.run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)
        audio_file = open(outFileSuffix+'.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        txtOutput = pd.read_csv(outFileSuffix+".csv",header=None)
        for pattern in txtOutput[0]:
            st.write(pattern)
        

#st.write('You selected:', inputPitch)
# You can access the value at any point with:
#st.session_state.name
#st.write('You selected:', outFileSuffix)

