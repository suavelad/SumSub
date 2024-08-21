##  SumSub Applicant Creation Flow

    - Make the API call the SumSub 
    - Save the response of the DB (if successful)



## Sample SQL DB Schema 

- User Model
  - UserId
  - FirstName
  - LastName
  - Gender
  - DoB
  - Phone
  - Email
  - ApplicantId
  - VerificationStatus
  - Verified Document Count  //To track when all the documents has been uploaded
  - AllDocumentUploaded 


- SumSub Applicant Model
  - ApplicantId
  - Applicant JSON


- User Document Model
  - UserId
  - ApplicantId
  - DocType
  - FileUrl
  - Document Number
  - Country
  - ImageId  //from SumSub



- SumSub Applicant Document Model
  - ApplicantId
  - ImageId
  - Document Response JSON





## Applicant SumSub Process

   * You can review the get started guide before you start: https://docs.sumsub.com/reference/get-started-with-api


     - Create Applicant:
          (See this:  https://docs.sumsub.com/reference/create-applicant)
    
     - Applicant upload document:
          (See this: https://docs.sumsub.com/reference/add-id-documents)
    
     - Alert SumSub to start the verification: 
            Nice to have. It can be used if a mistake is detected; it will also change 
            the status to pending. check the documentation for more details: https://docs.sumsub.com/reference/request-applicant-check
    
     - Verify applicant verification status: 
            (Check the documentation for more details: https://docs.sumsub.com/reference/get-applicant-verification-steps-status)


     - Setup Webhook: 
        This will help you get verification results 
        (Check the documentation for more details: https://docs.sumsub.com/docs/webhooks)


        
            SAMPLE WEBHOOK RESPONSE WITH RED:
              {
                "applicantId": "5cb744200a975a67ed1798a4",
                "inspectionId": "5cb744200a975a67ed1798a5",
                "correlationId": "req-fa94263f-0b23-42d7-9393-ab10b28ef42d",
                "externalUserId": "externalUserId",
                "levelName": "basic-kyc-level",
                "type": "applicantReviewed",
                "reviewResult": {
                  "moderationComment": "We could not verify your profile. If you have any questions, 
                                        please contact the Company where you try to verify your profile ${clientSupportEmail}",
                  "clientComment": " Suspected fraudulent account.",
                  "reviewAnswer": "RED",
                  "rejectLabels": ["UNSATISFACTORY_PHOTOS", "GRAPHIC_EDITOR", "FORGERY"],
                  "reviewRejectType": "FINAL"
                },
                "reviewStatus": "completed",
                "createdAtMs": "2020-02-21 13:23:19.001"
              }
            

              SAMPLE WEHBOOK RESPONSE WITH GREEN:
                  {
                  "applicantId": "5cb56e8e0a975a35f333cb83",
                  "inspectionId": "5cb56e8e0a975a35f333cb84",
                  "correlationId": "req-a260b669-4f14-4bb5-a4c5-ac0218acb9a4",
                  "externalUserId": "externalUserId",
                  "levelName": "basic-kyc-level",
                  "type": "applicantReviewed",
                  "reviewResult": {
                    "reviewAnswer": "GREEN"
                  },
                  "reviewStatus": "completed",
                  "createdAtMs": "2020-02-21 13:23:19.321"
              }