import frappe
from frappe.model.document import Document


class ImpactRecord(Document):

    def validate(self):
        self.calculate_trees_equivalent()
        self.write_to_stellar()

    def calculate_trees_equivalent(self):
        if self.carbon_saved_kg:
            self.trees_equivalent = self.carbon_saved_kg / 21.77

    def write_to_stellar(self):
        if self.docstatus == 1:
            try:
                from matxchange.utils.stellar import write_transaction
                data = {
                    "impact_id": self.name,
                    "period": self.period,
                    "total_waste_kg": self.total_waste_kg,
                    "carbon_saved_kg": self.carbon_saved_kg,
                    "trees_equivalent": self.trees_equivalent
                }
                stellar_hash = write_transaction(data)
                if stellar_hash:
                    self.db_set("stellar_hash", stellar_hash)
            except Exception as e:
                frappe.log_error(frappe.get_traceback(), "Impact Record Stellar Error")