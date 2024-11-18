// Copyright (c) 2024, Rahul Sah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Field Options", {
    async refresh(frm) {
 
        //    console.log(frm, "frm");
        if (frm.doc.ref_doctype) {
            let data = await frappe.call({
                method: "sva_form_vuejs.controllers.api.get_meta",
                args: {
                    doctype: frm.doc.ref_doctype
                },
            })
            let options = data.message.fields?.filter(f=> ['Link','Table MultiSelect'].includes(f.fieldtype))?.map((field) => { return {value:field.fieldname, label:field.label }});
            frm.fields_dict.field.set_data(options); 
        }
 
 
    },
    ref_doctype: async function (frm) {
        if (frm.doc.ref_doctype) {
            let data = await frappe.call({
                method: "sva_form_vuejs.controllers.api.get_meta",
                args: {
                    doctype: frm.doc.ref_doctype
                },
            })
            let options = data.message.fields?.filter(f=> ['Link', 'Table MultiSelect'].includes(f.fieldtype))?.map((field) => { return {value:field.fieldname, label:field.label }});
            console.log("options",options);
            
            frm.fields_dict.field.set_data(options);
        }
    }
});