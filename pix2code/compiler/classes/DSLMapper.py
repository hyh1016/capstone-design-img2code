import json

class DSLMapper:
    def __init__(self, class_group_path):
        with open(class_group_path) as style_file:
            self.styles = json.load(style_file)

        self.dsl_mapping = {}
        self.dsl_mapping["opening-tag"] = "{"
        self.dsl_mapping["closing-tag"] = "}"
        self.dsl_mapping["body"] = self.get_body()
        self.dsl_mapping["header"] = self.get_header()
        self.dsl_mapping["btn-active"] = self.get_btn_active()
        self.dsl_mapping["btn-inactive"] = self.get_btn_inactive()
        self.dsl_mapping["btn-red"] = self.get_btn_red()
        self.dsl_mapping["btn-orange"] = self.get_btn_orange()
        self.dsl_mapping["btn-yellow"] = self.get_btn_yellow()
        self.dsl_mapping["btn-green"] = self.get_btn_green()
        self.dsl_mapping["btn-purple"] = self.get_btn_purple()
        self.dsl_mapping["row"] = self.get_row()
        self.dsl_mapping["single"] = self.get_single()
        self.dsl_mapping["double"] = self.get_double()
        self.dsl_mapping["triple"] = self.get_triple()
        self.dsl_mapping["quadruple"] = self.get_quadruple()
        self.dsl_mapping["big-title"] = self.get_big_title()
        self.dsl_mapping["small-title"] = self.get_small_title()
        self.dsl_mapping["text"] = self.get_text()
    
    def get_body(self):
        pass
        return ('<html>\n'
                '<header>\n'
                    '<meta charset="utf-8">\n'
                    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                    '<style>\n'
                        # Define Global Stype Here
                        ' .header {margin:20px 0;}'
                        ' h2, h4, p {margin: 0.3rem 0;}'
                        ' p {font-size:14px;}'
                        ' .container {width:750px;padding: 0 15px;margin: 0 auto;}'
                        ' nav ul.nav-pills li {background-color:#333;border-radius:4px;margin-right:10px}'
                        ' .col-lg-3 {width:24%;margin-right:1.333333%}'
                        ' .col-lg-4 {width:33%;margin-right:0.5%}'
                        ' .col-lg-6 {width:49%;margin-right:2%}'
                        ' .col-lg-12, .col-lg-3, .col-lg-4, .col-lg-6 {margin-bottom:20px;border-radius:6px;background-color:#f5f5f5;padding:20px}'
                        ' .row .col-lg-3:last-child,.row .col-lg-6:last-child {margin-right:0}'
                        ' footer {padding:20px 0;text-align:center;border-top:1px solid #bbb}\n'
                    '</style>\n'
                    '<script src="https://cdn.tailwindcss.com"></script>\n'
                    '<title>Scaffold</title>\n'
                '</header>\n'
                '<body>\n'
                    '<main class="container">\n'
                    '{}\n'
                    '<footer class="footer">\n'
                    '<p>&copy; Tony Beltramelli 2017</p>\n'
                    '</footer>\n'
                    '</main>\n'
                '</body>\n'
                '</html>\n')
    
    def get_dsl_mapping(self):
        return self.dsl_mapping

    def get_header(self):
        nav = self.styles["nav"]
        return ('<div class="header clearfix">\n'
                    '<nav>\n'
                        f'<ul class="{nav}">\n'
                            '{}\n'
                        '</ul>\n'
                    '</nav>\n'
                '</div>\n')
    
    def get_btn_active(self):
        btn, btn_active = self.styles["btn"], self.styles["btn-active"]
        return f'<li class="active"><button class="{btn} {btn_active}">[]</button></li>\n'
    
    def get_btn_inactive(self):
        btn, btn_inactive = self.styles["btn"], self.styles["btn-inactive"]
        return f'<li><button class="{btn} {btn_inactive}">[]</button></li>\n'
    
    def get_btn_red(self):
        btn, btn_red = self.styles["btn"], self.styles["btn-red"]
        return f'<button class="{btn} {btn_red}">[]</button>\n'
    
    def get_btn_orange(self):
        btn, btn_orange = self.styles["btn"], self.styles["btn-orange"]
        return f'<button class="{btn} {btn_orange}">[]</button>\n'

    def get_btn_yellow(self):
        btn, btn_yellow = self.styles["btn"], self.styles["btn-yellow"]
        return f'<button class="{btn} {btn_yellow}">[]</button>\n'

    def get_btn_green(self):
        btn, btn_green = self.styles["btn"], self.styles["btn-green"]
        return f'<button class="{btn} {btn_green}">[]</button>\n'

    def get_btn_purple(self):
        btn, btn_purple = self.styles["btn"], self.styles["btn-purple"]
        return f'<button class="{btn} {btn_purple}">[]</button>\n'

    def get_row(self):
        row = self.styles["row"]
        return f'<div class="{row}">''{}''</div>\n'

    def get_single(self):
        single = self.styles["single"]
        return (f'<div class="{single}">\n'
                    '{}\n'
                '</div>\n')
    
    def get_double(self):
        double = self.styles["double"]
        return (f'<div class="{double}">\n'
                    '{}\n'
                '</div>\n')

    def get_triple(self):
            triple = self.styles["triple"]
            return (f'<div class="{triple}">\n'
                        '{}\n'
                    '</div>\n')

    def get_quadruple(self):
        quadruple = self.styles["quadruple"]
        return (f'<div class="{quadruple}">\n'
                    '{}\n'
                '</div>\n')

    def get_big_title(self):
        h2 = self.styles["h2"]
        return (f'<h2 class="{h2}">[]</h2>')

    def get_small_title(self):
        h4 = self.styles["h4"]
        return (f'<h4 class="{h4}">[]</h4>')
    
    def get_text(self):
        return '<p>[]</p>\n'
