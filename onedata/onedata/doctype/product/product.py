import frappe
import requests
from frappe import _
from frappe.model.document import Document

class Product(Document):
    @frappe.whitelist()
    def fetch_from_api(self):
        try:
            if not self.product_id:
                frappe.throw(_("Please enter Product ID first"))

            # Fetch data from the REST API
            api_url = f"https://api.restful-api.dev/objects/{self.product_id}"
            response = requests.get(api_url)
            response.raise_for_status()
            
            # Parse the JSON response
            product_data = response.json()
            
            # Set the basic fields
            self.product_name = product_data["name"]
            
            # Clear existing product data entries
            self.product_data = []
            
            # Add data key-value pairs to the child table
            if "data" in product_data and isinstance(product_data["data"], dict):
                for key, value in product_data["data"].items():
                    self.append("product_data", {
                        "key": key,
                        "value": str(value)
                    })
            
            return {
                "status": "success",
                "message": _("Product data fetched successfully")
            }
            
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"API Request Error: {str(e)}", _("Product Import Error"))
            frappe.throw(_("Failed to fetch product data from API"))
            
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), _("Product Import Error"))
            frappe.throw(_("Failed to process product data"))
    
    def get_data_value(self, key):
        """Get specific data value from product_data child table"""
        for d in self.product_data:
            if d.key == key:
                return d.value
        return None