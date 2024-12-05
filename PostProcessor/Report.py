from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, Paragraph, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

from PostProcessor import Tables
from PostProcessor.Plots import show_epuras_with_tabs

pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    "CenteredTitle1",
    parent=styles["Heading1"],
    fontName="Arial",
    fontSize=14,
    alignment=1,
    spaceAfter=12,
    textColor=colors.black
))

def generate_pdf(points_table, rods_table, calc_tables, scheme, input_data, self, output_file="output.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []

    def add_table(data, title, col_num, is_calc_table=False):
        elements.append(Spacer(1, 12))
        elements.append(Table([[title]], colWidths=[500], style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(Spacer(1, 12))

        if is_calc_table:
            headers = ["x", "N(x)", "U(x)", "σ(x)", "[σ]"]
            data.insert(0, headers)

        column_widths = [100] * col_num
        table = Table(data, colWidths=column_widths)

        styles = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]

        if is_calc_table:
            for row_idx, row in enumerate(data[1:], start=1):
                if abs(row[3]) > row[4]:
                    styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.red))
                    styles.append(('TEXTCOLOR', (0, row_idx), (-1, row_idx), colors.white))

        table.setStyle(TableStyle(styles))
        elements.append(table)
        elements.append(Spacer(1, 30))

    main_title = Paragraph("Результаты расчетов стержневой конструкции с заданными исходными параметрами и визуальный анализ", styles["CenteredTitle1"])
    elements.append(main_title)
    elements.append(Spacer(1, 20))

    add_table(points_table, "Таблица узлов", 3)
    add_table(rods_table, "Таблица стержней", 6)

    elements.append(PageBreak())

    scheme_title = Paragraph("Заданная конструкция", styles["CenteredTitle1"])
    elements.append(scheme_title)
    elements.append(Spacer(1, 12))

    img = Image(scheme, height=250, width=400)
    elements.append(img)

    table_title = Paragraph("Расчетные таблицы", styles["CenteredTitle1"])
    elements.append(table_title)

    for i, calc_table in enumerate(calc_tables, start=1):
        add_table(calc_table, f"Таблица {i}", 5, is_calc_table=True)

    epura_title = Paragraph("Полученные эпюры для конструкции", styles["CenteredTitle1"])
    elements.append(epura_title)
    elements.append(Spacer(1, 30))

    epura_images = show_epuras_with_tabs(self, input_data, need=False)

    for img_path in epura_images:
        epura_img = Image(img_path, height=250, width=400)
        elements.append(epura_img)
        elements.append(Spacer(1, 20))

    doc.build(elements)

    return output_file


def prepare_data(input_data):

    points = input_data["points"]
    rods = input_data["rods"]

    conc_loads = {int(item["point"]): item["val"] for item in input_data["point_loads"]}
    dist_loads = {int(item["rod"]): item["val"] for item in input_data["dist_loads"]}

    points_table = [["Узел", "S, м", "F, Па"]]
    for i, value in enumerate(points, start=1):
        points_table.append([i, value, conc_loads.get(i, "NaN")])

    rods_table = [["Узел 1", "Узел 2", "A", "E", "[σ], Па", "F, Па"]]
    for i, rod in enumerate(rods, start=1):
        rods_table.append([
            rod["point1"],
            rod["point2"],
            rod["a"],
            rod["e"],
            rod["sigma"],
            dist_loads.get(i, "NaN")
        ])

    calc_tables = Tables.prepare_tables(input_data, 10)

    return points_table, rods_table, calc_tables