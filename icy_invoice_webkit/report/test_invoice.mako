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
    margin-leftt: 50px; 
}
.footer1 {
    font-size: 12px;
    position: absolute;
    top: 50px;
}
.footer2 {
    font-size: 12px;
    position: absolute;
    top: 100px;
}
.footer3 {
    font-size: 12px;
    position: absolute;
    top: 150px;
}
.footer4 {
    font-size: 12px;
    position: absolute;
    top: 200px;
}
.footer5 {
    font-size: 12px;
    position: absolute;
    top: 250px;
}
.footer6 {
    font-size: 12px;
    position: absolute;
    top: 300px;
}
.footer7 {
    font-size: 12px;
    position: absolute;
    top: 350px;
}
.footer8 {
    font-size: 12px;
    position: absolute;
    top: 400px;
}
.footer9 {
    font-size: 12px;
    position: absolute;
    top: 450px;
}
.footer10 {
    font-size: 12px;
    position: absolute;
    top: 500px;
}
.footer11 {
    font-size: 12px;
    position: absolute;
    top: 550px;
}
.footer12 {
    font-size: 12px;
    position: absolute;
    top: 600px;
}
.footer13 {
    font-size: 12px;
    position: absolute;
    top: 650px;
}
.footer14 {
    font-size: 12px;
    position: absolute;
    top: 700px;
}
.footer15 {
    font-size: 12px;
    position: absolute;
    top: 750px;
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
    	return text.replace('0,', '')
    %>
    
    %for inv in objects:
    
    <div a class="footer1">
    test1
    </div>
    <div a class="footer2">
    test2
    </div>
    <div a class="footer3">
    test3
    </div>
    <div a class="footer4">
    test4
    </div>
    <div a class="footer5">
    test5
    </div>
    <div a class="footer6">
    test6
    </div>
    <div a class="footer7">
    test7
    </div>
    <div a class="footer8">
    test8
    </div>
    <div a class="footer9">
    test9
    </div>
    <div a class="footer10">
    test10
    </div>
    <div a class="footer11">
    test11
    </div>
    <div a class="footer12">
    test12
    </div>
    <div a class="footer13">
    test13
    </div>
    <div a class="footer14">
    test14
    </div>
    <div a class="footer15">
    test15
    </div>
    
    %endfor
</body>
</html>
