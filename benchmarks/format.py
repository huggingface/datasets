import json
import sys


def format_json_to_md(input_json_file, output_md_file):
    with open(input_json_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    output_md = ["<details>", "<summary>Show updated benchmarks!</summary>", " "]

    for benchmark_name in sorted(results):

        benchmark_res = results[benchmark_name]

        benchmark_file_name = benchmark_name.split("/")[-1]
        output_md.append(f"### Benchmark: {benchmark_file_name}")

        title = "| metric |"
        lines = "|--------|"
        value = "| new / old (diff) |"
        for metric_name in sorted(benchmark_res):
            metric_vals = benchmark_res[metric_name]
            new_val = metric_vals["new"]
            old_val = metric_vals.get("old", None)
            dif_val = metric_vals.get("diff", None)

            val_str = " {:f}".format(new_val) if isinstance(new_val, (int, float)) else "None"

            if old_val is not None:
                val_str += " / {:f}".format(old_val) if isinstance(old_val, (int, float)) else "None"
            if dif_val is not None:
                val_str += " ({:f})".format(dif_val) if isinstance(dif_val, (int, float)) else "None"

            title += " " + metric_name + " |"
            lines += "---|"
            value += val_str + " |"

        output_md += [title, lines, value, " "]

    output_md.append("</details>")

    with open(output_md_file, "w", encoding="utf-8") as f:
        f.writelines("\n".join(output_md))


if __name__ == "__main__":
    input_json_file = sys.argv[1]
    output_md_file = sys.argv[2]

    format_json_to_md(input_json_file, output_md_file)
