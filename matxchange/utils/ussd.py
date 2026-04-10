import frappe


@frappe.whitelist(allow_guest=True)
def handler(**kwargs):
    session_id = frappe.form_dict.get("sessionId", "")
    phone_number = frappe.form_dict.get("phoneNumber", "")
    text = frappe.form_dict.get("text", "")

    phone = format_phone(phone_number)
    parts = text.split("*") if text else []
    level = len(parts) if text else 0

    response = build_response(session_id, phone, parts, level)

    frappe.response["type"] = "text"
    frappe.response["http_status_code"] = 200
    frappe.local.response_headers = {"Content-Type": "text/plain"}
    return response


def build_response(session_id, phone, parts, level):
    if level == 0:
        return (
            "CON Welcome to MatXchange\n"
            "1. My Earnings\n"
            "2. Record Waste\n"
            "3. Request Payment\n"
            "4. My Transactions\n"
            "5. My Profile"
        )

    choice = parts[0] if parts else ""

    if choice == "1":
        picker = get_picker_by_phone(phone)
        if not picker:
            return "END Not registered on MatXchange. Contact your collector."

        earnings = frappe.db.sql(
            "SELECT COALESCE(SUM(total_amount_kes), 0) as total, COUNT(*) as transactions "
            "FROM `tabWaste Transaction` WHERE picker = %s AND docstatus = 1",
            picker.name, as_dict=True
        )[0]

        pending = frappe.db.sql(
            "SELECT COALESCE(SUM(total_amount_kes), 0) as pending "
            "FROM `tabWaste Transaction` "
            "WHERE picker = %s AND payment_status = 'Pending' AND docstatus = 1",
            picker.name, as_dict=True
        )[0]

        return (
            f"END MatXchange Earnings\n"
            f"Name: {picker.full_name}\n"
            f"Total Earned: KES {earnings.total}\n"
            f"Transactions: {earnings.transactions}\n"
            f"Pending: KES {pending.pending}"
        )

    if choice == "2":
        picker = get_picker_by_phone(phone)
        if not picker:
            return "END Not registered on MatXchange."

        if level == 1:
            categories = frappe.get_all(
                "Waste Category",
                fields=["name"],
                filters={"active": 1},
                limit=6
            )
            response = "CON Select Waste Category:\n"
            for i, cat in enumerate(categories, 1):
                response += f"{i}. {cat.name}\n"
            return response

        if level == 2:
            categories = frappe.get_all(
                "Waste Category",
                fields=["name", "base_price_per_kg"],
                filters={"active": 1},
                limit=6
            )
            try:
                cat_index = int(parts[1]) - 1
                if cat_index < 0 or cat_index >= len(categories):
                    return "END Invalid selection."
                frappe.cache().set_value(
                    f"ussd_cat_{session_id}",
                    categories[cat_index].name,
                    expires_in_sec=300
                )
                return f"CON Enter quantity in KG\nCategory: {categories[cat_index].name}:"
            except Exception:
                return "END Invalid selection."

        if level == 3:
            try:
                quantity = float(parts[2])
                cat_name = frappe.cache().get_value(f"ussd_cat_{session_id}")
                if not cat_name:
                    return "END Session expired. Please try again."
                cat = frappe.get_doc("Waste Category", cat_name)
                total = quantity * (cat.base_price_per_kg or 0)
                return (
                    f"CON Confirm:\n"
                    f"Category: {cat_name}\n"
                    f"Qty: {quantity} KG\n"
                    f"Amount: KES {total}\n"
                    f"1. Confirm\n"
                    f"2. Cancel"
                )
            except Exception:
                return "END Invalid quantity. Enter a number."

        if level == 4:
            picker = get_picker_by_phone(phone)
            if parts[3] == "1":
                try:
                    quantity = float(parts[2])
                    cat_name = frappe.cache().get_value(f"ussd_cat_{session_id}")
                    cat = frappe.get_doc("Waste Category", cat_name)
                    collector = frappe.db.get_value(
                        "Picker Profile", picker.name, "assigned_collector"
                    )
                    if not collector:
                        return "END No collector assigned. Contact support."
                    waste_doc = frappe.get_doc({
                        "doctype": "Waste Transaction",
                        "picker": picker.name,
                        "collector": collector,
                        "waste_category": cat_name,
                        "quantity_kg": quantity,
                        "unit_price_kes": cat.base_price_per_kg or 0,
                        "total_amount_kes": quantity * (cat.base_price_per_kg or 0),
                        "payment_method": picker.preferred_payment_method or "M-Pesa",
                        "payment_status": "Pending"
                    })
                    waste_doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                    return (
                        f"END Waste recorded!\n"
                        f"Ref: {waste_doc.name}\n"
                        f"Amount: KES {waste_doc.total_amount_kes}\n"
                        f"Payment coming shortly."
                    )
                except Exception as e:
                    frappe.log_error(frappe.get_traceback(), "USSD Waste Error")
                    return "END Error. Please try again."
            else:
                return "END Cancelled."

    if choice == "3":
        picker = get_picker_by_phone(phone)
        if not picker:
            return "END Not registered on MatXchange."

        pending = frappe.db.sql(
            "SELECT COALESCE(SUM(total_amount_kes), 0) as amount, COUNT(*) as count "
            "FROM `tabWaste Transaction` "
            "WHERE picker = %s AND payment_status = 'Pending' AND docstatus = 1",
            picker.name, as_dict=True
        )[0]

        if pending.count == 0:
            return "END No pending payments. All up to date."

        return (
            f"END Pending Payments:\n"
            f"Count: {pending.count}\n"
            f"Total: KES {pending.amount}\n"
            f"Processed automatically."
        )

    if choice == "4":
        picker = get_picker_by_phone(phone)
        if not picker:
            return "END Not registered on MatXchange."

        transactions = frappe.db.sql(
            "SELECT name, total_amount_kes, payment_status "
            "FROM `tabWaste Transaction` "
            "WHERE picker = %s AND docstatus = 1 "
            "ORDER BY creation DESC LIMIT 3",
            picker.name, as_dict=True
        )

        if not transactions:
            return "END No transactions found."

        response = "END Last 3 Transactions:\n"
        for t in transactions:
            status = "Paid" if t.payment_status == "Paid" else "Pending"
            response += f"{t.name[-8:]}: KES {t.total_amount_kes} {status}\n"
        return response

    if choice == "5":
        picker = get_picker_by_phone(phone)
        if not picker:
            return "END Not registered on MatXchange."

        return (
            f"END My Profile:\n"
            f"Name: {picker.full_name}\n"
            f"ID: {picker.name}\n"
            f"Phone: {picker.phone_number}\n"
            f"County: {picker.county or 'N/A'}"
        )

    return "END Invalid option. Please try again."


def format_phone(phone):
    if not phone:
        return ""
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    return "+" + phone


def get_picker_by_phone(phone):
    formatted = format_phone(phone)
    result = frappe.db.get_value(
        "Picker Profile",
        {"phone_number": ["in", [phone, formatted]]},
        ["name", "full_name", "phone_number", "county",
         "status", "preferred_payment_method", "assigned_collector"],
        as_dict=True
    )
    return result
