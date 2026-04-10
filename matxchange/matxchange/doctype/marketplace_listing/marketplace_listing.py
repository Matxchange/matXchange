import frappe
from frappe.model.document import Document
from frappe.utils import today


class MarketplaceListing(Document):

    def validate(self):
        self.validate_quantity()
        self.set_listing_date()
        self.check_expiry()

    def validate_quantity(self):
        if self.quantity_available_kg <= 0:
            frappe.throw("Quantity must be greater than zero")
        if self.minimum_order_kg and self.minimum_order_kg > self.quantity_available_kg:
            frappe.throw("Minimum order cannot exceed available quantity")

    def set_listing_date(self):
        if not self.listing_date:
            self.listing_date = today()

    def check_expiry(self):
        if self.expiry_date and self.expiry_date < today():
            self.status = "Expired"

    def on_submit(self):
        self.status = "Active"
        self.db_set("status", "Active")

    def on_cancel(self):
        self.status = "Expired"
        self.db_set("status", "Expired")

    def update_quantity(self, sold_quantity):
        new_quantity = self.quantity_available_kg - sold_quantity
        if new_quantity <= 0:
            self.db_set("status", "Sold")
            self.db_set("quantity_available_kg", 0)
        else:
            self.db_set("quantity_available_kg", new_quantity)