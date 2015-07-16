<html>
<head>
    <style type="text/css">
            ${css}
        </style>
    <title>requestforquotation.pdf</title>
</head>
<body RIGHTMARGIN="300">
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
    	return text.replace('0,', '')
    %>

    %for o in objects:
    <% setLang(o.partner_id.lang) %>
		<table class="shipping_address">
        	<tr>
        		<td width="5%">
        		</td>
        		<td width="65%">
          			</br>
                    ${ (o.partner_id and o.partner_id.name) or '' }</br>
                    ${o.partner_id.street or ''|entity}</br>
           			%if o.partner_id.street2 :
               			${o.partner_id.street2 or ''|entity}</br>
          			%endif
           				${o.partner_id.zip or ''|entity}, ${o.partner_id.city or ''|entity}</br>
          			%if o.partner_id.country_id :
               			${o.partner_id.country_id.name or ''|entity}</br>
          			%endif
          		</td>
          		<td style="text-align:left">
                </td>
             </tr>
		</table>
        </br>
        <h3><b>${_('Request for Quotation')} : ${ o.name }</b></h3>
        </br>
        </br>
        </br>
        <table class="tr_bottom_line" STYLE="font-size: 9px;">
            <tr>
            	<td width="3%" VALIGN="top"><b>${_('Pos')}</b></td>
                <td width="17%" VALIGN="top">
                  <b>${_('Part No.')}</b></br>
                  <b>${_('Productcode')}</b>
                </td>
                <td width="45%" VALIGN="top">
                  <b>${_('Description')}</b>
                </td>
                <td width="18%" VALIGN="top">
                  <b>${_('Request')}</b></br> 
                  <b>${_('Date')}</b></br>
                  <b>${_('MM-DD-YYYY')}</b>
                </td>
                <td style="text-align:right" width="15%" VALIGN="top">
                  <b>${_('Quantity')}</b>
                </td>
              </tr>
        </table>
        <% tel = 0 %>
        %for  order_line in o.order_line:
        <% tel += 1 %>
        <table  class="tr_bottom_line_dark_grey"STYLE="font-size: 9px;">
          <tr>
          	<td width="3%" VALIGN="top">
          		${tel}
          	</td>
            <td width="17%" VALIGN="top">
                 %if order_line.product_id.default_code:
                ${ order_line.product_id.default_code }
                %endif
                %if order_line.supplier_product_nbr:
                </br>${ order_line.supplier_product_nbr }
                %endif                
            </td>
            <td width="45%" VALIGN="top">
                ${ order_line.name }</br>
                %if order_line.product_id.icy_value:
                ${_('Value')}: ${ order_line.product_id.icy_value }</br>
                %endif
                %if order_line.product_id.icy_package:
                ${_('Package')}: ${ order_line.product_id.icy_package }</br>
                %endif
                %if order_line.manufacturer_product:
                ${_('Manufacturer')}: ${ order_line.manufacturer_product }</br>
                %endif
                %if order_line.manufacturer_product_nbr:
                ${_('Man. Prod. No.')}: ${ order_line.manufacturer_product_nbr }
                %endif
            </td>
            <td width="18%" VALIGN="top">
                ${ formatLang(order_line.date_planned, date = True) }
            </td>
            <td width="17%" align="right" VALIGN="top">
                ${ formatLang(order_line.product_qty, digits=get_digits(dp='SO Qty') )}
                <i>${ (order_line.product_uom and order_line.product_uom.name) or '' }</i>
            </td>
          </tr>
        </table>
         %endfor
        </br>
        </br>
        <table width="95%" STYLE="font-size: 9px;">
        	%if o.payment_term_id:
		        <tr>
		        	<td width="16%" VALIGN="top"><b>${_('Payment Term')}:</b></td>
		        	<td VALIGN="top">${o.payment_term_id.name}</td>
		        </tr>
			%endif
        	%if o.incoterm:
		        <tr>
		        	<td width="16%" VALIGN="top"><b>${_('Incoterm')}:</b></td>
		        	<td VALIGN="top">${o.incoterm.name}</td>
		        </tr>
			%endif
			<tr>
				<td width="16%" VALIGN="top"><b>${_('Delivery Address')}:</b></td>
				<td VALIGN="top">
                    ${ (o.warehouse_id and o.warehouse_id.name) or ''}</br>
                    ${o.warehouse_id.partner_id.street or ''|entity}</br>
           			%if o.warehouse_id.partner_id.street2 :
               			${o.warehouse_id.partner_id.street2 or ''|entity}</br>
          			%endif
           				${o.warehouse_id.partner_id.zip or ''|entity}, ${o.warehouse_id.partner_id.city or ''|entity}</br>
          			%if o.warehouse_id.partner_id.country_id :
               			${o.warehouse_id.partner_id.country_id.name or ''|entity}</br>
          			%endif
          		</td>
          	</tr>
			%if o.aanleiding :
				<tr>
            		<td width="16%" VALIGN="top"><b>${_('Cause')}:</b></td>
					<td VALIGN="top"> ${o.aanleiding | carriage_returns}</td>
				</tr>
        	%endif
        </table>
        <p class="td_f12" STYLE="font-size: 9px;">
        </br>
        </br>
        ${_('Regards,')}
        </br>
        ${ user.name or ''}</br>
        </br>
        </br>
        </br>
        ${ o.notes or '' | carriage_returns}</br>
        </p>
        <table width="95%" STYLE="font-size: 9px;">
        	%if o.po_text:
		        <tr>
		        	<td VALIGN="top">${o.po_text | carriage_returns}</td>
		        </tr>
			%endif
        </table>
       <p style="page-break-after:always">
        </p>
       
    %endfor
</body>
</html>