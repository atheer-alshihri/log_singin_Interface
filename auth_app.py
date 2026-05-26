import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import re

# ─── قاعدة بيانات مؤقتة في الذاكرة ───────────────────────────
users_db = {}  # { email: { "name": ..., "password_hash": ... } }

# ─── مساعدات ──────────────────────────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def password_strength(password):
    score = 0
    if len(password) >= 6:
        score += 1
    if re.search(r"[A-Z]", password) or re.search(r"[0-9]", password):
        score += 1
    if len(password) >= 10 and re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    return score  # 0-3

# ─── الألوان والأنماط ──────────────────────────────────────────
BG       = "#1a1a2e"
BG2      = "#16213e"
BG3      = "#0f3460"
ACC      = "#e94560"
ACC2     = "#f5a623"
FG       = "#ffffff"
FG2      = "#aaaacc"
INP_BG   = "#1e2a45"
INP_FG   = "#ffffff"
FONT     = ("Segoe UI", 11)
FONT_LG  = ("Segoe UI", 14, "bold")
FONT_SM  = ("Segoe UI", 9)

# ─── النافذة الرئيسية ─────────────────────────────────────────
class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("نظام تسجيل الدخول")
        self.geometry("700x520")
        self.resizable(False, False)
        self.configure(bg=BG)

        # شريط جانبي
        self.sidebar = tk.Frame(self, bg=BG3, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="🔐", font=("Segoe UI", 32),
                 bg=BG3, fg=FG).pack(pady=(40, 8))
        tk.Label(self.sidebar, text="مرحباً بك!", font=FONT_LG,
                 bg=BG3, fg=FG).pack()
        tk.Label(self.sidebar, text="سجّل دخولك أو أنشئ\nحساباً جديداً للمتابعة",
                 font=FONT_SM, bg=BG3, fg=FG2, justify="center",
                 wraplength=160).pack(pady=10)

        # منطقة المحتوى
        self.content = tk.Frame(self, bg=BG2)
        self.content.pack(side="left", fill="both", expand=True)

        self._build_tabs()
        self.show_tab("login")

    # ─── التبويبات ────────────────────────────────────────────
    def _build_tabs(self):
        tab_bar = tk.Frame(self.content, bg=BG, pady=6)
        tab_bar.pack(fill="x", padx=20, pady=(20, 0))

        self.tab_btns = {}
        tabs = [("login", "تسجيل الدخول"),
                ("register", "حساب جديد"),
                ("forgot", "نسيت كلمة المرور")]

        for key, label in tabs:
            b = tk.Button(tab_bar, text=label, font=FONT_SM,
                          relief="flat", cursor="hand2",
                          command=lambda k=key: self.show_tab(k))
            b.pack(side="right", padx=3)
            self.tab_btns[key] = b

        self.panels = {}
        for key, _ in tabs:
            f = tk.Frame(self.content, bg=BG2)
            self.panels[key] = f
            getattr(self, f"_build_{key}")(f)

    def show_tab(self, name):
        for k, f in self.panels.items():
            f.pack_forget()
        self.panels[name].pack(fill="both", expand=True, padx=30, pady=10)

        for k, b in self.tab_btns.items():
            if k == name:
                b.configure(bg=ACC, fg=FG)
            else:
                b.configure(bg=BG, fg=FG2)

    # ─── مساعد حقول الإدخال ──────────────────────────────────
    def _field(self, parent, label_text, show=""):
        tk.Label(parent, text=label_text, font=FONT_SM,
                 bg=BG2, fg=FG2, anchor="e").pack(fill="x", pady=(6, 2))
        e = tk.Entry(parent, font=FONT, bg=INP_BG, fg=INP_FG,
                     insertbackground=FG, relief="flat",
                     show=show, bd=0)
        e.pack(fill="x", ipady=7)
        tk.Frame(parent, bg=ACC, height=1).pack(fill="x")
        return e

    def _msg_label(self, parent):
        lbl = tk.Label(parent, text="", font=FONT_SM,
                       bg=BG2, wraplength=380)
        lbl.pack(pady=(6, 0))
        return lbl

    def _show_msg(self, lbl, text, ok=True):
        lbl.configure(text=text,
                      fg="#2ed573" if ok else ACC)

    def _btn(self, parent, text, cmd):
        tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                  bg=ACC, fg=FG, relief="flat", cursor="hand2",
                  activebackground="#c73652", activeforeground=FG,
                  command=cmd, pady=8).pack(fill="x", pady=(14, 0))

    # ─── لوحة تسجيل الدخول ──────────────────────────────────
    def _build_login(self, f):
        tk.Label(f, text="تسجيل الدخول", font=FONT_LG,
                 bg=BG2, fg=FG).pack(pady=(10, 4))

        self.l_email = self._field(f, "البريد الإلكتروني")
        self.l_pass  = self._field(f, "كلمة المرور", show="•")

        row = tk.Frame(f, bg=BG2)
        row.pack(fill="x", pady=6)
        self.l_remember = tk.BooleanVar()
        tk.Checkbutton(row, text="تذكّرني", variable=self.l_remember,
                       bg=BG2, fg=FG2, selectcolor=BG,
                       activebackground=BG2, font=FONT_SM).pack(side="right")
        tk.Label(row, text="نسيت كلمة المرور؟", font=FONT_SM,
                 fg=ACC2, bg=BG2, cursor="hand2").pack(side="left")
        row.winfo_children()[-1].bind(
            "<Button-1>", lambda e: self.show_tab("forgot"))

        self.l_msg = self._msg_label(f)
        self._btn(f, "تسجيل الدخول", self._do_login)

        tk.Label(f, text="─── أو ───", font=FONT_SM,
                 fg=FG2, bg=BG2).pack(pady=8)
        row2 = tk.Frame(f, bg=BG2)
        row2.pack()
        for name in ["🌐  Google", "  GitHub"]:
            tk.Button(row2, text=name, font=FONT_SM, bg=INP_BG,
                      fg=FG2, relief="flat", cursor="hand2",
                      padx=14, pady=6,
                      command=lambda n=name: messagebox.showinfo(
                          "تسجيل الدخول", f"سيتم تطبيق {n} لاحقاً")).pack(
                side="right", padx=4)

    def _do_login(self):
        email = self.l_email.get().strip()
        pwd   = self.l_pass.get()
        if not email or not pwd:
            self._show_msg(self.l_msg, "⚠ يرجى تعبئة جميع الحقول", False)
            return
        if not is_valid_email(email):
            self._show_msg(self.l_msg, "⚠ البريد الإلكتروني غير صحيح", False)
            return
        if email not in users_db:
            self._show_msg(self.l_msg, "✗ البريد غير مسجّل", False)
            return
        if users_db[email]["password_hash"] != hash_password(pwd):
            self._show_msg(self.l_msg, "✗ كلمة المرور غير صحيحة", False)
            return
        name = users_db[email]["name"]
        self._show_msg(self.l_msg, f"✔ مرحباً {name}! تم تسجيل الدخول بنجاح 🎉")

    # ─── لوحة إنشاء الحساب ──────────────────────────────────
    def _build_register(self, f):
        tk.Label(f, text="إنشاء حساب جديد", font=FONT_LG,
                 bg=BG2, fg=FG).pack(pady=(10, 4))

        row = tk.Frame(f, bg=BG2)
        row.pack(fill="x")
        lf = tk.Frame(row, bg=BG2)
        lf.pack(side="right", fill="x", expand=True, padx=(4, 0))
        rf = tk.Frame(row, bg=BG2)
        rf.pack(side="right", fill="x", expand=True)

        tk.Label(lf, text="الاسم الأول", font=FONT_SM,
                 bg=BG2, fg=FG2).pack(anchor="e")
        self.r_fname = tk.Entry(lf, font=FONT, bg=INP_BG,
                                fg=INP_FG, insertbackground=FG, relief="flat")
        self.r_fname.pack(fill="x", ipady=6)
        tk.Frame(lf, bg=ACC, height=1).pack(fill="x")

        tk.Label(rf, text="الاسم الأخير", font=FONT_SM,
                 bg=BG2, fg=FG2).pack(anchor="e")
        self.r_lname = tk.Entry(rf, font=FONT, bg=INP_BG,
                                fg=INP_FG, insertbackground=FG, relief="flat")
        self.r_lname.pack(fill="x", ipady=6)
        tk.Frame(rf, bg=ACC, height=1).pack(fill="x")

        self.r_email = self._field(f, "البريد الإلكتروني")
        self.r_pass  = self._field(f, "كلمة المرور", show="•")
        self.r_pass.bind("<KeyRelease>", self._update_strength)

        # مؤشر قوة كلمة المرور
        srow = tk.Frame(f, bg=BG2)
        srow.pack(fill="x", pady=(3, 0))
        self.strength_bars = []
        for _ in range(3):
            b = tk.Frame(srow, bg=INP_BG, height=4, width=80)
            b.pack(side="right", padx=2)
            self.strength_bars.append(b)

        self.r_pass2 = self._field(f, "تأكيد كلمة المرور", show="•")

        self.r_terms = tk.BooleanVar()
        tk.Checkbutton(f, text="أوافق على الشروط والأحكام",
                       variable=self.r_terms,
                       bg=BG2, fg=FG2, selectcolor=BG,
                       activebackground=BG2, font=FONT_SM).pack(
            anchor="e", pady=4)

        self.r_msg = self._msg_label(f)
        self._btn(f, "إنشاء الحساب", self._do_register)

    def _update_strength(self, event=None):
        v = self.r_pass.get()
        s = password_strength(v)
        colors = ["#e94560", "#f5a623", "#2ed573"]
        for i, bar in enumerate(self.strength_bars):
            bar.configure(bg=colors[s - 1] if i < s else INP_BG)

    def _do_register(self):
        fname = self.r_fname.get().strip()
        lname = self.r_lname.get().strip()
        email = self.r_email.get().strip()
        pwd   = self.r_pass.get()
        pwd2  = self.r_pass2.get()
        terms = self.r_terms.get()

        if not fname or not email or not pwd or not pwd2:
            self._show_msg(self.r_msg, "⚠ يرجى تعبئة جميع الحقول", False)
            return
        if not is_valid_email(email):
            self._show_msg(self.r_msg, "⚠ البريد الإلكتروني غير صحيح", False)
            return
        if pwd != pwd2:
            self._show_msg(self.r_msg, "✗ كلمتا المرور غير متطابقتين", False)
            return
        if len(pwd) < 6:
            self._show_msg(self.r_msg, "⚠ كلمة المرور 6 أحرف على الأقل", False)
            return
        if not terms:
            self._show_msg(self.r_msg, "⚠ يجب الموافقة على الشروط والأحكام", False)
            return
        if email in users_db:
            self._show_msg(self.r_msg, "✗ هذا البريد مسجّل مسبقاً", False)
            return

        users_db[email] = {
            "name": f"{fname} {lname}",
            "password_hash": hash_password(pwd)
        }
        self._show_msg(self.r_msg, f"✔ تم إنشاء الحساب بنجاح! مرحباً {fname} 🎉")

    # ─── لوحة نسيان كلمة المرور ──────────────────────────────
    def _build_forgot(self, f):
        tk.Label(f, text="✉", font=("Segoe UI", 36),
                 bg=BG2, fg=ACC).pack(pady=(20, 4))
        tk.Label(f, text="استعادة كلمة المرور", font=FONT_LG,
                 bg=BG2, fg=FG).pack()
        tk.Label(f, text="أدخل بريدك الإلكتروني وسنرسل لك رابط الاستعادة",
                 font=FONT_SM, bg=BG2, fg=FG2).pack(pady=6)

        self.fo_email = self._field(f, "البريد الإلكتروني")
        self.fo_msg   = self._msg_label(f)
        self._btn(f, "إرسال رابط الاستعادة", self._do_forgot)

        tk.Label(f, text="تذكّرت كلمة المرور؟", font=FONT_SM,
                 fg=FG2, bg=BG2).pack(pady=(10, 0))
        tk.Label(f, text="ارجع لتسجيل الدخول", font=FONT_SM,
                 fg=ACC2, bg=BG2, cursor="hand2").pack()
        f.winfo_children()[-1].bind(
            "<Button-1>", lambda e: self.show_tab("login"))

    def _do_forgot(self):
        email = self.fo_email.get().strip()
        if not email or not is_valid_email(email):
            self._show_msg(self.fo_msg, "⚠ يرجى إدخال بريد إلكتروني صحيح", False)
            return
        self._show_msg(self.fo_msg,
                       f"✔ تم إرسال رابط الاستعادة إلى {email} ✉️")

# ─── تشغيل التطبيق ────────────────────────────────────────────
if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
