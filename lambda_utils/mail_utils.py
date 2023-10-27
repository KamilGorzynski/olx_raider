import os
import boto3

from lambda_utils.const import SOURCE_EMAIL


def _get_offers_list_items(offers):
    result = ""
    for offer in offers:
        result += f"<li>{offer}</li><br/>"
    return result


def _get_email_html_body(count, offers):
    return f"""
      <html>
        <head></head>
        <body>
          <h2>Nowe oferty!</h2>
          <br/>
          <p>Liczba ofert: { count }</p>
          { _get_offers_list_items(offers) }
        </body>
      </html>
    """


def _get_email_message(count, offers):
    return {
        "Body": {
            "Html": {
                "Charset": "utf-8",
                "Data": _get_email_html_body(count, offers),
            },
        },
        "Subject": {
            "Charset": "utf-8",
            "Data": "Oferty z OLX",
        },
    }


def send_email(count, offers):
    client = boto3.client("ses")
    if not (source_email := SOURCE_EMAIL):
        raise Exception("Source email not provided")
    client.send_email(
        Destination={
            "ToAddresses": os.environ.get("TO_ADDRESSES", "").split(","),
        },
        Message=_get_email_message(count, offers),
        Source=source_email,
        ConfigurationSetName="olx_raider_config_set",
    )
