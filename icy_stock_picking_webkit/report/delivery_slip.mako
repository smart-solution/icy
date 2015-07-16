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
    %for picking in objects:
        <% setLang(picking.partner_id.lang) %>
	    <br/>
	    <br/>
        <div class="address">
            <table class="recipient">
                %if picking.partner_id.parent_id:
                <tr><td class="name">${picking.partner_id.parent_id.name or ''}</td></tr>
                <tr><td>${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
                <% address_lines = picking.partner_id.contact_address.split("\n")[1:] %>
                %else:
                <tr><td class="name">${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
                <% address_lines = picking.partner_id.contact_address.split("\n") %>
                %endif
                %for part in address_lines:
                    %if part:
                    <tr><td>${part}</td></tr>
                    %endif
                %endfor
            </table>
        </div>
        </br>
        </br>
        
        <h1 style="clear:both;">${_('Pakbon') } ${picking.name}</h1>
        </br>
        
        <table class="basic_table" width="100%">
            <tr>
                <td style="font-weight:bold;">${_('Pakbonnr')}</td>
                <td style="font-weight:bold;">${_('Pakbondatum')}</td>
                <td style="font-weight:bold;">${_('Klantnummer')}</td>
            </tr>
            <tr>
                <td>${picking.name}</td>
                <td>${formatLang(picking.min_date, date=True)}</td>
                <td>${picking.partner_id.ref or " "}</td>
            </tr>
        </table>
        </br>
        %if picking.sale_id:
        	%if picking.sale_id.client_order_ref:
		        <h3>
		        ${_('Betreft: uw inkooporder nr.')} ${picking.sale_id.client_order_ref}
		        </h3>
		    %endif
        %endif
    	</br></br>
        <table class="tr_bottom_line">
            <tr class="tr_bottom_line">
            	<th style="text-align:left"; width="13%">${_("Date")}</th>
            	<th style="text-align:right"; width="15%">${_("Quantity")}</th>
                <th style="text-align:left"; width="42%">${_("Description")}</th>
<!--
                %if picking.origin != "Service Omruil" :
	                <th style="text-align:right"; width="15%">${_("Aantal besteld")}</th>
                    <th style="text-align:right"; width="15%">${_("Reeds geleverd")}</th>
                %endif
-->
            </tr>
        </table>
        <table class="tr_bottom_line">
	        %for line in picking.move_lines:
        	<tbody class="tr_bottom_line_dark_grey">
                <tr class="line">
                	<td style="text-align:left"; width="13%">${formatLang(line.date_expected, date=True)}</td>
                    <td style="text-align:right"; width="15%">${ formatLang(line.product_qty, digits=get_digits(dp='Account')) }</td>
                    <td style="text-align:left"; width="42%" >${ line.name }</td>
<!--
                    %if line.sale_line_id.product_uom_qty:
                    <td style="text-align:right"; width="15%" >${ formatLang(line.sale_line_id.product_uom_qty, digits=get_digits(dp='Account'))}</td>
                    %endif
                    %if line.sale_line_id.product_uom_qty:
                    <td style="text-align:right"; width="15%" >${ formatLang(line.sale_line_id.qty_delivered, digits=get_digits(dp='Account'))}</td>
                    %endif
-->
                </tr>
	        %endfor
    	</table>
		<br/>
		%if picking.origin != "Service Omruil" :
			%if picking.sale_id:
				<h3>${_("Sales Order Overview")}</h3>
		        <table class="tr_bottom_line">
		            <tr class="tr_bottom_line">
		            	<th style="text-align:left"; width="13%">${_("Date")}</th>
<!--
		            	<th style="text-align:right"; width="15%">${_("Quantity")}</th>
-->
		                <th style="text-align:left"; width="42%">${_("Description")}</th>
		                <th style="text-align:right"; width="10%">${_("Aantal besteld")}</th>
	                    <th style="text-align:right"; width="10%">${_("Reeds geleverd")}</th>
	                    <th style="text-align:right"; width="10%">${_("Nog te leveren")}</th>
		            </tr>
		        </table>
		        <table class="tr_bottom_line">
			        %for soline in picking.sale_id.order_line:
		        	<tbody class="tr_bottom_line_dark_grey">
		                <tr class="line">
		                	<td style="text-align:left"; width="13%" VALIGN="top">${formatLang(soline.date_expected, date=True)}</td>
<!--
		                    <td style="text-align:right"; width="15%">${ formatLang(line.product_qty, digits=get_digits(dp='SO Qty')) }</td>
-->
		                    <td style="text-align:left"; width="42%" VALIGN="top">${ soline.name }</td>
		                    %if soline.product_uom_qty:
		                    <td style="text-align:right"; width="10%" VALIGN="top">${ formatLang(soline.product_uom_qty, digits=get_digits(dp='SO Qty'))}</td>
		                    %else:
		                    <td style="text-align:right"; width="10%" VALIGN="top"></td>
		                    %endif
		                    %if soline.qty_delivered:
		                    <td style="text-align:right"; width="10%" VALIGN="top">${ formatLang(soline.qty_delivered, digits=get_digits(dp='SO Qty'))}</td>
		                    %else:
		                    <td style="text-align:right"; width="10%" VALIGN="top"></td>
		                    %endif
		                    <td style="text-align:right"; width="10%" VALIGN="top">
		                    <% 
		                    	a = soline.product_uom_qty
		                    	a = a - soline.qty_delivered
		                    %>
		                    ${ formatLang(a, digits=get_digits(dp='SO Qty'))}
		                    </td>	
		                </tr>
			        %endfor
		    	</table>
			%endif
		%endif
		        
        <br/>
        %if picking.note and picking.note <> picking.sale_id.note:
            <p class="std_text">${picking.note | carriage_returns}</p>
        %endif
        
		%if picking.partner_id.delivery_note_signature:
			</br></br>
			<h3>In ontvangst genomen door:</h3>
			Naam (in blokletters):____________________________________</br></br>
			Datum: _______________________________________________</br></br></br>
			Handtekening: __________________________________________</br>
			<h3>Gelieve de getekende pakbon per omgaande te faxen naar 0514-564252</h3>
		%endif
        <p style="page-break-after: always"/>
	 
	 	%if picking.origin == "Service Omruil" :
	 	
	 	</br>
	 	</br>
	 	<h1>Retourformulier</h1>
	 	<h3>
	 	Let op: ICY kan terugzending/garantie alleen in</br>
	 	behandeling nemen wanneer dit retourformulier</br>
	 	compleet is ingevuld en bijgesloten.
	 	</h3>
	 	</br>
	 	</br>
	 	<h3>Uw gegevens</h3>
	 	<table class="tr_bottom_line">
            %if picking.partner_id.parent_id:
            <tr><td width="25%">Naam</td><td class="name" width="75%">:${picking.partner_id.parent_id.name or ''}</td></tr>
            <tr><td></td><td>${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
            <td></td><% address_lines = picking.partner_id.contact_address.split("\n")[1:] %>
            %else:
            <tr><td>Naam</td><td class="name">${picking.partner_id.title and picking.partner_id.title.name or ''} ${picking.partner_id.name }</td></tr>
            <% address_lines = picking.partner_id.contact_address.split("\n") %>
            %endif
            %for part in address_lines:
                %if part:
                <tr><td></td><td>${part}</td></tr>
                %endif
            %endfor
            <tr>
            <td>E-mail adres</td>
            %if picking.partner_id.parent_id:
            	%if picking.partner_id.parent_id.email:
            		<td>: ${picking.partner_id.parent_id.email}</td>
        		%else:
        			<td>:__________________________________________________________________</td>
        		%endif
            %else:
            	%if picking.partner_id.email:
            		<td>: ${picking.partner_id.email}</td>
        		%else:
        			<td>:__________________________________________________________________</td>
        		%endif
            %endif
            </tr>
			<tr></tr>
		 	<tr>
			 	<td>Uw merk ketel</td>
            	%if picking.helpdesk_id:
            		%if picking.helpdesk_id.brandtype:
            			<td>: ${picking.helpdesk_id.brandtype}</td>
	        		%else:
	        			<td>:__________________________________________________________________</td>
					 	</tr>
					 	<tr>
						 	<td>Uw type ketel</td>
						 	<td>:__________________________________________________________________</td>
	        		%endif
        		%else:
        			<td>:__________________________________________________________________</td>
				 	</tr>
				 	<tr>
					 	<td>Uw type ketel</td>
					 	<td>:__________________________________________________________________</td>
        		%endif
		 	</tr>
		 	<tr>
			 	<td>Power converter geplaatst</td>
			 	<td>: ja    /     nee </td>
		 	</tr>
		</table> 	
	 	<h3>Productgegevens</h3>
	 	<table class="tr_bottom_line">
		 	<tr>
			 	<td width="25%">Productnaam</td>
            	%if picking.helpdesk_id:
            		%if picking.helpdesk_id.product_id:
            			<td width="75%">: ${picking.helpdesk_id.product_id.name}</td>
	        		%else:
	        			<td width="75%">:__________________________________________________________________</td>
        			%endif
    			%else:
    				<td width="75%">:__________________________________________________________________</td>
				%endif
		 	</tr>
		 	<tr>
			 	<td>Serienummer</td>
            	%if picking.helpdesk_id:
            		%if picking.helpdesk_id.serial_nbr1:
            			<td width="75%">: ${picking.helpdesk_id.serial_nbr1.name}</td>
	        		%else:
	        			<td width="75%">:__________________________________________________________________</td>
        			%endif
    			%else:
    				<td width="75%">:__________________________________________________________________</td>
				%endif
		 	</tr>
		</table> 	
	 	<h3>Installatie</h3>
	 	<table class="tr_bottom_line">
		 	<tr>
			 	<td width="25%">Installatie gedaan door</td>
			 	<td width="75%">: mijzelf/een ander</td>
		 	</tr>
		 	<tr>
			 	<td></td>
			 	<td>namelijk door: ________________________________________________</td>
		 	</tr>
		 	<tr>
			 	<td></td>
			 	<td>telefoonnummer: ______________________________________________</td>
		 	</tr>
		</table> 	
	 	<h3>Reden retour:</h3>
	 	<table class="tr_bottom_line">
		 	<tr>
			 	<td>________________________________________________________________________________</td>
		 	</tr>
	 	</table>
	 	<h3>In te vullen door I.C.Y. B.V.</h3>
	 	<table class="tr_bottom_line">
		 	<tr>
			 	<td width="25%">Datum ontvangst</td>
			 	<td width="75%">:________________________________________________________________</td>
		 	</tr>
		 	<tr>
			 	<td>Reparatie/Garantie</td>
			 	<td>:________________________________________________________________</td>
		 	</tr>
		 	<tr>
			 	<td>Opmerkingen</td>
			 	<td>:________________________________________________________________</td>
		 	</tr>
		</table> 	
        <p style="page-break-after: always"/>
        
        %endif
    %endfor
</body>
</html>
