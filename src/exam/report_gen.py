import io
from django.http import FileResponse
from exam.models import Exam
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.platypus.tables import TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT


def test(request, id):
    exam = Exam.objects.get(id=id)
    pdf = io.BytesIO()

    doc = SimpleDocTemplate(pdf, pagesize=letter)

    story = []
    styles = getSampleStyleSheet()
    # Header
    styles.add(ParagraphStyle(name='Normal_CENTER',
                              parent=styles['Normal'],
                              fontName='Helvetica-Bold',
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=20,
                              leading=13,
                              textColor=colors.black,
                              borderPadding=0,
                              leftIndent=0,
                              rightIndent=0,
                              spaceAfter=0,
                              spaceBefore=0,
                              splitLongWords=True,
                              spaceShrinkage=0.05,
                              ))
    header = Paragraph(
        'Akshara International School\n\n'.replace("\n", "<br />"), styles['Normal_CENTER'])
    story.append(header)
    # Report card
    styles.add(ParagraphStyle(name='Normal_repo',
                              parent=styles['Normal'],
                              fontName='Helvetica',
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=15,
                              leading=13,
                              textColor=colors.black,
                              borderPadding=0,
                              leftIndent=0,
                              rightIndent=0,
                              spaceAfter=0,
                              spaceBefore=0,
                              splitLongWords=True,
                              spaceShrinkage=0.05,
                              ))
    header = Paragraph(
        'Report Card - '+exam.Name+'\n\n\n\n'.replace("\n", "<br />"), styles['Normal_repo'])
    story.append(header)

    # Student Details
    details = [
        ['Name:', request.user.get_full_name()],
        ['Date of Birth:', request.user.Student.dob.strftime('%d %b, %Y')],
        ['Class:', request.user.Student.Class.name],
        ['Contact:', request.user.Student.Contact],
    ]
    taa = Table(details, hAlign='LEFT')
    taa.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(taa)

    story.append(Paragraph('\n\n'.replace(
        "\n", "<br />"), styles['Normal_repo']))

    # Marks
    data = [['Subject', 'Pass Marks', 'Max Marks', 'Obtained Marks'], ]
    obtained = 0
    maxx = 0
    for x in exam.Paper.all():
        obtained += x.StudentPaper.filter(
            Student=request.user.Student)[0].Marks
        maxx += x.Max_Marks
        data.append([x.Subject.Name, x.Pass_Marks, x.Max_Marks, x.StudentPaper.filter(
            Student=request.user.Student)[0].Marks])

    t = Table(data, colWidths=[120, 120])

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ]))

    story.append(t)

    # Percentage
    styles.add(ParagraphStyle(name='Normal_perc',
                              parent=styles['Normal'],
                              fontName='Helvetica-Bold',
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              leading=13,
                              textColor=colors.black,
                              borderPadding=0,
                              leftIndent=0,
                              rightIndent=1,
                              spaceAfter=0,
                              spaceBefore=0,
                              splitLongWords=True,
                              spaceShrinkage=0.05,
                              ))
    story.append(Paragraph('\n\n\n'.replace(
        "\n", "<br />"), styles['Normal_perc']))
    story.append(Paragraph('Percentage: '+str((obtained/maxx)*100)+"%".replace(
        "\n", "<br />"), styles['Normal_perc']))

    doc.build(story)
    pdf.seek(0)

    return FileResponse(pdf, as_attachment=True, filename='hello.pdf')
