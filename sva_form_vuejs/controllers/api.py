import frappe

@frappe.whitelist(allow_guest=True)
def get_meta(doctype):
    return frappe.get_meta(doctype)

@frappe.whitelist(allow_guest=True)
def get_option(filters):
    return frappe.get_all('Field Options',filters=filters, fields=['name', 'label', 'code as level' ,"*"] , order_by='code')

@frappe.whitelist(allow_guest=True)
def get_option_with_dt(dt,filters=[]):
    meta = frappe.get_meta(dt).as_dict()
    return frappe.get_all(dt,filters=filters, fields=['name', f"{meta['title_field']} as label"])