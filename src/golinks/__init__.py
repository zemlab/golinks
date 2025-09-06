import os

import yaml
from jinja2 import Environment, select_autoescape

CONFIG_TEMPLATE = """
server {
    listen       80;
    server_name  _;

    root   /usr/share/nginx/html;
    index  index.html index.htm;

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    {% for redirect in redirects %}
    location {{redirect.from}} {
        return 301 {{redirect.to}};
    }
    {% endfor %}
}
"""


class Golinks:
    def __init__(self, configfile, outputdir) -> None:
        self.configfile = configfile
        self.outputdir = outputdir
        self.load_config()
        self.generate_nginx_config()

    def load_config(self) -> None:

        with open(self.configfile, "r") as f:
            self.config = yaml.safe_load(f)

    def generate_nginx_config(self) -> None:
        redirects = self.config.get("redirects", [])
        env = Environment(autoescape=select_autoescape())
        template = env.from_string(CONFIG_TEMPLATE)
        output = template.render(redirects=redirects)
        with open(self.outputdir, "w") as outputfile:
            outputfile.write(output)


def main() -> None:
    if "GOLINKS_CONFIG" not in os.environ:
        raise RuntimeError("GOLINKS_CONFIG environment variable is not set")
    if "GOLINKS_OUTPUT" not in os.environ:
        raise RuntimeError("GOLINKS_OUTPUT environment variable is not set")
    configfile = os.environ.get("GOLINKS_CONFIG")
    outputdir = os.environ.get("GOLINKS_OUTPUT")
    golinks = Golinks(configfile, outputdir)
