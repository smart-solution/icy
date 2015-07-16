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
    
    %for inv in objects:
	    <% print_detail = 0 %>
	    <% setLang(inv.partner_id.lang) %>
	    <br/>
	    <br/>
	    <div class="address">
	      %if hasattr(inv, 'commercial_partner_id'):
	        <table class="recipient">
	            %if inv.partner_id.id != inv.commercial_partner_id.id:
	            <tr>
	        		<td width="8%" VALIGN="top">
	        		</td>
		            <td class="name">${inv.commercial_partner_id.name or ''}</td></tr>
	            <tr>
	        		<td width="8%" VALIGN="top">
	        		</td>
		            <td>${inv.partner_id.title and inv.partner_id.title.name or ''} ${inv.partner_id.name }</td>
		        </tr>
	            %else:
	            <tr>
	        		<td width="8%" VALIGN="top">
	        		</td>
		            <td class="name">${inv.partner_id.title and inv.partner_id.title.name or ''} ${inv.partner_id.name }</td>
		        </tr>
	            %endif
	            %if inv.partner_id.parent_id:
	            <% address_lines = inv.partner_id.contact_address.split("\n")[1:] %>
	            %else:
	            <% address_lines = inv.partner_id.contact_address.split("\n") %>
	            %endif
	            %for part in address_lines:
	                %if part:
	                <tr>
	      	        	<td width="8%" VALIGN="top">
	      		  		</td>
	                	<td>${part}</td>
	                </tr>
	                %endif
	            %endfor
	            %if inv.partner_id.vat:
	            <tr>
	      	        <td width="8%" VALIGN="top">
	        		</td>
	            	<td>${_("VAT nbr.")}: ${inv.partner_id.vat or ''}</td>
	            </tr>
	            %endif
	        </table>
	      %else:
	        <table class="recipient">
	            %if inv.partner_id.parent_id:
	            <tr>
	      	        <td width="8%" VALIGN="top">
	        		</td>
	            	<td class="name">${inv.partner_id.parent_id.name or ''}</td>
	            </tr>
	            <tr>
	      	        <td width="8%" VALIGN="top">
	        		</td>
	            	<td>${inv.partner_id.title and inv.partner_id.title.name or ''} ${inv.partner_id.name }</td>
	            </tr>
	            <% address_lines = inv.partner_id.contact_address.split("\n")[1:] %>
	            %else:
	            <tr>
	      	        <td width="8%" VALIGN="top">
	        		</td>
	            	<td class="name">${inv.partner_id.title and inv.partner_id.title.name or ''} ${inv.partner_id.name }</td>
	            </tr>
	            <% address_lines = inv.partner_id.contact_address.split("\n") %>
	            %endif
	            %for part in address_lines:
	                %if part:
	                <tr>
	      	        	<td width="8%" VALIGN="top">
		        		</td>
		                <td>${part}</td></tr>
	                %endif
	            %endfor
	            %if inv.partner_id.vat:
	            <tr>
	        		<td width="8%" VALIGN="top">
	        		</td>
	            	<td><br/>${_("VAT nbr.")}: ${inv.partner_id.vat or ''}</td></tr>
	            %endif
	        </table>
	      %endif
	    </div>
	    <div>
	      <br/>
	      <br/>
	      <h1 style="clear: both; padding-top: 20px;">
	        <table width="100%">
	          <tr>
	          <td style="text-align:left;">
  	          %if inv.type == 'out_invoice' and inv.state == 'proforma2':
	            ${_("PRO-FORMA")}
	          %elif inv.type == 'out_invoice' and inv.state == 'draft':
	            ${_("Draft FACTUUR")}
	          %elif inv.type == 'out_invoice' and inv.state == 'cancel':
	            ${_("Geannulleerde FACTUUR")}: ${inv.number or ''}
	          %elif inv.type == 'out_invoice':
	            ${_("FACTUUR")}: ${inv.number or ''}
	          %elif inv.type == 'in_invoice':
	            ${_("Supplier Invoice")}: ${inv.number or ''}
	          %elif inv.type == 'out_refund':
	            ${_("Refund Invoice")}: ${inv.number or ''}
	          %elif inv.type == 'in_refund':
	            ${_("Supplier Refund")}: ${inv.number or ''}
	          %endif
	          <td style="text-align:right;">
	          ${_("Factuurdatum")}: ${formatLang(inv.date_invoice, date=True)}
	          </td>
	          </tr>
	        </table>
	      </h1>

	      %if inv.origin:
	        <% origin = inv.origin.split(":")[1:] %>
	      %endif
    
          
          %if inv.origin:
          	<b>${_("Betreft")}: </b>
            %for originpart in origin:
              %if originpart:
                Uw order ${originpart} 
              %endif
            %endfor
            </br>
          %endif
	    %if inv.name:
	    	<b>${_("Referentie")}: </b>${inv.name}
	    %endif
		</div>

		
	    <div>
	    %if inv.note1:
	        <p class="std_text"> ${inv.note1 | n} </p>
	    %endif
	    </div>
	    
		<div>
	      <table class="list_invoice_table" width="100%" style="margin-top: 20px;">
	        <thead>
	            <tr>
	                <th style="text-align:left;width:50px;">${_("Qty")}</th>
	                <th>${_("Description")}</th>
	                <th style="text-align:right;width:60px;">${_("Unit Price")}</th>
	                <th style="text-align:right;width:50px;">${_("Disc")}</th>
	                <th style="text-align:right;width:50px;">${_("VAT")}</th>
	                <th style="text-align:right;width:60px;">${_("Total")}</th>
	            </tr>
	        </thead>
	        <tbody>
	          %for line in inv.invoice_line :
	            <tr >
	                <td class="amount">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
	                <td>${line.product_id and line.product_id.code or ''} ${line.product_id and line.product_id.name or line.name}</td>
	                <td class="amount">${inv.currency_id.symbol} ${formatLang(line.price_unit, digits=get_digits(dp='Account'))}</td>
	                <td class="amount" >${formatLang(line.discount, digits=get_digits(dp='Account'))| convert_percentage_kort} %</td>
	                <td class="amount" >${ ', '.join([ formatLang(tax.amount, digits=get_digits(dp='Account')) for tax in line.invoice_line_tax_id ])| convert_percentage} %</td>
	                <td class="amount" width="13%">${inv.currency_id.symbol} ${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))}</td>
	            </tr>
	            %if line.formatted_note:
	            <tr>
	              <td class="formatted_note" colspan="5">
	                ${line.formatted_note| n}
	              </td>
	            </tr>
	            %endif
	          %endfor
	        </tbody>
	        <tfoot class="totals">
	            <tr>
	                <td colspan="5" style="text-align:right;border-right: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
	                    <b>${_("Net")}:</b>
	                </td>
	                <td class="amount" style="border-right: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
	                    ${inv.currency_id.symbol} ${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} 
	                </td>
	            </tr>
	            <tr class="no_bloc">
	                <td colspan="5" style="text-align:right; border-top: thin solid  #ffffff ; border-right: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
	                    <b>${_("VAT")}:</b>
	                </td>
	                <td class="amount" style="border-right: thin solid  #ffffff ;border-top: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
	                        ${inv.currency_id.symbol} ${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} 
	                </td>
	            </tr>
	            <tr>
	                <td colspan="5" style="border-right: thin solid  #ffffff ;border-top: thin solid  #ffffff ;border-left: thin solid  #ffffff ;border-bottom: thin solid  #ffffff ;text-align:right;">
	                    <b>${_("Total")}:</b>
	                </td>
	                <td class="amount" style="border-right: thin solid  #ffffff ;border-top: thin solid  #ffffff ;border-left: thin solid  #ffffff ;border-bottom: thin solid  #ffffff ;">
	                    <b>${inv.currency_id.symbol} ${formatLang(inv.amount_total, digits=get_digits(dp='Account'))}</b>
	                </td>
	            </tr>
	        </tfoot>
	      </table>
	    </div>
	    <div>
	        <br/>
	      <table class="list_total_table" width="60%" >      
	        %if inv.tax_line :
	        <tr>
	            <th style="text-align:left;">${_("VAT")} %</th>
	            <th style="text-align:right;">${_("Base")}</th>
	            <th style="text-align:right;">${_("VAT")}</th>
	        </tr>
	          %for t in inv.tax_line :
	            <tr>
	                <td style="text-align:left;">${ formatLang(tax.amount, digits=get_digits(dp='Account'))| convert_percentage } %</td>
	                <td class="amount">${inv.currency_id.symbol} ${ formatLang(t.base, digits=get_digits(dp='Account')) }</td>
	                <td class="amount">${inv.currency_id.symbol} ${ formatLang(t.amount, digits=get_digits(dp='Account')) }</td>
	            </tr>
	          %endfor
	        %endif
	      </table>
	      <br/>
	      %if inv.comment :
	        <p class="std_text">${inv.comment | carriage_returns}</p>
	      %endif
	      %if inv.note2 :
	        <p class="std_text">${inv.note2 | n}</p>
	      %endif
	      %if inv.fiscal_position.note :
	        <br/>
	        <p class="std_text">
	        ${inv.fiscal_position.note | n}
	        </p>
	      %endif
	        <br/>   
	    <br/>
	    %if inv.type == 'out_refund':
		    ${_("Bovengenoemd bedrag zal zo spoedig mogelijk worden overgemaakt op het bij ons bekende rekeningnummer ")}
		    	%if inv.partner_bank_id:
		    		${inv.partner_bank_id.acc_number}
		    	%endif
		    	,${_(" of verrekend met eventuele openstaande posten.")}
		%else:
		    ${_("Wij verzoeken u bovenstaand bedrag over te maken op bankrekening 904426270")} <br/>
		    (IBAN: NL51SNSB0904426270, BIC: SNSBNL2A).<br/>
		    ${_("Uw betaling dient ten laatste op")} ${formatLang(inv.date_due, date=True)} ${_("te zijn bijgeschreven op bovenstaand rekeningnummer.")} 
		    <br/>
		    %if inv.number:
		        <p class="std_text">${_("Gelieve te betalen met volgende mededeling:")} ${inv.number or ''}</p>
		    %endif
		    ${_("Betalingsvoorwaarde")}:
		    </br> ${inv.payment_term.note | carriage_returns}
	    %endif
	    %if inv.type == 'out_refund':
			</br></br>
			${_("Met vriendelijke groet,")}</br>
			I.C.Y.B.V.</br>
	    %endif
	    </div
	    <p style="page-break-after:always"> </p>
    %endfor
</body>
</html>
