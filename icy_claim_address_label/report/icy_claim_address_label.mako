<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<!--    <%page expression_filter="entity"/>
-->
    %for helpdesk in objects:
	    ${helpdesk.partner_id.name or ''}
	    <br/>
	    ${helpdesk.partner_id.street or ''}
	    <br/>
	    ${helpdesk.partner_id.zip  or ''} ${helpdesk.partner_id.city  or ''}
	    <br/>
	    <br/>
	    %if helpdesk.categ_id.image:
	    <img HEIGHT="14" src="data:image/img;base64,${helpdesk.categ_id.image}" />
	    %endif
    %endfor
</body>
</html>
