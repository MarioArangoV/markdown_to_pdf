from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from markdown import markdown
from bs4 import BeautifulSoup

# Función para convertir elementos HTML a elementos ReportLab
def parse_html_to_story(html_content, styles):
    soup = BeautifulSoup(html_content, 'html.parser')
    story = []

    for element in soup:
        if element.name == 'p':
            story.append(Paragraph(element.text, styles['Normal']))
            story.append(Spacer(1, 12))
        elif element.name == 'h1':
            story.append(Paragraph(element.text, styles['MyHeading1']))
            story.append(Spacer(1, 12))
        elif element.name == 'h2':
            story.append(Paragraph(element.text, styles['MyHeading2']))
            story.append(Spacer(1, 12))
        elif element.name == 'h3':
            story.append(Paragraph(element.text, styles['MyHeading3']))
            story.append(Spacer(1, 12))
        elif element.name == 'ul':
            items = [ListItem(Paragraph(li.text, styles['Normal']), bulletColor=colors.black) for li in element.find_all('li')]
            story.append(ListFlowable(items, bulletType='bullet'))
            story.append(Spacer(1, 12))
        elif element.name == 'ol':
            items = [ListItem(Paragraph(li.text, styles['Normal']), bulletColor=colors.black) for li in element.find_all('li')]
            story.append(ListFlowable(items, bulletType='1'))
            story.append(Spacer(1, 12))
        elif element.name == 'blockquote':
            story.append(Paragraph(element.text, styles['MyQuote']))
            story.append(Spacer(1, 12))
        # Puedes agregar más elif para manejar otros elementos como imágenes, tablas, etc.

    return story

# Leer archivo Markdown
with open('file.md', 'r', encoding='utf-8') as file:
    md_content = file.read()

# Convertir Markdown a HTML
html_content = markdown(md_content)

# Crear un documento PDF
pdf_file = 'output.pdf'
document = SimpleDocTemplate(pdf_file, pagesize=letter)
styles = getSampleStyleSheet()

# Crear nuevos estilos con nombres diferentes
styles.add(ParagraphStyle(name='MyHeading1', fontSize=24, leading=28, spaceAfter=12))
styles.add(ParagraphStyle(name='MyHeading2', fontSize=18, leading=22, spaceAfter=12))
styles.add(ParagraphStyle(name='MyHeading3', fontSize=14, leading=18, spaceAfter=12))
styles.add(ParagraphStyle(name='MyQuote', fontSize=12, leading=15, spaceBefore=12, spaceAfter=12, leftIndent=20, textColor=colors.grey))

# Parsear HTML y generar la historia del PDF
story = parse_html_to_story(html_content, styles)

# Construir el PDF
document.build(story)

print(f"PDF created successfully as '{pdf_file}'.")
