import json
import sys


def format_json_to_md(input_json_file, output_md_file):
    with open(input_json_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    output_md = []

    for benchmark_name, benchmark_res in results.items():

        benchmark_file_name = benchmark_name.split("/")[-1]
        output_md.append(f"## Benchmark: {benchmark_file_name}")

        title = "| metric |"
        lines = "|--------|"
        new = "| new    |"
        old = "| old    |"
        dif = "| diff   |"
        for metric_name in sorted(benchmark_res):
            metric_vals = benchmark_res[metric_name]
            new_val = metric_vals["new"]
            old_val = metric_vals["old"]
            dif_val = metric_vals.get("diff", None)
            new_val_str = " {:f} ".format(new_val) if isinstance(new_val, (int, float)) else "None"
            old_val_str = " {:f} ".format(old_val) if isinstance(old_val, (int, float)) else "None"
            dif_val_str = " {:f} ".format(dif_val) if isinstance(dif_val, (int, float)) else "None"

            title += " " + metric_name + " |"
            lines += "---|"
            new += new_val_str + "|"
            old += old_val_str + "|"
            dif += dif_val_str + "|"

        output_md += [title, lines, new, old, dif, " "]

    with open(output_md_file, "w", encoding="utf-8") as f:
        f.writelines("\n".join(output_md))


if __name__ == "__main__":
    input_json_file = sys.argv[1]
    output_md_file = sys.argv[2]

    format_json_to_md(input_json_file, output_md_file)
