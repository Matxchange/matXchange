import frappe


@frappe.whitelist()
def confirm_payment(transaction_name):
    frappe.db.set_value("Waste Transaction", transaction_name, "payment_status", "Paid")
    frappe.db.set_value("Waste Transaction", transaction_name, "payment_date", frappe.utils.today())
    frappe.msgprint("Payment confirmed successfully")


@frappe.whitelist()
def mark_payment_failed(transaction_name):
    frappe.db.set_value("Waste Transaction", transaction_name, "payment_status", "Failed")
    frappe.msgprint("Payment marked as failed")


@frappe.whitelist()
def retry_payment(transaction_name):
    doc = frappe.get_doc("Waste Transaction", transaction_name)
    doc.trigger_payment()
    frappe.msgprint("Payment retry initiated")

