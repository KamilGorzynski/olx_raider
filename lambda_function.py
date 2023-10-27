from lambda_utils.const import IS_LOCAL
from lambda_utils.bs_utils import get_offers
from lambda_utils.mail_utils import send_email


def lambda_handler(event, context):
    o_count, offers = get_offers()
    if IS_LOCAL:
        print(o_count, offers)
    else:
        send_email(o_count, offers)
        return {"statusCode": 200, "body": "Email with offers has been sent!"}


if IS_LOCAL:
    lambda_handler("event", "context")
