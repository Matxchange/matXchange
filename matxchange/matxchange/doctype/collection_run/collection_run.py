import frappe
from frappe.model.document import Document


class CollectionRun(Document):

    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        if not self.collector:
            return
        result = frappe.db.sql("""
            SELECT
                COUNT(*) as total_transactions,
                COALESCE(SUM(quantity_kg), 0) as total_weight,
                COALESCE(SUM(total_amount_kes), 0) as total_amount
            FROM `tabWaste Transaction`
            WHERE collector = %s
            AND docstatus = 1
        """, self.collector, as_dict=True)

        if result:
            self.total_transactions = result[0].total_transactions
            self.total_weight_kg = result[0].total_weight
            self.total_amount_kes = result[0].total_amount

    def on_submit(self):
        self.status = "Completed"
        self.db_set("status", "Completed")

    def on_cancel(self):
        self.status = "Cancelled"
        self.db_set("status", "Cancelled")