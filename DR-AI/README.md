# Code parental utterances during shared reading using GEMINI

1. Transcribe an audio recording into an excel file (see [google colab](https://github.com/smy1/swlab/blob/main/script/audio2xlsx.ipynb)).
   
>[!IMPORTANT]  
> - The excel transcript must be converted into a csv file.  
> - Get a unique GEMINI API key and store it in a .env file: `GEMINI_API_KEY =  the-API-key`
   
2. Extract rules from a coding scheme (see [document](./peek.docx)).
3. Code the transcript using GEMINI (the [script](./drei.py) is modified slightly from [Prof Tsai's script](https://github.com/peculab/autogen_project/blob/main/DRai/DRai.py)).
   ```python
   python -m venv venv #create venv the first time
   .\venv\Scripts\activate #activate venv
   python .\drei.py mc51.csv ##code utterances of the file "mc51"
   deactivate #deactivate venv
   ```
4. The coding output is saved as a csv file.
5. Create a simple html page that shows the summary of scores.
