// Copyright (c) 2026, samogera and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Waste Transaction", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Waste Transaction', {

    refresh: function(frm) {
        // Show payment status badge
        if (frm.doc.payment_status === 'Paid') {
            frm.dashboard.set_headline_alert(
                '<span class="indicator green">Payment Confirmed</span>'
            );
        } else if (frm.doc.payment_status === 'Pending') {
            frm.dashboard.set_headline_alert(
                '<span class="indicator orange">Payment Pending</span>'
            );
        } else if (frm.doc.payment_status === 'Failed') {
            frm.dashboard.set_headline_alert(
                '<span class="indicator red">Payment Failed</span>'
            );
        }

        // Add confirm payment button for submitted transactions
        if (frm.doc.docstatus === 1 && frm.doc.payment_status === 'Pending') {
            frm.add_custom_button('Confirm Payment', function() {
                frappe.confirm(
                    `Confirm that KES ${frm.doc.total_amount_kes} was received by picker?`,
                    function() {
                        frappe.call({
                            method: 'matxchange.utils.payment_utils.confirm_payment',
                            args: { transaction_name: frm.doc.name },
                            callback: function(r) {
                                if (!r.exc) {
                                    frm.reload_doc();
                                    frappe.show_alert('Payment confirmed!', 5);
                                }
                            }
                        });
                    }
                );
            }, 'Actions');

            frm.add_custom_button('Mark as Failed', function() {
                frappe.call({
                    method: 'matxchange.utils.payment_utils.mark_payment_failed',
                    args: { transaction_name: frm.doc.name },
                    callback: function(r) {
                        if (!r.exc) {
                            frm.reload_doc();
                        }
                    }
                });
            }, 'Actions');
        }

        // Add retry payment button if failed
        if (frm.doc.docstatus === 1 && frm.doc.payment_status === 'Failed') {
            frm.add_custom_button('Retry Payment', function() {
                frappe.call({
                    method: 'matxchange.utils.payment_utils.retry_payment',
                    args: { transaction_name: frm.doc.name },
                    callback: function(r) {
                        if (!r.exc) {
                            frm.reload_doc();
                            frappe.show_alert('Payment retry initiated!', 5);
                        }
                    }
                });
            }, 'Actions');
        }
    },

    picker: function(frm) {
        if (frm.doc.picker) {
            frappe.db.get_value('Picker Profile', frm.doc.picker, 
                ['full_name', 'phone_number', 'mpesa_number', 'preferred_payment_method'],
                function(value) {
                    if (value) {
                        frm.set_value('payment_method', value.preferred_payment_method);
                        frm.set_df_property('picker', 'description', 
                            `Phone: ${value.phone_number}`);
                    }
                }
            );
        }
    },

    waste_category: function(frm) {
        if (frm.doc.waste_category) {
            frappe.db.get_value('Waste Category', frm.doc.waste_category, 
                'base_price_per_kg',
                function(value) {
                    if (value && value.base_price_per_kg) {
                        frm.set_value('unit_price_kes', value.base_price_per_kg);
                    }
                }
            );
        }
    },

    quantity_kg: function(frm) {
        calculate_total(frm);
    },

    unit_price_kes: function(frm) {
        calculate_total(frm);
    }
});

function calculate_total(frm) {
    if (frm.doc.quantity_kg && frm.doc.unit_price_kes) {
        let total = frm.doc.quantity_kg * frm.doc.unit_price_kes;
        frm.set_value('total_amount_kes', total);
    }
}