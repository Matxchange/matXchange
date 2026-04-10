import frappe
from frappe.model.document import Document


class PickerProfile(Document):

    def before_save(self):
        self.validate_phone_numbers()
        self.set_picker_id()

    def validate_phone_numbers(self):
        if self.phone_number:
            self.phone_number = self.format_phone(self.phone_number)
        if self.mpesa_number:
            self.mpesa_number = self.format_phone(self.mpesa_number)
        if self.airtel_money_number:
            self.airtel_money_number = self.format_phone(self.airtel_money_number)

    def format_phone(self, phone):
        phone = str(phone).strip().replace(" ", "").replace("-", "")
        if phone.startswith("0") and len(phone) == 10:
            phone = "+254" + phone[1:]
        elif phone.startswith("254") and len(phone) == 12:
            phone = "+" + phone
        return phone

    def set_picker_id(self):
        if not self.picker_id and self.name:
            self.picker_id = self.name

    def on_submit(self):
        self.status = "Active"
        self.db_set("status", "Active")

    def on_cancel(self):
        self.status = "Inactive"
        self.db_set("status", "Inactive")

    def get_total_earnings(self):
        result = frappe.db.sql("""
            SELECT COALESCE(SUM(total_amount_kes), 0)
            FROM `tabWaste Transaction`
            WHERE picker = %s
            AND payment_status = 'Paid'
            AND docstatus = 1
        """, self.name)
        return result[0][0] or 0

    def get_total_waste_collected(self):
        result = frappe.db.sql("""
            SELECT COALESCE(SUM(quantity_kg), 0)
            FROM `tabWaste Transaction`
            WHERE picker = %s
            AND docstatus = 1
        """, self.name)
        return result[0][0] or 0


@frappe.whitelist()
def get_picker_stats(picker):
    total_earnings = frappe.db.sql("""
        SELECT COALESCE(SUM(total_amount_kes), 0)
        FROM `tabWaste Transaction`
        WHERE picker = %s AND payment_status = 'Paid' AND docstatus = 1
    """, picker)[0][0]

    total_waste = frappe.db.sql("""
        SELECT COALESCE(SUM(quantity_kg), 0)
        FROM `tabWaste Transaction`
        WHERE picker = %s AND docstatus = 1
    """, picker)[0][0]

    total_transactions = frappe.db.count("Waste Transaction", {
        "picker": picker,
        "docstatus": 1
    })

    return {
        "total_earnings": total_earnings,
        "total_waste_kg": total_waste,
        "total_transactions": total_transactions
    }