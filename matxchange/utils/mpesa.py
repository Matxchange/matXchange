import frappe
import requests
import base64
import uuid


def get_access_token():
    consumer_key = frappe.conf.get("mpesa_consumer_key", "")
    consumer_secret = frappe.conf.get("mpesa_consumer_secret", "")
    environment = frappe.conf.get("mpesa_environment", "sandbox")

    if environment == "sandbox":
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    else:
        url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    response = requests.get(url, headers={"Authorization": f"Basic {auth}"})
    return response.json().get("access_token")


def format_phone_number(phone):
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    return phone


def send_b2c_payment(phone_number, amount, reference, remarks="MatXchange Payment"):
    try:
        environment = frappe.conf.get("mpesa_environment", "sandbox")
        initiator_name = frappe.conf.get("mpesa_initiator_name", "testapi")
        initiator_password = frappe.conf.get("mpesa_initiator_password", "Safaricom999!*!")
        shortcode = frappe.conf.get("mpesa_shortcode", "600998")

        access_token = get_access_token()
        if not access_token:
            return {"success": False, "error": "Could not get M-Pesa access token"}

        if environment == "sandbox":
            url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest"
            result_url = "https://webhook.site/matxchange-result"
            timeout_url = "https://webhook.site/matxchange-timeout"
        else:
            url = "https://api.safaricom.co.ke/mpesa/b2c/v3/paymentrequest"
            result_url = frappe.utils.get_url("/api/method/matxchange.utils.mpesa.b2c_result")
            timeout_url = frappe.utils.get_url("/api/method/matxchange.utils.mpesa.b2c_timeout")

        phone = format_phone_number(phone_number)

        payload = {
            "OriginatorConversationID": str(uuid.uuid4()),
            "InitiatorName": initiator_name,
            "SecurityCredential": initiator_password,
            "CommandID": "BusinessPayment",
            "Amount": int(amount),
            "PartyA": shortcode,
            "PartyB": phone,
            "Remarks": remarks,
            "QueueTimeOutURL": timeout_url,
            "ResultURL": result_url,
            "Occassion": reference
        }

        response = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )

        result = response.json()

        if result.get("ResponseCode") == "0":
            return {
                "success": True,
                "conversation_id": result.get("ConversationID"),
                "originator_id": result.get("OriginatorConversationID")
            }
        else:
            error_msg = result.get("ResponseDescription") or result.get("errorMessage") or str(result)
            return {
                "success": False,
                "error": error_msg
            }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "M-Pesa B2C Error")
        return {"success": False, "error": str(e)}


@frappe.whitelist(allow_guest=True)
def b2c_result(**kwargs):
    try:
        data = frappe.request.get_json()
        result = data.get("Result", {})
        conversation_id = result.get("ConversationID")
        result_code = result.get("ResultCode")

        if conversation_id:
            transaction = frappe.db.get_value(
                "Waste Transaction",
                {"payment_reference": conversation_id},
                "name"
            )
            if transaction:
                if result_code == 0:
                    frappe.db.set_value("Waste Transaction", transaction, {
                        "payment_status": "Paid",
                        "payment_date": frappe.utils.today()
                    })
                else:
                    frappe.db.set_value("Waste Transaction", transaction, {
                        "payment_status": "Failed"
                    })
                frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "B2C Result Callback Error")


@frappe.whitelist(allow_guest=True)
def b2c_timeout(**kwargs):
    frappe.log_error("B2C payment timed out", "M-Pesa Timeout")
