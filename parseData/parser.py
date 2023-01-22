from ttp import ttp
from ttp_templates import get_template

def load_ttp(command: str) -> ttp:
    template = get_template(platform="cisco_xr", command=command)
    return ttp(template=template)


def parse_ttp(parser: ttp, cli_output: str, format: str):
    parser.set_input(cli_output)
    parser.parse()
    return parser.result(format=format)[0]


