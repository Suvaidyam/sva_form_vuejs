import frappe
import json

@frappe.whitelist(allow_guest=True)
def get_meta(doctype):
    return frappe.get_meta(doctype)

@frappe.whitelist(allow_guest=True)
def get_option(filters):
    return frappe.get_all('Field Options',filters=filters, fields=['name', 'label', 'code as level' , 'score','group','depends_on'] , order_by='code asc')

@frappe.whitelist(allow_guest=True)
def get_criteria(filters):
    ids = frappe.get_list('Number field Scoring Logic',filters=filters,order_by="creation desc", pluck='name',ignore_permissions=True)
    if not ids:
        return {}
    return frappe.get_doc('Number field Scoring Logic',ids[0])

@frappe.whitelist(allow_guest=True)
def get_option_with_dt(dt,filters=[]):
    meta = frappe.get_meta(dt).as_dict()
    if meta['title_field']:
        return frappe.get_all(dt,filters=filters, fields=['name', f"{meta['title_field']} as label"])
    else:
        return frappe.get_all(dt,filters=filters, fields=['name', 'name as label'])
    

@frappe.whitelist(allow_guest=True)
def get_fields(fieldtype):
    if isinstance(fieldtype, str):
        fieldtype = json.loads(fieldtype)
    fields = frappe.get_all(
        'DocField',
        filters={
            'parent': 'Assessment',
            'fieldtype': ['in', fieldtype]
        },
        fields=['fieldname', 'label']
    )
    return fields

@frappe.whitelist(allow_guest=True)
def add_criteria(data):
    data = json.loads(data)
    fields = get_fields(['Int', 'Float','Percent'])
    filter_field = [field for field in fields if field.get('label') == data['field']][0]
    # return filter_field.get('fieldname')
    data['field'] = filter_field.get('fieldname')
    ids = frappe.get_list('Number field Scoring Logic',filters={'name':filter_field.get('fieldname')},order_by="creation desc", pluck='name',ignore_permissions=True)
    if data and filter_field:
        if ids:
            new_doc = frappe.get_doc('Number field Scoring Logic',ids[0])
            new_doc.ref_doc = data.get('ref_doc')
            new_doc.field = data.get('field')
            new_doc.min = data.get('min')
            new_doc.max = data.get('max')
            new_doc.criteria = []
            if data.get('criteria') and len(data.get('criteria')):
                for item in data.get('criteria'):
                    new_doc.append('criteria', item)
            new_doc.save(ignore_permissions=True
            )
            return frappe.msgprint('Criteria added successfully')
        else:
            new_doc = frappe.new_doc('Number field Scoring Logic')
            new_doc.update(data)
            new_doc.save(ignore_permissions=True)
            return frappe.msgprint('Criteria added successfully')
    

@frappe.whitelist()
def get_min_max_criteria(filters):
    data= frappe.get_doc('Number field Scoring Logic',filters)
    if data.max == 0:
        return {'min':data.min}
    else:
        return {'min':data.min,'max':data.max}