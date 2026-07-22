import random
import ast
import operator as op
import math

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

# ================= WINDOW =================
Window.clearcolor = (0, 0, 0, 1)

# ================= OPERATORS =================
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
    ast.UAdd: op.pos
}

# ================= SAFE CALCULATOR ENGINE =================
def safe_calculate(expression):
    try:
        if not expression or not expression.strip():
            return ""

        clean_expr = expression.strip()

        if len(clean_expr) > 50:
            return "TOO LONG"

        allowed_chars = "0123456789+-*/(). "
        for char in clean_expr:
            if char not in allowed_chars:
                return "ERROR"

        tree = ast.parse(clean_expr, mode="eval").body

        def calculate(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    if not math.isfinite(node.value):
                        raise ValueError
                    return node.value
                raise ValueError

            elif isinstance(node, ast.BinOp):
                left = calculate(node.left)
                right = calculate(node.right)

                operator_type = type(node.op)
                if operator_type not in OPERATORS:
                    raise ValueError

                if operator_type == ast.Div:
                    if right == 0 or not math.isfinite(right):
                        raise ZeroDivisionError

                result = OPERATORS[operator_type](left, right)
                if not math.isfinite(result):
                    raise ValueError
                return result

            elif isinstance(node, ast.UnaryOp):
                operand = calculate(node.operand)
                operator_type = type(node.op)

                if operator_type not in OPERATORS:
                    raise ValueError

                result = OPERATORS[operator_type](operand)
                if not math.isfinite(result):
                    raise ValueError
                return result

            raise ValueError

        res = calculate(tree)
        
        if isinstance(res, float) and res.is_integer():
            return int(res)
            
        return round(res, 6) if isinstance(res, float) else res

    except ZeroDivisionError:
        return "DIV_BY_ZERO"
    except Exception:
        return "ERROR"


class HackerCalculatorApp(App):

    def build(self):
        root = FloatLayout()

        # ==========================================
        # 1. MATRIX RAIN BACKDROP (Running Text Mode)
        # ==========================================
        self.bg_label = Label(
            text="",
            color=(0, 1, 0, 0.16), 
            font_size="13sp",
            font_name="Roboto", 
            halign="left",
            valign="top",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        self.bg_label.bind(size=lambda instance, size: setattr(instance, 'text_size', size))
        root.add_widget(self.bg_label)

        self.matrix_rows = [""] * 45
        Clock.schedule_interval(self.update_matrix, 0.20)

        # ==========================================
        # 2. CYBER GLITCH SYSTEM HEADER BANNER
        # ==========================================
        self.base_header_text = "SYSTEM ACTIVE: WELCOME MR. SNEHASISH"
        self.welcome_banner = Label(
            text=f"[ {self.base_header_text} ]",
            color=(0, 1, 0.4, 0.95),
            font_size="16sp",
            font_name="Roboto",
            bold=True,
            size_hint=(1, 0.06), 
            pos_hint={"x": 0, "top": 0.95} 
        )
        root.add_widget(self.welcome_banner)
        
        Clock.schedule_interval(self.trigger_text_glitch, 0.12)

        # ==========================================
        # 3. INTERACTIVE CALCULATOR ENGINE UI
        # ==========================================
        calc_layout = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=12,
            size_hint=(0.95, 0.70), 
            pos_hint={"center_x": 0.5, "center_y": 0.35} 
        )

        self.display = TextInput(
            font_size="36sp",
            halign="right",
            multiline=False,
            readonly=True,
            background_normal="", 
            background_active="", 
            background_color=(0, 0.05, 0, 0.7), 
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            size_hint_y=0.18
        )
        calc_layout.add_widget(self.display)

        buttons_layout = GridLayout(cols=4, spacing=8, size_hint_y=0.82)
        buttons = [
            "(", ")", "C", "/",
            "7", "8", "9", "*",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "0", ".", "<-", "="
        ]

        for button_text in buttons:
            if button_text in ["/", "*", "-", "+", "=", "(", ")"]:
                btn_bg = (0, 0.22, 0.12, 0.85)
                text_color = (0.3, 1, 0.7, 1)
            elif button_text == "C":
                btn_bg = (0.28, 0, 0.06, 0.9)
                text_color = (1, 0.3, 0.4, 1)
            elif button_text == "<-":
                btn_bg = (0.2, 0.14, 0, 0.9) 
                text_color = (1, 0.8, 0.2, 1)
            else:
                btn_bg = (0, 0.10, 0.03, 0.9)
                text_color = (0, 1, 0.2, 1)

            btn = Button(
                text=button_text,
                font_size="26sp",
                background_normal="",
                background_color=btn_bg,
                color=text_color
            )
            btn.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(btn)

        calc_layout.add_widget(buttons_layout)
        root.add_widget(calc_layout)

        return root

    def trigger_text_glitch(self, dt):
        try:
            if random.random() > 0.82:
                glitch_chars = ["_", "#", "█", "Ø", "▲", "*", "%", "$", "!", "X", "7"]
                modified_text = list(self.base_header_text)
                
                for _ in range(random.randint(1, 3)):
                    idx = random.randint(0, len(modified_text) - 1)
                    if modified_text[idx] != " ":
                        modified_text[idx] = random.choice(glitch_chars)
                        
                self.welcome_banner.text = f"[ {''.join(modified_text)} ]"
                self.welcome_banner.color = (0.2, 1, 0.6, 1)
            else:
                self.welcome_banner.text = f"[ {self.base_header_text} ]"
                self.welcome_banner.color = (0, 1, 0.4, 0.95)
        except Exception:
            pass

    def update_matrix(self, dt):
        try:
            line_parts = []
            for _ in range(5):
                line_parts.append("".join(random.choices(["0", "1", " ", " "], k=4)))

            if random.random() > 0.65:
                pos = random.randint(0, len(line_parts))
                line_parts.insert(pos, " WELCOME MR. SNEHASISH ")

            new_row = "  ".join(line_parts)
            self.matrix_rows.insert(0, new_row)
            self.matrix_rows = self.matrix_rows[:45]
            self.bg_label.text = "\n".join(self.matrix_rows)
        except Exception:
            pass

    def on_button_press(self, instance):
        try:
            button_text = instance.text

            if self.display.text in ["ERROR", "DIV_BY_ZERO", "TOO LONG"]:
                self.display.text = ""

            if button_text == "C":
                self.display.text = ""

            elif button_text == "<-":
                current_text = str(self.display.text)
                if current_text:
                    self.display.text = current_text[:-1]

            elif button_text == "=":
                if self.display.text:
                    result = safe_calculate(self.display.text)
                    self.display.text = str(result)
            else:
                if len(self.display.text) < 24:
                    self.display.text += button_text
        except Exception:
            self.display.text = ""


if __name__ == "__main__":
    HackerCalculatorApp().run()
