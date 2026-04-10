import frappe
from frappe.model.document import Document


class CollectorProfile(Document):

    def before_save(self):
        self.set_collector_id()
        self.validate_phone()

    def set_collector_id(self):
        if not self.collector_id and self.name:
            self.collector_id = self.name

    def validate_phone(self):
        if self.phone_number:
            phone = str(self.phone_number).strip().replace(" ", "")
            if phone.startswith("0") and len(phone) == 10:
                self.phone_number = "+254" + phone[1:]

    def on_submit(self):
        self.status = "Active"
        self.db_set("status", "Active")

    def on_cancel(self):
        self.status = "Inactive"
        self.db_set("status", "Inactive")

    def get_total_pickers(self):
        return frappe.db.count("Picker Profile", {"assigned_collector": self.name})

    def get_total_waste_collected(self):
        result = frappe.db.sql("""
            SELECT COALESCE(SUM(quantity_kg), 0)
            FROM `tabWaste Transaction`
            WHERE collector = %s AND docstatus = 1
        """, self.name)
        return result[0][0] or 0