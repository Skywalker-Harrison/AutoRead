### This program is used for extracting vocabulary in the pdf file according to the user's level ###

####### Please modify the parameters according to your needs #######
PDF_FILE_PATH=/home/jhliang/fun/AutoRead/data/The_Road_Less_Traveled.pdf  # Please replace it with your own pdf file
USER_LEVEL=5 # 0-中考 1-高考 2-CET4 3-CET6 4-考研 5-TOEFL，IETLS 6-GRE
### Stage 1 Convert PDF to txt ###
# You don't need to change the code below. 
ROOT_PATH=$(dirname "$PDF_FILE_PATH")
ROOT_NAME=$(basename "$PDF_FILE_PATH")
FILE_NAME_WITHOUT_EXTENSION="${ROOT_NAME%.pdf}"
FILE_PATH=$ROOT_PATH/$FILE_NAME_WITHOUT_EXTENSION

TXT_FILE_PATH=$FILE_PATH".txt"
python ./pdf2txt/pdf2txt.py --input_file $PDF_FILE_PATH --output_file $TXT_FILE_PATH
echo "Convert txt file complete"

### Stage 2 Extract Words in the txt file ###
VOCAB_FILE_PATH=$FILE_PATH".vocab"
python ./txt2dic/Script/txt2dic.py --input_file $TXT_FILE_PATH --output_file $VOCAB_FILE_PATH
echo "Building Vocab Complete"

### Stage 3 Extract importance according to user's level ###
cd ECDICT
JSON_FILE_PATH=$FILE_PATH".json"
CSV_FILE_PATH=$FILE_PATH".csv"
python ./read_word_list.py --input_vocab_file $VOCAB_FILE_PATH --input_txt_file $TXT_FILE_PATH --user_level 5 --output_csv_file $CSV_FILE_PATH --output_json_file $JSON_FILE_PATH