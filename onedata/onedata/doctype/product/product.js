frappe.ui.form.on('Product', {
    refresh: function(frm) {
        // Only show Fetch button if document is new (not saved)
        if (frm.is_new()) {
            frm.add_custom_button(__('Fetch'), function() {
                if (!frm.doc.product_id) {
                    frappe.throw(__('Please enter Product ID first'));
                    return;
                }
                
                // Call the fetch method
                frm.call({
                    doc: frm.doc,
                    method: 'fetch_from_api',
                    freeze: true,
                    freeze_message: __('Fetching Product Data...'),
                    callback: function(r) {
                        if (r.message && r.message.status === 'success') {
                            // Update the form with new data
                            frm.doc.product_name = r.message.data.product_name;
                            frm.doc.product_data = r.message.data.product_data;
                            
                            // Refresh the form to show new data
                            frm.refresh();
                            
                            frappe.show_alert({
                                message: __('Product data fetched successfully'),
                                indicator: 'green'
                            });
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    },
    
    // Optional: Clear data when product_id is changed
    product_id: function(frm) {
        if (frm.is_new()) {  // Only clear if document is new
            // Clear existing data when product ID is changed
            frm.doc.product_name = "";
            frm.doc.product_data = [];
            frm.refresh();
        }
    }
});