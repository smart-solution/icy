<html>
<head>
    <style type="text/css">
        ${css}

.list_invoice_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
.list_invoice_table th {
    background-color: #EEEEEE;
    border: thin solid #000000;
    text-align:center;
    font-size:12;
    font-weight:bold;
    padding-right:3px;
    padding-left:3px;
}
.list_invoice_table td {
    border-top : thin solid #EEEEEE;
    text-align:left;
    font-size:12;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_invoice_table thead {
    display:table-header-group;
}

.list_invoice_det_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
.list_invoice_det_table th {
    background-color: #EEEEEE;
    border: thin solid #000000;
    text-align:center;
    font-size:8;
    font-weight:bold;
    padding-right:3px;
    padding-left:3px;
}
.list_invoice_det_table td {
    border-top : thin solid #EEEEEE;
    text-align:left;
    font-size:8;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_invoice_det_table thead {
    display:table-header-group;
}

td.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
}


.list_bank_table {
    text-align:center;
    border-collapse: collapse;
}
.list_bank_table th {
    background-color: #EEEEEE;
    text-align:left;
    font-size:12;
    font-weight:bold;
    padding-right:3px;
    padding-left:3px;
}
.list_bank_table td {
    text-align:left;
    font-size:12;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}


.list_tax_table {
}
.list_tax_table td {
    text-align:left;
    font-size:12;
}
.list_tax_table th {
}
.list_tax_table thead {
    display:table-header-group;
}


.list_total_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
.list_total_table td {
    border-top : thin solid #EEEEEE;
    text-align:left;
    font-size:12;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_total_table th {
    background-color: #EEEEEE;
    border: thin solid #000000;
    text-align:center;
    font-size:12;
    font-weight:bold;
    padding-right:3px
    padding-left:3px
}
.list_total_table thead {
    display:table-header-group;
}


.no_bloc {
    border-top: thin solid  #ffffff ;
}

.right_table {
    right: 4cm;
    width:"100%";
}

.std_text {
    font-size:12;
}

tfoot.totals tr:first-child td{
    padding-top: 15px;
}

th.date {
    width: 140px;
}

td.amount, th.amount {
    text-align: right;
    white-space: nowrap;
}
.header_table {
    text-align: center;
    border: 1px solid lightGrey;
    border-collapse: collapse;
}
.header_table th {
    font-size: 12px;
    border: 1px solid lightGrey;
}
.header_table td {
    font-size: 12px;
    border: 1px solid lightGrey;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

td.vat {
    white-space: nowrap;
}
.address .recipient {
    font-size: 12px;
    margin-leftt: 120px; 
}
.footer {
    font-size: 12px;
    position: absolute;
    top: 600px;
}
    </style>
</head>
<body class="std_text">
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>
    <%
    def replace_description(text):
        text=carriage_returns(text)
        return text.replace('- 100%', '')
    %>
    <%
    def convert_percentage(text):
        text=text.replace('00', '')
        text=text.replace('0.', '')
    	return text.replace('0,', '')
    %>
    <%
    def convert_percentage_kort(text):
        text=text.replace(',00', '')
        text=text.replace('.00', '')
    	return text
    %>
    
    %for aanv in objects:
	    <% setLang(aanv.partner_id.lang) %>
	    <br/>
	    <h1>${_("Installatieaanvraag")} ${aanv.name}</h1>
	    <br/>
	    <h3>${_("Klantgegevens")}:</h3>
	    <% address_lines = aanv.address.split(", ") %>
	    <div>
	    	<table width="100%">
	    		<tr>
	    			<td style="text-align:left;width:200px;">${_("Naam")}:</td>
	    			<td style="text-align:left;">${aanv.partner_id.name}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Adres")}:</td>
	    			<td>${address_lines[0]}</td>
	    		</tr>
	    		<tr>
	    			<td></td>
	    			<td>${address_lines[1]}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Telefoon vast")}:</td>
	    			<td>${aanv.phone or ''}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Telefoon mobiel")}:</td>
	    			<td>${aanv.mobile or ''}</td>
	    		</tr>
	    	</table>
	    </div
	    <h3>${_("Reparatiegegevens")}:</h3>
	    <div>
	    	<table class="">
	    		<tr>
	    			<td style="text-align:left;width:200px;"><b>${_("RID")}:</b></td>
	    			<td style="text-align:left;">${aanv.name}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Gebracht")}:</td>
	    			<td>${formatLang(aanv.request_date, date=True) or ''}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Aangenomen door")}:</td>
	    			<td>${aanv.user_id.name or ''}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Geplande installatiedatum")}:</td>
	    			<td>${formatLang(aanv.installation_date, date=True) or ''}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Status")}:</td>
	    			<td>${aanv.state}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Type thermostaat")}:</td>
	    			<td>${aanv.case_section_id.name}</td>
	    		</tr>
	    		<tr>
	    			<td>${_("Software Versie")}:</td>
	    			<td>${aanv.software_version_id.name or ''}</td>
	    		</tr>
	    		<tr>
	    			<td VALIGN="top">${_("Aangesloten op klemmen")}:</td>
	    			<td>${aanv.connected_to or '' | carriage_returns}</td>
	    		</tr>
	    		<tr>
	    			<td VALIGN="top">${_("Probleem")}:</td>
	    			<td>${aanv.problem or '' | carriage_returns}</td>
	    		</tr>
	    	</table>
	    </div
	    <p style="page-break-after:always"> </p>
    %endfor
</body>
</html>
