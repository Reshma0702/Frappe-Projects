frappe.listview_settings['Lead'] = {
    onload: function (listview) {
        // Add a custom action for converting leads to customers
        listview.page.add_action_item(__("Convert Customer"), () => {
            erpnext.bulk_transaction_processing.create(listview, "Lead", "Customer");
        });
    }
};

// Provide the bulk transaction processing namespace
frappe.provide("erpnext.bulk_transaction_processing");

$.extend(erpnext.bulk_transaction_processing, {
    create: function(listview, from_doctype, to_doctype) {
        let checked_items = listview.get_checked_items();

        if (checked_items.length === 0) {
            frappe.msgprint(__('Please select at least one lead.'));
            return;
        }

        // Collect document names for processing
        const lead_names = checked_items.map(item => item.name);

        // Confirm the action
        frappe.confirm(
            __("Convert {0} Lead(s) to Customer(s)?", [lead_names.length]),
            () => {
                frappe.call({
                    method: "onedata.custom_onedata.bulk_actions.convert_leads_to_customers",
                    args: {
                        lead_names: lead_names
                    },
                    callback: function(response) {
                        frappe.msgprint(response.message);
                        listview.refresh(); // Refresh the list view after conversion
                    }
                });
            }
        );
    }
});
