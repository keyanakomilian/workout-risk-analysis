from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
from analysis import perform_analysis 
from idlookup import lookup
import numpy as np
import os
import requests
from fhir_parser import FHIR
from fhir_parser import Patient
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
from io import BytesIO
import base64
from matplotlib.colors import Normalize

app = Flask(__name__)
app.secret_key = 'taylorswift'
data_folder = os.path.join(os.getcwd(), 'data')
static_folder = os.path.join(os.getcwd(), 'static')
fhirobj = FHIR()
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    #clear user-specific data from the session
    session.clear()
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.form.get('user_id') #from text box
    activity_file = request.files['activity_file'] #from upload
    sleep_file = request.files['sleep_file']

    #save uploaded files
    activity_file.save(f'data/{user_id}_activity.csv')
    sleep_file.save(f'data/{user_id}_sleep.csv')

    #do analysis
    apath = f'data/{user_id}_activity.csv'
    spath = f'data/{user_id}_sleep.csv'
    result, patientDF = perform_analysis(user_id, apath, spath) 
    avgSleep = (np.average(patientDF['TotalMinutesAsleep']))/60
    avgSleep = round(avgSleep, 2)
    sentence = 'Over the period of time logged by your wearable device, you slept for an average of ' + str(avgSleep) + ' hours per night. Given the amount of sleep you got and the minutes spent doing vigorous activity, the average risk of inadequate recovery from this amount of exercise is ' + str(round(result,2))+'.'
    if result >= 0.2:
        secondsent = 'Your average risk measurment indicates a lack of sleep for the amount of activity you have.'
    else:
        secondsent = 'Your average risk measurement indicates adequate sleep to ensure recovery from the amount you exercise.'
    # fig, ax = plt.subplots(figsize=(8, 6))
    # norm = Normalize(vmin=min(patientDF['Risk'])+0.1, vmax=max(patientDF['Risk'])+0.1)
    # normalized_values = norm(patientDF['Risk'])
    # cmap = plt.get_cmap('spring')
    # plt = seaborn.barplot(x=patientDF['Date'], y=patientDF['Risk'], data=patientDF, palette=cmap(normalized_values), ax=ax)
    # #plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.figure(figsize=(8, 6))
    norm = Normalize(vmin=min(patientDF['Risk'])+0.1, vmax=max(patientDF['Risk'])+0.1)
    normalized_values = norm(patientDF['Risk'])
    cmap = plt.get_cmap('spring')
    plt.bar(patientDF['Date'], patientDF['Risk'], color=[cmap(value) for value in normalized_values])
    plt.xlabel('Date')
    plt.ylabel('Risk Measurement')
    plt.title('Risk Levels By Day')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Verdana' 

    
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    plt.close()
    img_str = "data:image/png;base64," + base64.b64encode(img_buf.read()).decode('utf-8')


    fhirID = lookup(user_id) #fhir id and the ids in the fitbit data are not the same, this function looks it up for you 
    print('fhir id', fhirID)
    #fhirID = "421e45e2-0ad3-e5c3-9e0f-2cb25f672354"
     #search for patient based on fhir id
    search_url = f'http://localhost:8080/fhir/Patient?identifier={fhirID}'
    search_response = requests.get(search_url)

    if search_response.status_code == 200:
        #get the matching patient 
        existing_patient_data = search_response.json().get('entry', [{}])[0].get('resource', {})
        existing_patient_id = existing_patient_data.get('id', None)
        print(existing_patient_data)
        #exit extension to the avg risk value
        #existing_patient_data['extension'] = [{'url': 'risk', 'valueDecimal': result}]

        if existing_patient_id:
            
            existing_patient_data['extension'] = [{'url': 'risk', 'valueDecimal': result}]

            #update resource on server
            update_url = f'http://localhost:8080/fhir/Patient/{existing_patient_id}'
            update_response = requests.put(update_url, json=existing_patient_data)

            if update_response.status_code == 200:
                print(f"Patient {user_id} updated successfully.")
            else:
                print(f"Error updating Patient {user_id}: {update_response.status_code}")
        else:
            print(f"Error: Patient {user_id} not found in the FHIR server.")

    return render_template('chart_display.html', img_data=img_str, variable1= sentence, variable2= secondsent)

#for styling 
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_folder, filename)



if __name__ == '__main__':
    
#app.run(host="0.0.0.0", port=port)
    app.run(host="0.0.0.0", port=port)

#something i can try is to retrieve the patient from the server (like previously uploaded) then add the risk exention
#to do this, i would have to rename their IDs to their names from synthea
