frappe.ui.form.on('Marketplace Transaction', {

    setup: function(frm) {
        // runs before refresh
    },

    refresh: function(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.total_amount_kes) {
            frm.dashboard.set_headline_alert(
                '<span class="indicator green">Total: KES ' + frm.doc.total_amount_kes + '</span>'
            );
        }
    },

    listing: function(frm) {
        if (frm.doc.listing) {
            frappe.db.get_value('Marketplace Listing', frm.doc.listing,
                ['price_per_kg_kes', 'quantity_available_kg'],
                function(value) {
                    if (value && frm.doc.quantity_kg) {
                        frm.set_value('total_amount_kes',
                            frm.doc.quantity_kg * value.price_per_kg_kes
                        );
                    }
                }
            );
        }
    },

    quantity_kg: function(frm) {
        if (frm.doc.listing && frm.doc.quantity_kg) {
            frappe.db.get_value('Marketplace Listing', frm.doc.listing,
                'price_per_kg_kes',
                function(value) {
                    if (value && value.price_per_kg_kes) {
                        frm.set_value('total_amount_kes',
                            frm.doc.quantity_kg * value.price_per_kg_kes
                        );
                    }
                }
            );
        }
    }
});