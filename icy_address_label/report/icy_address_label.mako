<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<!--    <%page expression_filter="entity"/>
-->
    %for partner in objects:
	    ${partner.name or ''}
	    <br/>
	    ${partner.street or ''}
	    <br/>
	    ${partner.zip  or ''} ${partner.city  or ''}
	    <br/>
	    <br/>
    %endfor
</body>
</html>
