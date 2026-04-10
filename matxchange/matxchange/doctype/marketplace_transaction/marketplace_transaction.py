import frappe
from frappe.model.document import Document


class MarketplaceTransaction(Document):

    def validate(self):
        if self.listing:
            self.validate_quantity()
            self.calculate_total()

    def validate_quantity(self):
        listing = frappe.get_doc("Marketplace Listing", self.listing)
        if not listing:
            return
        if self.quantity_kg and self.quantity_kg > listing.quantity_available_kg:
            frappe.throw(
                f"Requested {self.quantity_kg} KG exceeds available {listing.quantity_available_kg} KG"
            )
        if listing.minimum_order_kg and self.quantity_kg and self.quantity_kg < listing.minimum_order_kg:
            frappe.throw(f"Minimum order is {listing.minimum_order_kg} KG")

    def calculate_total(self):
        if self.listing and self.quantity_kg:
            listing = frappe.get_doc("Marketplace Listing", self.listing)
            if listing and listing.price_per_kg_kes:
                self.total_amount_kes = self.quantity_kg * listing.price_per_kg_kes

    def on_submit(self):
        listing = frappe.get_doc("Marketplace Listing", self.listing)
        listing.update_quantity(self.quantity_kg)
        self.write_to_stellar()

    def write_to_stellar(self):
        try:
            from matxchange.utils.stellar import write_transaction
            data = {
                "transaction_id": self.name,
                "listing": self.listing,
                "buyer": self.buyer_name,
                "quantity_kg": self.quantity_kg,
                "total_amount_kes": self.total_amount_kes
            }
            stellar_hash = write_transaction(data)
            if stellar_hash:
                self.db_set("stellar_hash", stellar_hash)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Marketplace Stellar Error")