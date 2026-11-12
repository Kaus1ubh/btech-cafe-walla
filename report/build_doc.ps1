# report.html -> BTech_Cafe_Walla_Report.docx + .pdf via Word COM.
# Kept deliberately minimal: setting View.Type or PageBreakBefore over COM, or wrapping the
# calls in helper logging, left SaveAs2 hanging behind a hidden dialog on this machine.
# Page breaks come from <br style='page-break-before:always'> in the HTML.
$dir  = "A:\Programming\Projects\Uni\btech-cafe-walla\report"
python "$dir\prep.py"
$html = "$dir\report_word.html"
$tmp  = "$env:TEMP\btech-cafe-report"
New-Item -ItemType Directory -Force $tmp | Out-Null
$docx = "$tmp\BTech_Cafe_Walla_Report.docx"
$pdf  = "$tmp\BTech_Cafe_Walla_Report.pdf"

$w = New-Object -ComObject Word.Application
$w.Visible = $false; $w.DisplayAlerts = 0
$d = $w.Documents.Open($html, $false, $false)
foreach ($s in @($d.InlineShapes)) { if ($s.LinkFormat) { $s.LinkFormat.SavePictureWithDocument = $true; $s.LinkFormat.BreakLink() } }
$ps = $d.PageSetup; $ps.PaperSize = 7; $ps.TopMargin = 56; $ps.BottomMargin = 56; $ps.LeftMargin = 62; $ps.RightMargin = 62
$d.SaveAs2($docx, 16)
"docx saved"
$d.Close()
$d = $w.Documents.Open($docx)
$d.ExportAsFixedFormat($pdf, 17)
"pdf saved, pages: " + $d.ComputeStatistics(2)
$d.Close(); $w.Quit()
Copy-Item $docx, $pdf -Destination $dir -Force
"copied"
