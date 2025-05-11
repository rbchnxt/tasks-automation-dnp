Note:
==================================================================================
First copy the sample CD docs and corresponding sqls files in respective folder.
Then run below commands or run batch file. 
Once running above commands visit http://127.0.0.1:5000 in your browser.



This is a combined training + inference web app.
1. Place your training DOCX files in 'training_data/docs/'
2. Place matching .SQL files in 'training_data/sqls/' (same base filename)
3. Run 'train_model.bat' to train the model.
4. After training, run 'start_webapp.bat' to start the web interface.

==================================================================================

or after copying the docs, sqls Use below Commands (manual)
================================================================
unzip sql_gen_app.zip
cd sql_gen_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py



