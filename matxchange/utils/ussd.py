import frappe


@frappe.whitelist(allow_guest=True)
def handler(**kwargs):
    session_id = frappe.form_dict.get("sessionId", "")
    phone_number = frappe.form_dict.get("phoneNumber", "")
    text = frappe.form_dict.get("text", "")
    phone = format_phone(phone_number)
    parts = text.split("*") if text else []
    level = len(parts) if text else 0
    result = build_response(session_id, phone, parts, level)
    frappe.local.response["type"] = "txt"
    frappe.local.response["message"] = result
    return result


def format_phone(phone):
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    return phone


def build_response(session_id, phone, parts, level):
    if level == 0:
        return "CON Welcome to MatXchange\n1. My Earnings\n2. Record Waste\n3. Request Payment\n4. My Transactions\n5. My Profile"
    choice = parts[0] if parts else ""
    if choice == "1":
        return get_earnings(phone)
    elif choice == "2":
        if level == 1:
            return "CON Select Waste Category\n1. Plastic PET\n2. Plastic HDPE\n3. E-Waste\n4. Cardboard\n5. Metal Scrap"
        elif level == 2:
            return "CON Enter weight in KG:"
        elif level == 3:
            return record_waste(phone, parts[1], parts[2])
    elif choice == "3":
        return request_payment(phone)
    elif choice == "4":
        return get_transactions(phone)
    elif choice == "5":
        return get_profile(phone)
    return "END Invalid option."


def get_earnings(phone):
    try:
        picker = frappe.db.get_value(
            "Picker Profile",
            {"phone_number": ["like", "%" + phone[-9:] + "%"]},
            ["name", "first_name", "total_earnings"],
            as_dict=True
        )
        if picker:
            return "END Hello " + picker.first_name + "\nTotal Earnings: KES " + str(picker.total_earnings or 0)
        return "END Profile not found."
    except Exception:
        return "END Error fetching earnings."


def record_waste(phone, category_choice, weight):
    categories = {"1": "Plastic PET", "2": "Plastic HDPE", "3": "E-Waste", "4": "Cardboard", "5": "Metal Scrap"}
    category = categories.get(category_choice, "Unknown")
    return "END Waste recorded!\nCategory: " + category + "\nWeight: " + weight + " KG\nPayment coming shortly."


def request_payment(phone):
    try:
        picker = frappe.db.get_value(
            "Picker Profile",
            {"phone_number": ["like", "%" + phone[-9:] + "%"]},
            ["name", "first_name"],
            as_dict=True
        )
        if picker:
            return "END Payment request submitted.\nYou will receive M-Pesa shortly."
        return "END Profile not found."
    except Exception:
        return "END Error processing."


def get_transactions(phone):
    try:
        txns = frappe.get_all(
            "Waste Transaction",
            filters={"docstatus": 1},
            fields=["name", "total_amount_kes", "payment_status"],
            limit=3,
            order_by="creation desc"
        )
        if txns:
            msg = "END Last Transactions:\n"
            for t in txns:
                msg += t.name + ": KES " + str(t.total_amount_kes) + " - " + t.payment_status + "\n"
            return msg.strip()
        return "END No transactions found."
    except Exception:
        return "END Error fetching."


def get_profile(phone):
    try:
        picker = frappe.db.get_value(
            "Picker Profile",
            {"phone_number": ["like", "%" + phone[-9:] + "%"]},
            ["name", "first_name", "last_name", "phone_number"],
            as_dict=True
        )
        if picker:
            return "END Profile\nName: " + picker.first_name + " " + picker.last_name + "\nPhone: " + picker.phone_number
        return "END Profile not found."
    except Exception:
        return "END Error fetching."
