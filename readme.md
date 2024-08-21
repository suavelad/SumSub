##  SumSub Applicant Creation Save to DB

    - Make the API call the SumSub 
    - Save the response of the DB



## DB Schema

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
  - Verified Document Count 
  - AllDocumentUploaded 


- SumSub Applicant Model
  - ApplicantId
  - Applicant JSON


- User Document Model
  - UserId
  - ApplicantId
  - DocType
  - FileUrl
  - ImageId //from sumsub



- SumSub Applicant Document Model
  - ApplicantId
  - ImageId
  - Document Response JSON





## Applicant SumSub Process
   * You can review the get started guide before you start: https://docs.sumsub.com/reference/get-started-with-api
    - Create  Applicant (See this: https://docs.sumsub.com/reference/create-applicant)
    
    - Applicant upload document (See this: https://docs.sumsub.com/reference/add-id-documents)
    
    - Alert SumSub to start the verification (request applicant check) (Nice to have. Can be used if a mistake was detected, also it will change the status to pending. check the documentation for more details: https://docs.sumsub.com/reference/request-applicant-check )
    
    - Verify applicant verification status (See this: https://docs.sumsub.com/reference/get-applicant-verification-steps-status)


    - Setup Webhook : This will help you get verification results (See this: https://docs.sumsub.com/docs/webhooks)



