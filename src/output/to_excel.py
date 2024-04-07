import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment


def export_orders(
        i_data: list,
        i_columns: list,
        path: str,
        excel_name="all_orders.xlsx",
        sheet_name="order") -> str:
    db = pd.DataFrame(i_data, columns=i_columns, dtype=str)
    writer = pd.ExcelWriter(os.path.join(path, excel_name))
    db.to_excel(writer, sheet_name=sheet_name)
    worksheet = writer.sheets[sheet_name]
    writer._save()
    return excel_name


def append_table(rows: list, sheet_index: int = 0, interval: int = 1, path='./', file_name: str = "all_orders.xlsx"):
    excel_name = os.path.join(path, file_name)
    # 加载已存在的工作簿
    wb = load_workbook(excel_name)
    # 选择要追加数据的工作表，这里假设是第一个工作表
    ws = wb._sheets[sheet_index]
    # 获取当前工作表中的最大行数
    max_row = ws.max_row
    max_row += interval
    # 追加一行数据，注意行号是从1开始的，所以新行的行号是 max_row + 1
    for col_num, value in enumerate(rows, start=1):
        cell = ws.cell(row=max_row + 1, column=col_num, value=value)

        # 保存工作簿
    wb.save(excel_name)


def append_sheet_title(start: str, end: str, value: str = "", sheet_index: int = 0, path='./',
                       file_name: str = "all_orders.xlsx"):
    # 创建一个新的工作簿
    excel_name = os.path.join(path, file_name)
    # 加载已存在的工作簿
    wb = load_workbook(excel_name)
    # 选择要追加数据的工作表，这里假设是第一个工作表
    ws = wb._sheets[sheet_index]

    # 设置填充颜色为蓝色
    fill = PatternFill(start_color='709bfa', end_color='709bfa', fill_type='solid')
    # 合并单元格，从 A1 到 C2（跨3列，高2行）
    ws.merge_cells(f'{start}:{end}')
    # 选择合并后的单元格（合并后仍然可以通过左上角的单元格引用）
    merged_cell = ws[start]
    # 设置单元格填充颜色
    merged_cell.fill = fill
    # 设置文本内容
    merged_cell.value = value or '合并单元格文本'
    # 设置文本内容居中
    merged_cell.alignment = Alignment(horizontal='center', vertical='center')
    # 保存工作簿
    wb.save(excel_name)


if __name__ == '__main__':
    export_orders([1, 2, 3], ['column'], "./")

    # append_table([1, 2, 3])
    append_sheet_title("A1", "D1")
