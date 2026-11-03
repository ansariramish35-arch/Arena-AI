<?xml version="1.0" encoding="UTF-8"?>
<!-- books.xsl : XSL style sheet (XSLT 1.0). It transforms books.xml into a normal
HTML page so that the XML data can be displayed in a browser. -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="UTF-8"/>
<xsl:template match="/">
<html>
<head>
<title>Book Catalogue (XML + XSL)</title>
<style>
body { font-family:"Times New Roman"; margin:20px; background-color:#FFFFFF; }
h2 { color:#1F4E79; text-align:center; }
table { border-collapse:collapse; width:90%; margin:auto; }
th { background-color:#1F4E79; color:#FFFFFF; padding:7px; border:1px solid #000000; }
td { padding:6px; border:1px solid #999999; text-align:center; }
tr:nth-child(even) { background-color:#EAF1FA; }
.low { color:#0B6623; font-weight:bold; }
.high { color:#990000; font-weight:bold; }
p.note { text-align:center; font-size:13px; color:#666666; }
</style>
</head>
<body>
<h2>BOOK CATALOGUE - DISPLAYED THROUGH XSL</h2>
<table>
<tr><th>S. No.</th><th>Title</th><th>Author</th><th>Category</th><th>Year</th>
<th>Price (Rs.)</th></tr>
<!-- repeat the row for every <book>, sorted by title -->
<xsl:for-each select="catalogue/book">
<xsl:sort select="title" order="ascending" data-type="text"/>
<tr>
<td><xsl:value-of select="position()"/></td>
<td style="text-align:left;"><xsl:value-of select="title"/></td>
<td><xsl:value-of select="author"/></td>
<td><xsl:value-of select="@category"/></td>
<td><xsl:value-of select="year"/></td>
<!-- conditional formatting of the price with xsl:choose -->
<td><xsl:choose>
<xsl:when test="price &lt; 300"><span class="low"><xsl:value-of select="price"/></span></xsl:when>
<xsl:otherwise><span class="high"><xsl:value-of select="price"/></span></xsl:otherwise>
</xsl:choose></td>
</tr>
</xsl:for-each>
</table>
<p class="note">Total books : <xsl:value-of select="count(catalogue/book)"/>
&#160;|&#160; Generated from books.xml by books.xsl</p>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
