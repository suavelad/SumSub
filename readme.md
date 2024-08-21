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