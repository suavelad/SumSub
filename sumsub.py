import os
import requests
import json
from decouple import config
from loguru import logger

from helper import signed_payload


SUMSUB_TEST_BASE_URL = config('SUMSUB_TEST_BASE_URL')
REQUEST_TIMEOUT = config('REQUEST_TIMEOUT')


payload = {
          "externalUserId": "externalUserId", #the id of the user identifier our application 
          "email": "john.smith@sumsub.com",
          "phone": "+449112081223",
          "fixedInfo": {
              "country": "GBR",
              "placeOfBirth": "London"
          }
      }

doc_metadata_payload = {
                "metadata":{
                    "idDocType":"PASSPORT", 
                    "idDocSubType": "FRONT_SIDE",  # optional
                    "country":"USA", 
                    "firstName" : "Doe" , # optional
                    "lasttName":"Jane" , # optional
                    "issuedDate": "2010-09-25", # optional
                    "validUntil": "2025-09-25" # optional
                    }
                }

class SumSub:

    def __init__(self) -> None:
        self.SUMSUB_BASE_URL  = config('SUMSUB_TEST_BASE_URL')
        self.REQUEST_TIMEOUT = config('REQUEST_TIMEOUT')
        self.base_headers = {
                            'Content-Type': 'application/json',
                            'Content-Encoding': 'utf-8'
                        }
        
    
    def _send_request(self, method, url, params=None, data=None, files=None):
        try:
            request = requests.Request(method, url, params=params, data=data, headers=self.base_headers, files=files)
            signed_request = signed_payload(request)
            with requests.Session() as session:
                response = session.send(signed_request, timeout=self.request_timeout)
                response.raise_for_status()
                return response
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            return None


    def _download_file(self, url, file_name):
        try:
            with requests.get(url, stream=True, timeout=self.request_timeout) as response:
                response.raise_for_status()
                with open(file_name, 'wb') as file_handle:
                    for block in response.iter_content(1024):
                        if block:
                            file_handle.write(block)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download file: {e}")
            raise


    def _cleanup_temp_file(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
            logger.info(f"Temporary file {file_name} deleted")
        else:
            logger.warning(f"Temporary file {file_name} not found")


    def get_access_token(self,external_user_id, level_name):
        
        params = {'userId': external_user_id, 'ttlInSecs': '600', 'levelName': level_name}
        resp = signed_payload(requests.Request('POST', self.SUMSUB_BASE_URL + '/resources/accessTokens',
                                            params=params,
                                            headers=self.base_headers))
        s = requests.Session()
        response = s.send(resp, timeout=REQUEST_TIMEOUT)
        token = (response.json()['token'])

        return token


    def create_Sumsub_applicant(self,payload,level_name):
        params = {'levelName': level_name}
        URL = f"{self.SUMSUB_BASE_URL}/resources/applicants?levelName={level_name}"

        response = self._send_request('POST', URL, params=params, data=json.dumps(payload))

        if not response:
            logger.error("Error occurred when creating the SumSub Applicant")
            return False,  "Unable to create Appliciant"

        if response.status_code not in [200,201]:
            logger.error("Error occurred when creating SumSub Applicant | Error: {response}")
            return False, "Unable to create Appliciant"
        

            # Applicant Object:
            # {
            #     "id": "5b594ade0a975a36c9349e66",
            #     "createdAt": "2020-06-24 05:05:14",
            #     "clientId": "ClientName",
            #     "inspectionId": "5b594ade0a975a36c9379e67",
            #     "externalUserId": "SomeExternalUserId",
            #     "fixedInfo": {
            #         "firstName": "Chris",
            #         "lastName": "Smith"
            #     },
            #     "info": {
            #         "firstName": "CHRISTIAN",
            #         "firstNameEn": "CHRISTIAN",
            #         "lastName": "SMITH",
            #         "lastNameEn": "SMITH",
            #         "dob": "1989-07-16",
            #         "country": "DEU",
            #         "idDocs": [
            #         {
            #             "idDocType": "ID_CARD",
            #             "country": "DEU",
            #             "firstName": "CHRISTIAN",
            #             "firstNameEn": "CHRISTIAN",
            #             "lastName": "SMITH",
            #             "lastNameEn": "SMITH",
            #             "validUntil": "2028-09-04",
            #             "number": "LGXX359T8",
            #             "dob": "1989-07-16",
            #             "mrzLine1": "IDD<<LGXX359T88<<<<<<<<<<<<<<<",
            #             "mrzLine2": "8907167<2809045D<<<<<<<<<<<<<8",
            #             "mrzLine3": "SMITH<<CHRISTIAN<<<<<<<<<<<<<<"
            #         }
            #         ]
            #     },
            #     "agreement": {  //present when SDK was initialized with Agreement screen enabled
            #         "createdAt": "2020-06-24 04:18:40",
            #         "source": "WebSDK",
            #         "targets": [
            #         "By clicking Next, I accept [the Terms and Conditions](https://www.sumsub.com/consent-to-personal-data-processing/)",
            #         "I agree to the processing of my personal data, as described in [the Consent to Personal Data Processing](https://sumsub.com/consent-to-personal-data-processing/)"
            #         ]
            #     },
            #     "email": "christman1@gmail.com",
            #     "applicantPlatform": "Android",
            #     "requiredIdDocs": {
            #         "docSets": [
            #         {
            #             "idDocSetType": "IDENTITY",
            #             "types": [
            #             "PASSPORT",
            #             "ID_CARD"
            #             ]
            #         },
            #         {
            #             "idDocSetType": "SELFIE",
            #             "types": [
            #             "SELFIE"
            #             ]
            #         }
            #         ]
            #     },
            #     "review": {
            #         "elapsedSincePendingMs": 115879,
            #         "elapsedSinceQueuedMs": 95785,
            #         "reprocessing": true,
            #         "levelName": "basic-kyc",
            #         "createDate": "2020-06-24 05:11:02+0000",
            #         "reviewDate": "2020-06-24 05:12:58+0000",
            #         "reviewResult": {
            #         "reviewAnswer": "GREEN"
            #         },
            #         "reviewStatus": "completed"
            #     },
            #     "lang": "de",
            #     "type": "individual"
            # }

        applicant_object = response.json()

        #  returns:  status and  applicant response json 
        return True,applicant_object
        
            

    def get_applicant_status(self,applicantId):
        URL = f"{self.SUMBSUB_BASE_URL}/resources/applicants/{applicantId}/requiredIdDocsStatus"

        response = self._send_request('GET', URL)

        if not response:
            logger.error("Error occurred when getting the  SumSub Applicant Status")
            return False,  "Unable to get Appliciant Status"


        if response.status_code not in [200,201]:
            logger.error("Error occurred when creating SumSub Applicant | Error: {response}")
            return False, "Unable to get  Appliciant status"
        
        # {
        #     "IDENTITY": {
        #     // a step identifier
        #         "reviewResult": {
        #         // if exists, that means that a document was uploaded
        #         "moderationComment": "Please upload a photo of the front of your ID card.",
        #         "reviewAnswer": "RED"
        #         },
        #         "country": "LVA", // document country
        #         "idDocType": "ID_CARD", // specific document type for the step
        #         "imageIds": [122352326,34246467], // image IDs that represent a document
        #         //If imageIds array contains more than one element, the first one would be front side and others - back sides
        #         "imageReviewResults": {
        #         "34246467": {
        #             "reviewAnswer": "GREEN"
        #         },
        #         "122352326": {
        #             "moderationComment": "Please upload a photo of the front of your ID card.", // A human-readable comment that can be shown to your end user
        #             "clientComment": "One side of the document is missing.",  //A human-readable comment that should not be shown to an end user, and is meant to be read by a client
        #             "reviewAnswer": "RED",
        #             "rejectLabels": ["DOCUMENT_PAGE_MISSING","FRONT_SIDE_MISSING"],
        #             "reviewRejectType": "RETRY"
        #         }
        #         }
        #     },
        #     "SELFIE": {
        #         "reviewResult": {
        #         "reviewAnswer": "GREEN"    #GREEN - approved, , RED- Rejected, if RED, there will be a new field called : moderationComment
        #         },
        #         "country": "LVA",
        #         "idDocType": "SELFIE",
        #         "imageIds": [181314576],
        #         "imageReviewResults": {
        #         "181314576": {
        #             "reviewAnswer": "GREEN"
        #         }
        #         }
        #     }
        # }
        return True,response.json()


    def add_Sumsub_applicant_document(self,applicant_id,doc_metadata_payload,doc_url):
        # img_url = 'https://icon.com/image.png'

        URL = f"{self.SUMBSUB_BASE_URL}/resources/applicants/{applicant_id}/info/idDoc"
        temp_file_name = 'img.jpg'

        try:
            self._download_file(doc_url, temp_file_name)
            with open(temp_file_name, 'rb') as file_handle:
                files = [('content', file_handle)]
                response = self._send_request('POST', URL, data=doc_metadata_payload, files=files)

            if not response:
                logger.error("Error occurred when uploading SumSub Applicant Document")
                return False,  "Unable to upload Appliciant Document"

            if response.status_code not in [200,201]:
                logger.error("Status Code was not 200 or 201 while uploading SumSub Applicant Document | Error: {response}")
                return False,  "Unable to upload Appliciant Document"
            
            document_object = response.json()
            image_id = response.headers.get('X-Image-Id')

        except Exception as e:
            logger.error(f"An error occurred during document upload: {e}")
            return False, None

        finally:
            self._cleanup_temp_file(temp_file_name)
        
        # returns status, document response json, image id 
         # Expected  Document object :
                # {
                # "idDocType": "PASSPORT",
                # "country": "GBR",
                # "issuedDate": "2015-01-02",
                # "number": "40111234567",
                # "dob": "2000-02-01",
                # "placeOfBirth": "London"
                # }

        return True, document_object, image_id