import frappe

@frappe.whitelist()
def convert_leads_to_customers(lead_names):
   lead_names = frappe.parse_json(lead_names)
   converted_customers = []
   skipped = []

   for lead_name in lead_names:
       # Skip if customer already exists
       if frappe.db.exists("Customer", {"lead_name": lead_name}):
           skipped.append(lead_name)
           continue
           
       lead_doc = frappe.get_doc("Lead", lead_name)
       customer_doc = frappe.get_doc({
           "doctype": "Customer",
           "customer_name": lead_doc.lead_name,
           "lead_name": lead_doc.name,
           "customer_type": "Company",
           "territory": lead_doc.territory,
           "customer_group": "Individual",
           "territory": "India"
       })
       customer_doc.insert(ignore_permissions=True)
       converted_customers.append(customer_doc.name)

   return {
       "message": f"{len(converted_customers)} Lead(s) converted to Customer(s) successfully. {len(skipped)} skipped.",
       "customers": converted_customers,
       "skipped": skipped
   }