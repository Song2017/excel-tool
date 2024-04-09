from src.db.db_query import execute_query
import json
from src.output.to_excel import export_excel, append_sheet_title, get_excel_range


def loader() -> dict:
    with open("./src/data/conf.json") as f:
        conf = json.loads(f.read())
    return conf


def main():
    conf = loader()
    file_name = "./dev.xlsx"
    # sheet
    for k, v in conf.items():
        if not k.startswith("sheet"):
            continue
        sheet_index = int(k.split()[1]) - 1
        export_excel([""], [""], sheet_name=v.get('name'), file_path=file_name)
        # period
        period = v.get('period')
        er = get_excel_range(period["base_line"], period["height"], period["column"])
        append_sheet_title(er[0], er[1], value=period.get("name"),
                           file_path=file_name, sheet_index=sheet_index)
        # groups
        for key in v.keys():
            if not key.startswith("group"):
                continue
            gp = v.get(key)
            gp_base_line = gp["base_line"]
            er = get_excel_range(gp["base_line"], gp["height"], gp["column"])
            append_sheet_title(er[0], er[1], value=gp.get("name"),
                               file_path=file_name, sheet_index=sheet_index, font_size=16)
            # table
            for t_key in gp.keys():
                if not t_key.startswith("table"):
                    continue
                t = gp.get(t_key)
                er = get_excel_range(t["inc_line"]+gp_base_line, t["height"], t["column"])
                append_sheet_title(er[0], er[1], value=t.get("name"),
                                   file_path=file_name, sheet_index=sheet_index)
                # head
                head = t.get('head')



    # rows = execute_query("", {})


if __name__ == '__main__':
    main()
