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

.text_table {
	width:90%;
	text-align: left;
	font-family: Helvetica;
    font-size: 12px;
	padding-bottom:20px; 
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
    	text=text.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
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
    
    
    %for contract in objects:
	    <% setLang(contract.partner_id.lang) %>
	    </br>
	    %for text in contract.contract_type_id.text_ids:
	    	<%
	    	txt=text.text
	    	txt2=text.text2
	    	%>
	    	%for fields in text.field_ids:
	    		%if fields.label:
					<%
					resp="..............."
					orig = fields.label
					if fields.dbfield:
						sql_stat = fields.dbfield % (contract.id, )
						cr.execute(sql_stat)
						for sql_res in cr.dictfetchall():
							if sql_res['resp']:
								resp = sql_res['resp']
					if txt:
						txt = txt.replace(orig, resp)
					if txt2:
						txt2 = txt2.replace(orig, resp)
					%>
	    		%endif
	    	%endfor
	    	<table class="text_table">
	    		<td valign="top" width="5%">
	    			%if text.prefix:
				    	%if text.bold:
				    		<b>
				    	%endif
				    	%if text.underlined:
				    		<u>
				    	%endif
		    			${text.prefix}
				    	%if text.underlined:
				    		</u>
				    	%endif
				    	%if text.bold:
				    		</b>
				    	%endif
			    	%endif
	    		</td>
	    		%if text.text2:
		    		<td valign="top" width="48%">
				    	%if text.bold:
				    		<b>
				    	%endif
				    	%if text.underlined:
				    		<u>
				    	%endif
		    			${txt | carriage_returns}
				    	%if text.underlined:
				    		</u>
				    	%endif
				    	%if text.bold:
				    		</b>
				    	%endif
		    		<td valign="top" width="47%">
				    	%if text.bold:
				    		<b>
				    	%endif
				    	%if text.underlined:
				    		<u>
				    	%endif
		    			${txt2 | carriage_returns}
				    	%if text.underlined:
				    		</u>
				    	%endif
				    	%if text.bold:
				    		</b>
				    	%endif
	    		%else:
		    		<td valign="top" width="95%">
				    	%if text.bold:
				    		<b>
				    	%endif
				    	%if text.underlined:
				    		<u>
				    	%endif
		    			${txt | carriage_returns}
				    	%if text.underlined:
				    		</u>
				    	%endif
				    	%if text.bold:
				    		</b>
				    	%endif
			    	</td>
		    	%endif
	    	</table>
	    	%if text.product_table:
				<table class="basic_table">
					<tr>
						<td width="50%">
							<b>${_('Omschrijving')}</b>
						</td></br>
						<td width="25%">
							<b>${_('Aantal')}</b>
						</td>
						<td width="25%">
							<b>${_('Prijs')}</b>
						</td>
					</tr>
					%for product in contract.product_ids:
					<tr>
						<td width="50%">
							${ product.product_id.name_template }
						</td>
						<td width="25%">
							${ product.qty_contract }
						</td>
						<td  width="25%">
							${ product.unit_price }
						</td>
					</tr>
					%endfor
				</table>
	    	%endif
	    	%if text.page_skip_after:
	    		<p style="page-break-after:always">&nbsp;</p></br></br>
	    	%endif
	    %endfor
    %endfor
</body>
</html>
