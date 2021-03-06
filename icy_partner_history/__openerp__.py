{ "name"         : "ICY Parnter History"
, "version"      : "1.0"
, "author"       : "Smart Solution (wim.audenaert@smartsolution.be)"
, "website"      : "http://www.smartsolution.be"
, "description"  : """Shows all customer related history data (sale orders, shipments, invoices, phone calls, meetings)"""
, "category"     : "Sale"
, "depends"      : ["sale","stock","account","purchase"]
, "init_xml"     : []
, "demo_xml"     : []
, "update_xml"   : 
    [ "icy_partner_history_view.xml"
    , "security/ir.model.access.csv"
    ]
, "auto_install" : False
, "installable"  : True
}
