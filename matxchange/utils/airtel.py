import frappe


def send_airtel_payment(phone_number, amount, reference):
    # Airtel Money integration pending API approval
    frappe.log_error(
        f"Airtel payment attempted for {reference} - KES {amount} to {phone_number}. API pending approval.",
        "Airtel Money Pending"
    )
    return {
        "success": False,
        "error": "Airtel Money integration pending API approval. Please pay manually."
    }
