import frappe

@frappe.whitelist(allow_guest=True)
def get_meta(doctype):
    return frappe.get_meta(doctype)