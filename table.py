import chevron


def write_table(*, data, state_list):
    with open("table.mustache", "r") as template:
        with open("docs/table.html", "w") as output:
            output.write(
                chevron.render(template, {"data": data, "all_states": state_list})
            )
            output.close()
        template.close()
