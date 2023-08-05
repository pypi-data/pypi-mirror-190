import re
import mkdocs
from mkdocs.config import config_options
from mkdocs.exceptions import ConfigurationError


class Plugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("mark", config_options.Type(str, default="type:video")),
        ("is_video", config_options.Type(bool, default=False)),
        ("video_type", config_options.Type(str, default="mp4")),
        ("video_muted", config_options.Type(bool, default=False)),
        ("video_loop", config_options.Type(bool, default=False)),
        ("video_controls", config_options.Type(bool, default=True)),
        ("video_autoplay", config_options.Type(bool, default=False)),
        ("css_style", config_options.Type(dict, default={
            "position": "relative",
            "width": "100%",
            "height": "22.172vw"
        }))
    )


    def on_page_content(self, html, page, config, files):
        # Separate tags by strings to simplify the use of regex
        content = html
        content = re.sub(r'>\s*<', '>\n<', content)

        tags = self.find_marked_tags(content)

        for tag in tags:
            src = self.get_tag_src(tag)
            if src is None:
                continue
            repl_tag = self.create_repl_tag(src)
            esc_tag = re.sub(r'\/', "\\\\/", tag)
            html = re.sub(esc_tag, repl_tag, html)

        return html


    def get_tag_src(self, tag):
        '''
        Get value of the src attribute

        return: str
        '''

        result = re.search(
            r'src=\"[^\s]*\"',
            tag
        )

        return result[0][5:-1] if result is not None else None


    def create_repl_tag(self, src):
        '''
        Сreate a replacement tag with the specified source and style.

        return: str
        '''

        style = self.config["css_style"]
        style = "; ".join(
            ["{}: {}".format(str(atr), str(style[atr])) for atr in style]
        )

        is_video = self.config["is_video"]
        video_loop = self.config["video_loop"]
        video_muted = self.config["video_muted"]
        video_controls = self.config["video_controls"]
        video_autoplay = self.config["video_autoplay"]
        video_type = self.config['video_type'].lower().strip()
        if " " in video_type or "/" in video_type:
            raise ConfigurationError("Unsupported video type")
        video_type = f"video/{video_type}"

        tag = (
            f'<video style="{style}"'
                f'{" loop" if video_loop else ""}'
                f'{" muted" if video_muted else ""}'
                f'{" controls" if video_controls else ""}'
                f'{" autoplay" if video_autoplay else ""}'
            '>'
                f'<source src="{src}" type="{video_type}" />'
            '</video>'
        ) if is_video else (
            f'<iframe src="{src}" style="{style}" frameborder="0"'
                'allowfullscreen>'
            '</iframe>'
        )

        return f'<div class="video-container">{tag}</div>'


    def find_marked_tags(self, content):
        '''
        Find image tag with marked alternative name

        return: list
        '''

        mark = self.config["mark"]

        return re.findall(
            r'<img alt="' + mark + '" src="[^\s]*"\s*\/>',
            content
        )
