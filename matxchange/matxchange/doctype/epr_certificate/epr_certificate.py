import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today


class EPRCertificate(Document):

    def validate(self):
        self.check_dates()
        self.check_expiry_status()

    def check_dates(self):
        if self.issue_date and self.expiry_date:
            if str(self.expiry_date) <= str(self.issue_date):
                frappe.throw("Expiry date must be after issue date")

    def check_expiry_status(self):
        if self.expiry_date:
            days = date_diff(self.expiry_date, today())
            if days < 0:
                self.status = "Expired"
            elif days <= 30:
                frappe.msgprint(
                    f"This EPR Certificate expires in {days} days. Please renew soon.",
                    alert=True,
                    indicator="orange"
                )

    def on_submit(self):
        self.db_set("status", "Active")
        self.write_to_stellar()

    def write_to_stellar(self):
        try:
            from matxchange.utils.stellar import write_transaction
            data = {
                "certificate_id": self.name,
                "producer": self.producer,
                "waste_offset_kg": self.waste_offset_kg,
                "issue_date": str(self.issue_date),
                "expiry_date": str(self.expiry_date)
            }
            stellar_hash = write_transaction(data)
            if stellar_hash:
                self.db_set("stellar_hash", stellar_hash)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "EPR Stellar Error")

    def on_cancel(self):
        self.db_set("status", "Revoked")
