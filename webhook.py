import hmac
import hashlib
from flask import Flask, request, jsonify
from  loguru import logger
from decouple import config


app = Flask(__name__)

SUMSUB_SECRET_KEY = config('SUMSUB_SECRET_KEY')





@app.route('v1/sumsub/webhook/', methods=['POST'])
def sumsub_webhook():

    #TODO: Make it a background task: 
    process_webhook(request)

    return jsonify({'status': ''}), 200
    


def verify_signature(x_payload_digest, x_payload_digest_alg, raw_body):
    
    # It will choose the HMAC algorithm based on the signature algorithm  set in the admin which will be returned in the x-payload-digest-alg header
    match x_payload_digest_alg:
        case 'HMAC-SHA256':
            digest = hmac.new(SUMSUB_SECRET_KEY.encode('utf-8'), raw_body, hashlib.sha256).hexdigest()
        
        case 'HMAC-SHA512':
            digest = hmac.new(SUMSUB_SECRET_KEY.encode('utf-8'), raw_body, hashlib.sha512).hexdigest()
        case _:
            logger.error(f"Unsupported HMAC algorithm: {x_payload_digest_alg}")
            return False

    # Compare the calculated digest with the x-payload-digest gotten from the header
    return hmac.compare_digest(digest, x_payload_digest)

def process_webhook(request):
    try:
        # Extract headers and raw body
        x_payload_digest = request.headers.get('x-payload-digest')
        x_payload_digest_alg = request.headers.get('x-payload-digest-alg')
        raw_body = request.get_data()

        # Verify the signature
        if not verify_signature(x_payload_digest, x_payload_digest_alg, raw_body):
            return False

        # Process the webhook
        data = request.json()
        event_type = data.get('type')
        payload = data.get('payload')

        # Handle different event types
        match event_type.lower():
            case 'applicantreviewed':
               return  handle_applicant_reviewed(payload)
            case 'applicantcreated':
                return handle_applicant_created(payload)
            case _:
                return False

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return False

def handle_applicant_reviewed(payload):
    # Process the applicantReviewed event
    # Sample Response: 
    #     {
    #         "applicantId": "5c9e177b0a975a6eeccf5960",
    #         "inspectionId": "5c9e177b0a975a6eeccf5961",
    #         "correlationId": "req-63f92830-4d68-4eee-98d5-875d53a12258",
    #         "levelName": "basic-kyc-level",
    #         "externalUserId": "12672",
    #         "type": "applicantCreated",
    #         "sandboxMode": "false",
    #         "reviewStatus": "init",
    #         "createdAtMs": "2020-02-21 13:23:19.002",
    #         "clientId": "coolClientId"
    #     }
    #TODO: Save to DB

    logger.info(f"Applicant reviewed: {payload}")
    return True

def handle_applicant_created(payload):
    # Process the applicantCreated event

    # Sample Success Response: 
        # {
        #     "applicantId": "5cb56e8e0a975a35f333cb83",
        #     "inspectionId": "5cb56e8e0a975a35f333cb84",
        #     "correlationId": "req-a260b669-4f14-4bb5-a4c5-ac0218acb9a4",
        #     "externalUserId": "externalUserId",
        #     "levelName": "basic-kyc-level",
        #     "type": "applicantReviewed",
        #     "reviewResult": {
        #         "reviewAnswer": "GREEN"
        #     },
        #     "reviewStatus": "completed",
        #     "createdAtMs": "2020-02-21 13:23:19.321"
        #     }

    # Sample Failed / Rejected Response: 
        # {
        #     "applicantId": "5cb744200a975a67ed1798a4",
        #     "inspectionId": "5cb744200a975a67ed1798a5",
        #     "correlationId": "req-fa94263f-0b23-42d7-9393-ab10b28ef42d",
        #     "externalUserId": "externalUserId",
        #     "levelName": "basic-kyc-level",
        #     "type": "applicantReviewed",
        #     "reviewResult": {
        #         "moderationComment": "We could not verify your profile. If you have any questions, please contact the Company where you try to verify your profile ${clientSupportEmail}",
        #         "clientComment": " Suspected fraudulent account.",
        #         "reviewAnswer": "RED",
        #         "rejectLabels": ["UNSATISFACTORY_PHOTOS", "GRAPHIC_EDITOR", "FORGERY"],
        #         "reviewRejectType": "FINAL"
        #     },
        #     "reviewStatus": "completed",
        #     "createdAtMs": "2020-02-21 13:23:19.001"
        #     }

    #TODO: Save to DB, verify the result

    logger.info(f"Applicant created: {payload}")
    return True


if __name__ == "__main__":
    app.run(port=5000, debug=True)
