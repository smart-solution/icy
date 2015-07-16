<html>
<head>
     <style type="text/css">
                ${css}
            </style>
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
    	text = text.replace('0.', '')
    	return text.replace('0,', '')
    %>
    <%def name="note_repl(text, user=None, oref=None, prijs=None)">
    	<%
    	output = (((text.replace('\n', '<br />')).replace('[OREF]', oref)).replace('[ACCTMGR]', user)).replace('[PRIJS]', prijs)
    	%>
    	${output}
    </%def>


    %for o in objects:
    <% setLang(o.partner_id.lang) %>
		<table class="shipping_address">
        	<tr>
        		<td width="8%" VALIGN="top">
        		</td>
        		<td width="55%" VALIGN="top">
                    ${ (o.partner_id and o.partner_id.name) or '' }</br>
                    %if o.contact_id:
                   		${_('attn.')}: &nbsp
                    	${o.contact_id.name}</br>
                    %endif
                    ${o.partner_id.street or ''|entity}</br>
           			%if o.partner_id.street2 :
               			${o.partner_id.street2 or ''|entity}</br>
          			%endif
           				${o.partner_id.zip or ''|entity} &nbsp ${o.partner_id.city or ''|entity}</br>
          			%if o.partner_id.country_id :
               			${o.partner_id.country_id.name or ''|entity}</br>
          			%endif
          			</br>
          			%if o.partner_id.phone:
                		${_('Tel.')} : ${ (o.partner_id.phone) or '' }</br>
                	%endif
                	%if o.partner_id.fax :
                		${_('Fax')} : ${ o.partner_id.fax or ''|entity}</br>
                	%endif
                	%if o.partner_id.vat :
                		${_('Vat')} : ${ o.partner_id.vat or ''|entity}</br>
                	%endif
                    </br>
          		</td>
          		<td style="text-align:left" VALIGN="top">
          			%if o.state not in ['draft','sent'] or '':
	                    <b>${_('Shipping address')} :</b>
	                    ${ (o.partner_shipping_id and o.partner_shipping_id.title and o.partner_shipping_id.title.name) or ''}</br>
	                    ${ (o.partner_shipping_id and o.partner_shipping_id.name) or '' }</br>
	                    ${o.partner_shipping_id.street or ''|entity}</br>
	           			%if o.partner_shipping_id.street2 :
	               			${o.partner_shipping_id.street2 or ''|entity}</br>
	          			%endif
	           				${o.partner_shipping_id.zip or ''|entity} &nbsp ${o.partner_shipping_id.city or ''|entity}</br>
	          			%if o.partner_shipping_id.country_id :
	               			${o.partner_shipping_id.country_id.name or ''|entity}</br>
	          			%endif
          			%endif
                </td>
             </tr>
             %if o.state not in ['draft','sent'] or '':
	             <tr>
	        		<td width="8%"  VALIGN="top">
	        		</td>
	        		<td width="55%" VALIGN="top">
	          		</td>
	          		<td style="text-align:left" VALIGN="top">
	                 	<b>${_('Invoice address')} :</b>
	                 	${ (o.partner_invoice_id and o.partner_invoice_id.title and o.partner_invoice_id.title.name) or ''}</br>
                    	${ (o.partner_invoice_id and o.partner_invoice_id.name) or '' }</br>
	                    ${o.partner_invoice_id.street or ''|entity}</br>
	           			%if o.partner_invoice_id.street2 :
	               		${o.partner_invoice_id.street2 or ''|entity}</br>
	          			%endif
	           			${o.partner_invoice_id.zip or ''|entity} &nbsp ${o.partner_invoice_id.city or ''|entity}</br>
	          			%if o.partner_invoice_id.country_id :
	               		${o.partner_invoice_id.country_id.name or ''|entity}</br>
	          			%endif
	                </td>
	              </tr>
              %endif
		</table>
		
		%if o.state in ['draft','sent'] or '':
			<p class="title"><b> ${_('Quotation No') } ${ o.name }</b></p>
		%endif
		%if o.state not in ['draft','sent'] or '':
			<p class="title"><b>${_('Order No') } ${ o.name }</b></p>
		%endif

    	<p class="td_f12">
    	
    	%if o.cc_quotation:
    		<table class="shipping_address">
    			<tr>
    				<td width="14%" VALIGN="top">
    					${_('Bijlage')}:
    				</td>
    				<td>
    					${_('Productomschrijvingen offerte')} ${ o.name }</br>
    					${_('Prijsbepaling ICY Control Center')}
    				</td>
    			</tr>
    		</table>
    	%endif
    	
    	<%
    	note=o.note or ''
    	userid=o.partner_id.user_id.name or ''
    	oref=o.client_order_ref or ''
    	prijs=o.cc_amount or ''
    	%>
		${note_repl(note, userid, oref, prijs)}
		</p>
		
		<p class="td_f12">
		%if o.cc_quotation:
			%for line in o.order_line:
				${_(line.product_id.description_sale_cc) | carriage_returns }</br>
			%endfor
			</br>
		%endif
		</p>
				
		<table class="basic_table">
			<tr>
				<td width="25%">
				%if o.state not in ['draft','sent'] :
					<b>${_('Date Ordered')}</b>
				%endif
				%if o.state in ['draft','sent'] :
					<b>${_('Quotation Date')}</b>
				%endif
				</td></br>
				<td width="25%">
					<b>${_('Salesperson')}</b>
				</td>
				<td width="50%">
					<b>${_('Payment Term')}</b>
				</td>
			</tr>
		
			<tr>
				<td width="25%">
					${ formatLang(o.date_order,date = True) }
				</td>
				<td width="25%">
					${ (o.create_uid and o.create_uid.name) or '' }
				</td>
				<td  width="50%">
					${ (o.payment_term and o.payment_term.name) or '' }
				</td>
			</tr>
		</table>
	   	</br>
		<table class="tr_bottom_line">
<!--
			<tr>
			    <td width="13%">
			    </td>
				<td width="40%">
					<b>${_('Description')}</b>
				</td>
				<td width="5%" align="center">
					<b>${_('VAT(%)')}</b>
				</td>
				<td width="10%" align="center">
					<b>${_('Quantity')}</b>
				</td>
				<td width="10%" align="right">
					<b>${_('Unit Price')}</b>
				</td>
				<td width="10%" align="right">
					<b>${_('Disc.(%)')}</b>
				</td>
				<td width="12%" align="right">
					<b>${_('Price')}</b>
				</td>
			</tr>
-->
			<tr>
				<td width="58%">
					<b>${_('Description')}</b>
				</td>
				<td width="10%" align="center">
					<b>${_('Quantity')}</b>
				</td>
				<td width="10%" align="right">
					<b>${_('Unit Price')}</b>
				</td>
				<td width="10%" align="right">
					<b>${_('Disc.(%)')}</b>
				</td>
				<td width="12%" align="right">
					<b>${_('Price')}</b>
				</td>
			</tr>
		</table>
    
    %for line in o.order_line:
    	<table class="tr_bottom_line_dark_grey" width="90%">
<!--
    		<tr>
 			    <td width="13%">
 			    	%if line.product_id.image_medium:
 			    	${ helper.embed_image("img",line.product_id.image_medium,60,60)}
 			    	%endif
			    </td>
    			<td width="40%" VALIGN="top"> 
    				${ format(line.name) }
    			</td>
    			<td width="5%" align="center" VALIGN="top">
    				${ ', '.join([ formatLang(tax.amount, dp='Account') for tax in line.tax_id ])| convert_percentage}
    			</td>
    			<td width="10%" align="right" VALIGN="top">
    				${ formatLang(line.product_uos and line.product_uos_qty or line.product_uom_qty, dp='SO Qty') }
    			</td>
    			<td width="10%" align="right" VALIGN="top">
    				${ formatLang(line.price_unit , dp='Product Price')}
    				%if line.discount2 :
    				</br>${_('Projkrt.')}
    				%endif
    			</td>
    			<td width="10%" align="right" VALIGN="top">
					%if line.discount1 :
					${ show_discount(user.id) and formatLang(line.discount1, dp='Discount') or ''|entity }
					%endif
					%if line.discount2 :
					</br>${ show_discount(user.id) and formatLang(line.discount2, dp='Discount') or ''|entity }
					%endif
				</td>
    			<td width="12%" align="right" VALIGN="top">
    				${ o.pricelist_id.currency_id.symbol } ${ formatLang(line.price_subtotal, dp='Account') }
    			</td>
    		</tr>
-->
    		<tr>
    			<td width="58%" VALIGN="top"> 
    				${ format(line.name) }
    			</td>
    			<td width="10%" align="right" VALIGN="top">
    				${ formatLang(line.product_uos and line.product_uos_qty or line.product_uom_qty, dp='SO Qty') }
    			</td>
    			<td width="10%" align="right" VALIGN="top">
    				${ formatLang(line.price_unit , dp='Account')}
    				%if line.discount2 :
    				</br>${_('Projkrt.')}
    				%endif
    			</td>
    			<td width="10%" align="right" VALIGN="top">
					%if line.discount1 :
					${ show_discount(user.id) and formatLang(line.discount1, dp='Discount') or ''|entity }
					%endif
					%if line.discount2 :
					</br>${ show_discount(user.id) and formatLang(line.discount2, dp='Discount') or ''|entity }
					%endif
				</td>
    			<td width="12%" align="right" VALIGN="top">
    				${ o.pricelist_id.currency_id.symbol } ${ formatLang(line.price_subtotal, dp='Account') }
    			</td>
    		</tr>
    	</table>
    %endfor
    		<tr>
    			<td width="70%">
    			</td>
    			<td width="30%">
    				<table class="tr_top">
			    		<tr>
			    			<td >
			    				${_('Net Total')} :
			    			</td>
			    			<td width="40%" style="text-align:right">
			    				${ o.pricelist_id.currency_id.symbol } ${ formatLang(o.amount_untaxed, dp='Account') }
			    			</td>
			    		</tr>
			    		<tr>
			    			<td >
			    				${_('VAT')} ${ ', '.join([ formatLang(tax.amount, dp='Account') for tax in o.order_line[0].tax_id ])| convert_percentage}%:
			    			</td>
			    			<td width="40%" style="text-align:right"> 
			    				${ o.pricelist_id.currency_id.symbol } ${ formatLang(o.amount_tax, dp='Account') }
			    			</td>
			    		</tr>
			    	</table>
    			</td>
    		</tr>
    		<tr>
    			<td></td>
    			<td>
    				<table class="tr_top">
    					<tr>
    						<td>
    							<b>${_('Total :')}</b>
				    		</td>
				    		<td align="right">
				    			<b>${ o.pricelist_id.currency_id.symbol } ${ formatLang(o.amount_total, dp='Account') }</b>
				    		</td>
				 		</tr>
				 	</table>
				 </td>
			</tr>
    	</table>
    	
    	<p class="td_f12">
    	</br>

    	<%
    	note=_(o.cc_product_id.description_sale_cc) or ''
    	%>
		</p>
		    	
    	%if o.cc_quotation:
    		<p style="page-break-after: always">&nbsp</p>
    		<p class="td_f12">
    		</br>
			${note_repl(note, userid, oref, prijs) | carriage_returns}
			</br>
			</p>
		%endif
    	
    	%if o.state in ['draft','sent'] or '':
    		<p style="page-break-after: always">&nbsp</p>
    	%endif
    	<p class="td_f12">
		%if o.state in ['draft','sent'] or '':
			</br>
    		${ (format(o.note_footer or '') )| carriage_returns }
    		</br></br>
		%endif
		%if o.state not in ['draft','sent'] or '':
    		${format(o.payment_term and o.payment_term.note or (o.partner_id.property_payment_term and o.partner_id.property_payment_term.note or '')) | carriage_returns }
		%endif
		</p>
    	<p style="page-break-after: always">&nbsp</p>
		%if o.cc_quotation:
			</br>
			<p class="b12"><b>${_('Product descriptions tender')} ${ o.name } d.d. ${ formatLang(o.date_order,date = True) }</b></p></br></br>
			%for line in o.order_line:
				<p class="i12"><i>${ format(line.name) }</i></p>
				</br>
				<p class="td_f12">${_(line.product_id.product_description_sale_cc) | carriage_returns}</br></p>
				</br>
			%endfor
			%if o.cc_product_id.product_description_sale_cc:
				<p style="page-break-after: always">&nbsp</p>
				<p class="td_f12">
				</br>
				${_(o.cc_product_id.product_description_sale_cc) | carriage_returns}</br>
				</p>
				<p style="page-break-after: always">&nbsp</p>
			%endif
		%endif
    %endfor
</body>
</html>

