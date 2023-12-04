import json

# Load the bundle JSON
path = '/Users/keyanakomilian/Desktop/6440_project/synthea-master/output/fhir/Lorna458_Bashirian201_325cd99c-840d-ad30-555b-75e680f2e103.json'
with open(path, 'r') as f:
    bundle_data = json.load(f)

patient_resource = None
for entry in bundle_data.get('entry', []):
    if entry.get('resource', {}).get('resourceType') == 'Patient':
        patient_resource = entry['resource']
        break

if patient_resource:
    with open('patient_resource25.json', 'w') as f:
        json.dump(patient_resource, f, indent=2)

#first run this extract code with the patient resource bundle
#then run this curl command. make sure to replace path
#run this to verify that it was uploaded (can check on webapp)
#curl -X GET http://localhost:8080/fhir/R4/Patient

#curl -X POST -H "Content-Type: application/fhir+json" -d @/Users/keyanakomilian/Desktop/6440_project/project-root/patient_resource8.json http://localhost:8080/fhir/Patient

