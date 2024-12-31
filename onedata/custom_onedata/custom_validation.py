import frappe
from frappe import _

def validate_lead_phone(doc, method):
    if doc.phone:
        # Check for country code (must start with +)
        if not doc.phone.startswith('+'):
            frappe.throw(_('Phone number must start with country code (e.g. +1)'))
            
        # Check length
        if len(doc.phone) > 15:
            frappe.throw(_('Phone number cannot exceed 15 characters'))