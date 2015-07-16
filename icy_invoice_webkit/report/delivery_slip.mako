## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>

<body RIGHTMARGIN="300">
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>
    %for inv in objects:
        <% setLang(inv.partner_id.lang) %>
        <div class="address">
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
	        </table>
        </div>
        </br>
        </br>
		<h1>
  	          %if inv.type == 'out_invoice' and inv.state == 'proforma2':
	            ${_("Pakbon voor PRO-FORMA")}
	          %elif inv.type == 'out_invoice' and inv.state == 'draft':
	            ${_("Pakbon voor Draft FACTUUR")}
	          %elif inv.type == 'out_invoice' and inv.state == 'cancel':
	            ${_("Pakbon voor Geannulleerde FACTUUR")}: ${inv.number or ''}
	          %elif inv.type == 'out_invoice':
	            ${_("Pakbon voor FACTUUR")}: ${inv.number or ''}
	          %elif inv.type == 'in_invoice':
	            ${_("Pakbon voor Supplier Invoice")}: ${inv.number or ''}
	          %elif inv.type == 'out_refund':
	            ${_("Pakbon voor Refund Invoice")}: ${inv.number or ''}
	          %elif inv.type == 'in_refund':
	            ${_("Pakbon voor Supplier Refund")}: ${inv.number or ''}
	          %endif
        </h1>
        </br>
        
        <table class="basic_table" width="100%">
            <tr>
                <td style="font-weight:bold;">${_("Pakbonnr (fact)")}</td>
                <td style="font-weight:bold;">${_("Pakbondatum")}</td>
                <td style="font-weight:bold;">${_("Klantnummer")}</td>
            </tr>
            <tr>
                <td>${inv.number or ''}</td>
                <td>${formatLang(inv.date_invoice, date=True)}</td>
                <td>${inv.partner_id.ref or " "}</td>
            </tr>
        </table>
        <p class="td_f12">
        </br>
	      %if inv.origin:
	        <% origin = inv.origin.split(":")[1:] %>
	      %endif
    
          <b>Betreft: </b>
          %if inv.origin:
            %for originpart in origin:
              %if originpart:
                Uw order ${originpart} 
              %endif
            %endfor
          %endif
    	</br>
    	</br>
    	</p>
        <table class="tr_bottom_line">
            <tr class="tr_bottom_line">
            	<th style="text-align:left"; width="13%">${_("Datum")}</th>
            	<th style="text-align:right"; width="15%">${_("Aantal")}</th>
                <th style="text-align:left"; width="52%">${_("Description")}</th>
                <th style="text-align:right"; width="20%">${_("Aantal besteld")}</th>
            </tr>
        </table>
        <table class="tr_bottom_line">
	        %for line in inv.invoice_line:
	        	%if line.order_lines:
		        	%for orderline in line.order_lines:
	        		<tbody class="tr_bottom_line_dark_grey">
	                <tr class="line">
	                	<td style="text-align:left"; width="13%">${formatLang(inv.date_invoice, date=True)}</td>
	                    <td style="text-align:right"; width="15%">${ formatLang(line.quantity, digits=get_digits(dp='Account')) }</td>
	                    <td style="text-align:left"; width="57%" >${line.product_id and line.product_id.name or line.name}</td>
	                    %if orderline.product_uom_qty:
	                    <td style="text-align:right"; width="15%" >${ formatLang(orderline.product_uom_qty, digits=get_digits(dp='Account'))}</td>
	                    %endif
	                </tr>
	                %endfor
	            %else:
	        		<tbody class="tr_bottom_line_dark_grey">
	                <tr class="line">
	                	<td style="text-align:left"; width="13%">${formatLang(inv.date_invoice, date=True)}</td>
	                    <td style="text-align:right"; width="15%">${ formatLang(line.quantity, digits=get_digits(dp='Account')) }</td>
	                    <td style="text-align:left"; width="57%" >${line.product_id and line.product_id.name or line.name}</td>
	                </tr>
	            %endif
	        %endfor
    	</table>
        
        <br/>
        
		%if inv.partner_id.delivery_note_signature:
			</br></br>
			<h3>In ontvangst genomen door:</h3>
			Naam (in blokletters):____________________________________</br></br>
			Datum: _______________________________________________</br></br></br>
			Handtekening: __________________________________________</br>
			<h3>Gelieve de getekende pakbon per omgaande te faxen naar 0514-564252</h3>
		%endif
        <p style="page-break-after: always"/>
	 
    %endfor
</body>
</html>
