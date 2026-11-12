"""Crea el PDF de estudio desde la guía Markdown, con capítulos y tablas legibles."""
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]


def build():
    source = (ROOT / 'docs/04_seguimiento/GUIA_ESTUDIO.md').read_text(encoding='utf-8')
    target = ROOT / 'outputs/entrega/Guia_estudio_CafeNorte_Aaron_Barrales.pdf'
    target.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='StudyBody', fontName='Helvetica', fontSize=10, leading=14.5, spaceAfter=10, textColor=colors.HexColor('#263342')))
    styles.add(ParagraphStyle(name='StudyCell', parent=styles['StudyBody'], fontSize=9, leading=12, spaceAfter=0))
    styles['Title'].textColor = colors.HexColor('#173B42')
    styles['Title'].fontSize = 23
    styles['Title'].leading = 28
    styles['Heading2'].textColor = colors.HexColor('#173B42')
    styles['Heading2'].fontSize = 16
    styles['Heading2'].leading = 20
    story, chapters = [], 0
    for block in source.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        if block.startswith('# '):
            story.append(Paragraph(escape(block[2:]), styles['Title']))
        elif block.startswith('## '):
            if chapters and block != '## Conclusión':
                story.append(PageBreak())
            story.append(Paragraph(escape(block[3:]), styles['Heading2']))
            chapters += 1
        elif block.startswith('|'):
            rows = [[Paragraph(escape(c.strip()), styles['StudyCell']) for c in line.strip('|').split('|')]
                    for line in block.splitlines() if not re.match(r'^\|[-|: ]+\|$', line)]
            table = Table(rows, colWidths=[150, 55, 285], repeatRows=1)
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDEAE8')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F6F7')]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('INNERGRID',(0,0),(-1,-1),0.3,colors.HexColor('#D7E0E2')),('BOX',(0,0),(-1,-1),0.4,colors.HexColor('#D7E0E2')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            story.extend([table, Spacer(1,10)])
        else:
            story.append(Paragraph(escape(block), styles['StudyBody']))

    def footer(canvas, doc):
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#657780'))
        canvas.drawString(46, 27, 'Aaron Barrales | CaféNorte | Guía de estudio')
        canvas.drawRightString(A4[0]-46, 27, str(doc.page))

    SimpleDocTemplate(str(target), pagesize=A4, leftMargin=46, rightMargin=46, topMargin=40, bottomMargin=44,
                      title='CaféNorte: guía de estudio y defensa técnica', author='Aaron Barrales').build(story, onFirstPage=footer, onLaterPages=footer)
    print(target)


if __name__ == '__main__':
    build()
