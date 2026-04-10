import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, flt


class WasteTransaction(Document):

    def validate(self):
        self.calculate_total()
        self.validate_payment_fields()
        self.set_transaction_date()

    def calculate_total(self):
        if self.quantity_kg and self.unit_price_kes:
            self.total_amount_kes = flt(self.quantity_kg) * flt(self.unit_price_kes)

    def validate_payment_fields(self):
        if not self.picker:
            return
        if self.payment_method == "M-Pesa":
            picker = frappe.get_doc("Picker Profile", self.picker)
            if not picker.mpesa_number:
                frappe.throw("Picker does not have an M-Pesa number. Please update their profile.")

    def set_transaction_date(self):
        if not self.transaction_date:
            self.transaction_date = frappe.utils.today()

    def on_submit(self):
        self.db_set("payment_status", "Pending")
        self.trigger_payment()
        self.write_to_stellar()

    def trigger_payment(self):
        if self.payment_method == "M-Pesa":
            self.trigger_mpesa_payment()
        elif self.payment_method == "Cash":
            self.handle_cash_payment()
        else:
            frappe.msgprint(
                f"{self.payment_method} payment of KES {self.total_amount_kes} — please process manually.",
                alert=True,
                indicator="orange"
            )

    def trigger_mpesa_payment(self):
        try:
            from matxchange.utils.mpesa import send_b2c_payment
            picker = frappe.get_doc("Picker Profile", self.picker)
            result = send_b2c_payment(
                phone_number=picker.mpesa_number,
                amount=self.total_amount_kes,
                reference=self.name,
                remarks=f"MatXchange payment for {self.name}"
            )
            if result.get("success"):
                frappe.db.set_value("Waste Transaction", self.name, {
                    "payment_reference": result.get("conversation_id"),
                    "payment_status": "Pending"
                })
                frappe.msgprint(
                    f"M-Pesa payment of KES {self.total_amount_kes} initiated to {picker.mpesa_number}",
                    indicator="green"
                )
            else:
                frappe.db.set_value("Waste Transaction", self.name, "payment_status", "Failed")
                frappe.msgprint(
                    f"M-Pesa failed: {result.get('error')}. Please pay manually.",
                    alert=True,
                    indicator="red"
                )
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "M-Pesa Payment Error")
            frappe.msgprint(f"Payment error: {str(e)}. Please pay manually.", alert=True)

    def handle_cash_payment(self):
        try:
            cash_payment = frappe.get_doc({
                "doctype": "Cash Payment",
                "payment_date": frappe.utils.today(),
                "amount_kes": self.total_amount_kes,
                "picker": self.picker,
                "waste_transaction": self.name,
                "received_by": frappe.session.user
            })
            cash_payment.insert(ignore_permissions=True)
            frappe.db.set_value("Waste Transaction", self.name, "payment_status", "Paid")
            frappe.msgprint(
                f"Cash payment of KES {self.total_amount_kes} recorded.",
                indicator="green"
            )
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Cash Payment Error")
            frappe.msgprint(f"Cash payment error: {str(e)}", alert=True)

    def write_to_stellar(self):
        try:
            from matxchange.utils.stellar import write_transaction
            data = {
                "transaction_id": self.name,
                "picker": self.picker,
                "collector": self.collector,
                "waste_category": self.waste_category,
                "quantity_kg": self.quantity_kg,
                "total_amount_kes": self.total_amount_kes,
                "timestamp": str(now_datetime())
            }
            stellar_hash = write_transaction(data)
            if stellar_hash:
                frappe.db.set_value("Waste Transaction", self.name, "stellar_hash", stellar_hash)
                frappe.msgprint(
                    f"Blockchain hash: {stellar_hash[:20]}...",
                    indicator="green"
                )
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Stellar Write Error")

    def on_cancel(self):
        frappe.db.set_value("Waste Transaction", self.name, "payment_status", "Cancelled")
