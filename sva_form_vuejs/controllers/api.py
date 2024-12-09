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
    return frappe.get_all('Number field Scoring Logic',filters=filters, fields=['name', 'min', 'max' , 'score','upper_limit','lower_limit','code'] , order_by='score asc')

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


@frappe.whitelist()
def update_many(dt,docs):
    try:
        docs_list = json.loads(docs)
        for doc in docs_list:
            updated_doc = frappe.get_doc(dt, doc['name'])
            updated_doc.update(doc)
            updated_doc.save(ignore_permissions=True)
        return {"status": "success", "message": "Updated successfully.", "data": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def delete_many(dt,docs):
    try:
        docs_list = json.loads(docs)
        for doc in docs_list:
            frappe.delete_doc(dt, doc['name'], ignore_permissions=True)
        return {"status": "success", "message": "Deleted successfully.", "data": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@frappe.whitelist()
def get_min_max_criteria(filters):
    data= frappe.get_all('Number field Scoring Logic',filters=filters, fields=['min', 'max','name'] , order_by='score asc')

    if data:
        minValue = data[0].min
        maxValue = data[0].max
        name = data[0].name
        if maxValue == 0:
            return {"min": minValue, "name": name}
        return {"min": minValue, "max": maxValue, "name": name}        