# Automatically code parental utterances using the PEER scheme

1. Transcribe an audio recording into an excel file (see [google colab](https://github.com/smy1/swlab/blob/main/script/audio2xlsx.ipynb)).
2. Convert the excel transcript into a csv file.
   
>[!IMPORTANT]  
> - The excel transcript must be converted into a csv file.  
> - Get a unique GEMINI API key and store it in a .env file: `GEMINI_API_KEY =  the-API-key`
   
4. Extract rules from a coding scheme (see [document](./peek.docx)).
5. Code the transcript using GEMINI (the [script](./drei.py) is modified slightly from [Prof Tsai's github](https://github.com/peculab/autogen_project/blob/main/DRai/DRai.py)).
   ```python
   python -m venv venv #create venv the first time
   .\venv\Scripts\activate #activate venv
   python .\drei.py mc51.csv ##code utterances of the file "mc51"
   deactivate #deactivate venv
   ```
6. Present the coding output in a csv file.
7. Create a simple html page that shows the summary of scores.
