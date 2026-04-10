frappe.ui.form.on('Picker Profile', {

    refresh: function(frm) {
        if (!frm.is_new()) {
            // Show total earnings
            frappe.call({
                method: 'matxchange.matxchange.doctype.picker_profile.picker_profile.get_picker_stats',
                args: { picker: frm.doc.name },
                callback: function(r) {
                    if (r.message) {
                        frm.dashboard.add_indicator(
                            `Total Earnings: KES ${r.message.total_earnings}`,
                            'green'
                        );
                        frm.dashboard.add_indicator(
                            `Total Waste: ${r.message.total_waste_kg} KG`,
                            'blue'
                        );
                        frm.dashboard.add_indicator(
                            `Transactions: ${r.message.total_transactions}`,
                            'orange'
                        );
                    }
                }
            });

            // Add Pay All Pending button
            frm.add_custom_button('View Transactions', function() {
                frappe.set_route('List', 'Waste Transaction', {
                    picker: frm.doc.name
                });
            });
        }

        // Show status indicator
        if (frm.doc.status === 'Active') {
            frm.dashboard.set_headline_alert(
                '<span class="indicator green">Active Picker</span>'
            );
        } else if (frm.doc.status === 'Suspended') {
            frm.dashboard.set_headline_alert(
                '<span class="indicator red">Suspended</span>'
            );
        }
    },

    preferred_payment_method: function(frm) {
        if (frm.doc.preferred_payment_method === 'M-Pesa') {
            frm.set_df_property('mpesa_number', 'reqd', 1);
            frm.set_df_property('airtel_money_number', 'reqd', 0);
        } else if (frm.doc.preferred_payment_method === 'Airtel Money') {
            frm.set_df_property('airtel_money_number', 'reqd', 1);
            frm.set_df_property('mpesa_number', 'reqd', 0);
        }
    }
});