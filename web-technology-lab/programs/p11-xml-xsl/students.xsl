<?xml version="1.0" encoding="UTF-8"?>
<!-- XSL style sheet: converts the XML data into an HTML table. -->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="/">
    <html>
      <head>
        <title>Student Records (XML + XSL)</title>
        <style>
          body { font-family: Arial, sans-serif; }
          h2 { color: #1f3864; }
          table { border-collapse: collapse; width: 70%; }
          th, td { border: 1px solid #333; padding: 6px; }
          th { background: #1f3864; color: #fff; }
          tr:nth-child(even) { background: #eef3f8; }
        </style>
      </head>
      <body>
        <h2>Student Records</h2>
        <table>
          <tr>
            <th>ID</th><th>Name</th><th>Roll No.</th>
            <th>Course</th><th>Marks</th>
          </tr>
          <xsl:for-each select="students/student">
            <tr>
              <td><xsl:value-of select="@id"/></td>
              <td><xsl:value-of select="name"/></td>
              <td><xsl:value-of select="roll"/></td>
              <td><xsl:value-of select="course"/></td>
              <td><xsl:value-of select="marks"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
