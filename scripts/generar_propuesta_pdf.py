"""Renderiza la propuesta Markdown como PDF de dos páginas, sin duplicar su contenido."""
import re
import math
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]


def build():
    source = (ROOT / 'docs/03_negocio/PROPUESTA_TECNICA.md').read_text(encoding='utf-8')
    target = ROOT / 'outputs/entrega/Propuesta_CafeNorte_Aaron_Barrales.pdf'
    target.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyProposal', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=6, textColor=colors.HexColor('#263342')))
    styles['Title'].fontSize = 21
    styles['Title'].leading = 25
    styles['Title'].textColor = colors.HexColor('#173B42')
    styles['Heading2'].fontSize = 12
    styles['Heading2'].leading = 15
    styles['Heading2'].textColor = colors.HexColor('#173B42')
    styles.add(ParagraphStyle(name='CellProposal', parent=styles['BodyProposal'], fontSize=8, leading=10, spaceAfter=0))
    story = []

    def rich(text):
        value = escape(text)
        value = re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#176876">\1</link>', value)
        return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', value)

    # Mantengo un diagrama vectorial legible con las mismas relaciones de la propuesta.
    diagram = Drawing(480, 150)
    nodes = [(0, 110, 135, 'Archivos POS / ERP / Shopify'), (165, 110, 135, 'S3 originales privados'),
             (330, 110, 145, 'EventBridge + Step Functions'), (165, 57, 135, 'Lambda: validar + transformar'),
             (0, 4, 135, 'S3 excepciones / manifiestos'), (165, 4, 135, 'S3 Parquet + Glue Catalog'),
             (330, 4, 145, 'Athena > CSV / BI existente')]
    for x1,y1,x2,y2 in [(135,124,165,124),(232,110,232,85),(402,110,300,71),(232,57,232,32),(165,71,67,32),(300,18,330,18)]:
        diagram.add(Line(x1,y1,x2,y2,strokeColor=colors.HexColor('#829BA0'),strokeWidth=1))
        angle = math.atan2(y2-y1, x2-x1)
        points = [x2,y2,x2-6*math.cos(angle-0.4),y2-6*math.sin(angle-0.4),x2-6*math.cos(angle+0.4),y2-6*math.sin(angle+0.4)]
        diagram.add(Polygon(points, fillColor=colors.HexColor('#829BA0'), strokeColor=None))
    for x,y,w,label in nodes:
        diagram.add(Rect(x,y,w,28,rx=4,ry=4,fillColor=colors.HexColor('#EDF4F3'),strokeColor=colors.HexColor('#74969A')))
        diagram.add(String(x+w/2,y+11,label,fontName='Helvetica',fontSize=7,textAnchor='middle',fillColor=colors.HexColor('#173B42')))
    diagram.add(String(405,62,'CloudWatch: logs y alertas',fontSize=7,textAnchor='middle',fillColor=colors.HexColor('#49646B')))

    blocks = source.split('\n\n')
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith('```mermaid'):
            story += [diagram, Spacer(1, 6)]
        elif block.startswith('|'):
            rows = [[Paragraph(rich(c.strip()), styles['CellProposal']) for c in line.strip('|').split('|')]
                    for line in block.splitlines() if not re.match(r'^\|[-|: ]+\|$', line)]
            table = Table(rows, colWidths=[120, 305, 45], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDEAE8')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F6F7')]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOX',(0,0),(-1,-1),0.4,colors.HexColor('#CAD6DA')),('INNERGRID',(0,0),(-1,-1),0.3,colors.HexColor('#D7E0E2')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story += [table, Spacer(1, 7)]
        elif block.startswith('# '):
            story.append(Paragraph(rich(block[2:]), styles['Title']))
        elif block.startswith('## '):
            if block == '## Presupuesto mensual':
                story.append(PageBreak())
            story.append(Paragraph(rich(block[3:]), styles['Heading2']))
        else:
            story.append(Paragraph(rich(block), styles['BodyProposal']))

    def footer(canvas, doc):
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#657780'))
        canvas.drawString(48, 27, 'Aaron Barrales | CaféNorte | Propuesta técnica')
        canvas.drawRightString(A4[0]-48, 27, str(doc.page))

    SimpleDocTemplate(str(target), pagesize=A4, rightMargin=48, leftMargin=48, topMargin=36, bottomMargin=42,
                      title='CaféNorte: una base común para decidir', author='Aaron Barrales').build(story, onFirstPage=footer, onLaterPages=footer)
    print(target)


if __name__ == '__main__':
    build()
