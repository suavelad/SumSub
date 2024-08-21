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
    - Create  Applicant
    - Applicant upload document
    - Alert Sumsub to start the verification (request applicant check)
    - Verify applicant verification status 