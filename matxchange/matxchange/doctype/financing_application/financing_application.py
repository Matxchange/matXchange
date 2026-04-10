import frappe
from frappe.model.document import Document


class FinancingApplication(Document):

    def validate(self):
        self.validate_applicant()
        self.set_application_date()

    def validate_applicant(self):
        if self.applicant_type == "Picker" and not self.picker:
            frappe.throw("Please select a Picker")
        elif self.applicant_type == "Collector" and not self.collector:
            frappe.throw("Please select a Collector")
        elif self.applicant_type == "Recycler" and not self.recycler:
            frappe.throw("Please select a Recycler")

    def set_application_date(self):
        if not self.application_date:
            self.application_date = frappe.utils.today()

    def on_submit(self):
        self.status = "Submitted"
        self.db_set("status", "Submitted")
        self.notify_dfi()

    def notify_dfi(self):
        frappe.publish_realtime(
            "new_financing_application",
            {
                "application": self.name,
                "applicant": self.applicant_name,
                "amount": self.amount_requested_kes
            }
        )

    def approve(self, approved_amount, dfi_name):
        self.db_set("status", "Approved")
        self.db_set("approved_amount_kes", approved_amount)
        self.db_set("dfi_name", dfi_name)
        frappe.msgprint(f"Application approved for KES {approved_amount}")

    def reject(self, reason):
        self.db_set("status", "Rejected")
        self.db_set("notes", reason)
        frappe.msgprint("Application rejected")