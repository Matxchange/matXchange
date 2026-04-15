import frappe

no_cache = 1

def get_context(context):
    session_id = frappe.form_dict.get("sessionId", "")
    phone_number = frappe.form_dict.get("phoneNumber", "")
    text = frappe.form_dict.get("text", "")
    from matxchange.utils.ussd import format_phone, build_response
    phone = format_phone(phone_number)
    parts = text.split("*") if text else []
    level = len(parts) if text else 0
    result = build_response(session_id, phone, parts, level)
    frappe.local.response["content_type"] = "text/plain; charset=utf-8"
    frappe.local.response["type"] = "txt"
    frappe.local.response["message"] = result
    context.result = result
