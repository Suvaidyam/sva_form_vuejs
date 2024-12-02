import frappe

@frappe.whitelist(allow_guest=True)
def get_meta(doctype):
    return frappe.get_meta(doctype)

@frappe.whitelist(allow_guest=True)
def get_option(filters):
    return frappe.get_all('Field Options',filters=filters, fields=['name', 'label', 'code as level' , 'score'] , order_by='code asc')

@frappe.whitelist(allow_guest=True)
def get_option_with_dt(dt,filters=[]):
    meta = frappe.get_meta(dt).as_dict()
    if meta['title_field']:
        return frappe.get_all(dt,filters=filters, fields=['name', f"{meta['title_field']} as label"])
    else:
        return frappe.get_all(dt,filters=filters, fields=['name', 'name as label'])
    

@frappe.whitelist(allow_guest=True)
def get_fields():
    fieldtype= ['Table MultiSelect', 'Link']
    fields = frappe.get_all(
        'DocField',
        filters={
            'parent': 'Assessment',
            'fieldtype': ['in', fieldtype]
        },
        fields=['fieldname', 'label']
    )
    return fields
