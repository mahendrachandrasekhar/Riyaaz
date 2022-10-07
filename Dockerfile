FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive
ENV QT_QPA_PLATFORM=offscreen
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update 
RUN apt install python3.8 -y
RUN apt install python3-pip -y
RUN pip3 install pandas
RUN add-apt-repository universe -y
RUN apt-get update
RUN apt-get upgrade -y
RUN add-apt-repository ppa:mscore-ubuntu/mscore3-stable -y
RUN apt-get update
RUN apt-get install musescore3 -y
RUN strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5
RUN pip3 install streamlit
RUN pip3 install streamlit-ext
RUN pip3 install jinja2==3.0.1
RUN apt install git -y
RUN pip3 install gspread
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN git clone https://github.com/mahendrachandrasekhar/Riyaaz.git
RUN mkdir .config
RUN cd .config
RUN mkdir gspread
RUN cd gspread
COPY /.config/gspread/service_account.json /Riyaaz/.config/gspread/service_account.json
WORKDIR /Riyaaz
ENTRYPOINT ["streamlit", "run", "renderRiyaaz.py", "--server.port=8502", "--server.address=0.0.0.0"]
EXPOSE 8502
