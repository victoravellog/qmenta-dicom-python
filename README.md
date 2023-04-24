# qmenta-dicom-python
Qmenta challenge. API that analize dicom files with fastapi and pydicom.

Implemented Auth with OAuth2 and users control.
Implemented endpoints to read the PatientName propertie on a dicom file send it through form-multipart field.
Main endpoints:
```sh
POST /auth/token              # Request a new token to interact with the api
POST /users                   # Creates a new user
POST /dicom/data/patient_name # Retrieves the PatientName propertie of the dicom attached file
POST /data/slice_image        # Retrives the base64 encoded png file
```

To launch the app you must have installed Docker and Docker compose. After that, run the next command on your terminal:

```sh
docker compose up --build
```
