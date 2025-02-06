import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class BlackjackCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("21点算牌助手 v1.3")
        self.root.geometry("680x380")  # 稍微增加窗口高度

        # 颜色配置
        self.btn_colors = {
            "low": "#90EE90",  # 浅绿色
            "neutral": "#F0E68C",  # 卡其色
            "high": "#FFB6C1"  # 浅粉色
        }

        # 初始化参数
        self.total_decks = 6
        self.cards_per_deck = 52
        self.used_cards = 0
        self.running_count = 0

        # 创建主容器
        main_container = tk.Frame(root, bd=0)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 操作区框架（宽度占比60%）
        self.control_frame = tk.Frame(main_container, padx=10, width=400)
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # 分隔线
        sep = tk.Canvas(main_container, width=2, bg="#808080")
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        sep.create_line(0, 0, 0, 380, fill="gray")

        # 帮助区框架（宽度占比40%）
        self.help_frame = tk.Frame(main_container, width=260, bg="#F5F5F5")
        self.help_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # 初始化组件
        self.create_control_panel()  # 确保方法已定义
        self.create_help_panel()
        self.update_displays()

    def create_control_panel(self):
        """操作面板"""
        # 数据显示区
        display_frame = tk.Frame(self.control_frame)
        display_frame.pack(pady=10)

        self.lbl_running = tk.Label(display_frame, text="流水数：0",
                                    font=("微软雅黑", 12), width=12)
        self.lbl_running.grid(row=0, column=0)

        self.lbl_true_count = tk.Label(display_frame, text="真数：0.0",
                                       font=("微软雅黑", 12), width=12)
        self.lbl_true_count.grid(row=1, column=0)

        self.lbl_remaining = tk.Label(display_frame, text="剩余牌副：6.0",
                                      font=("微软雅黑", 12), width=12)
        self.lbl_remaining.grid(row=2, column=0)

        # 建议标签
        self.lbl_advice = tk.Label(self.control_frame, text="建议：最小注",
                                   font=("微软雅黑", 12, "bold"), fg="#2E8B57")
        self.lbl_advice.pack(pady=5)

        # 操作按钮
        btn_frame = tk.Frame(self.control_frame)
        btn_frame.pack(pady=10)

        self.btn_low = tk.Button(btn_frame, text="2-6 (+1)", width=8,
                                 bg=self.btn_colors["low"], relief=tk.GROOVE,
                                 command=lambda: self.update_count(1))
        self.btn_low.grid(row=0, column=0, padx=3)

        self.btn_neutral = tk.Button(btn_frame, text="7-9 (0)", width=8,
                                     bg=self.btn_colors["neutral"], relief=tk.GROOVE,
                                     command=lambda: self.update_count(0))
        self.btn_neutral.grid(row=0, column=1, padx=3)

        self.btn_high = tk.Button(btn_frame, text="10-A (-1)", width=8,
                                  bg=self.btn_colors["high"], relief=tk.GROOVE,
                                  command=lambda: self.update_count(-1))
        self.btn_high.grid(row=0, column=2, padx=3)

        # 控制按钮
        ctrl_frame = tk.Frame(self.control_frame)
        ctrl_frame.pack(pady=10)

        self.btn_reset = tk.Button(ctrl_frame, text="重置", width=8,
                                   relief=tk.GROOVE, command=self.reset_count)
        self.btn_reset.grid(row=0, column=0, padx=5)

        self.btn_set_decks = tk.Button(ctrl_frame, text="设置牌副", width=8,
                                       relief=tk.GROOVE, command=self.set_deck_count)
        self.btn_set_decks.grid(row=0, column=1, padx=5)

    def create_help_panel(self):
        """帮助面板（无需滚动）"""
        # 标题
        lbl_title = tk.Label(self.help_frame, text="实时帮助说明",
                             font=("微软雅黑", 11, "bold"), bg="#F5F5F5")
        lbl_title.pack(pady=5)

        # 紧凑型帮助内容
        help_text = """
1. 根据发牌点击对应按钮：
   → 2-6点：点击+1按钮
   → 7-9点：点击0按钮
   → 10/J/Q/K/A：点击-1按钮

2. 点击[重置]开始新牌局
3. 点击[设置牌副]修改总牌数

【核心算法】
真数 = 流水数 / 剩余牌副数
剩余牌数 = 总牌数 - 已用牌数
总牌数 = 牌副数 × 52

【下注策略】
● 真数≤0 → 最小注
● 1-2 → 基础注
● 2-5 → 2^(真数)倍注
● ≥5 → 最大注
"""
        # 使用Text组件实现紧凑排版
        help_box = tk.Text(self.help_frame, bg="#F5F5F5", wrap=tk.WORD,
                           font=("微软雅黑", 9), padx=5, pady=5,
                           height=22, width=32, relief=tk.FLAT)
        help_box.insert(tk.END, help_text)
        help_box.config(state=tk.DISABLED)  # 禁止编辑
        help_box.pack(pady=5)

    def calculate_true_count(self):
        """计算真数"""
        remaining_cards = (self.total_decks * self.cards_per_deck) - self.used_cards
        remaining_decks = remaining_cards / self.cards_per_deck
        return self.running_count / remaining_decks if remaining_decks > 0 else 0

    def update_count(self, value):
        """更新计数"""
        self.running_count += value
        self.used_cards += 1
        self.update_displays()

    def update_displays(self):
        """更新所有显示"""
        # 计算剩余牌副数
        remaining_cards = (self.total_decks * self.cards_per_deck) - self.used_cards
        remaining_decks = round(remaining_cards / self.cards_per_deck, 1)

        # 计算真数
        true_count = round(self.calculate_true_count(), 1)

        # 更新显示
        self.lbl_running.config(text=f"流水数：{self.running_count}")
        self.lbl_true_count.config(text=f"真数：{true_count}")
        self.lbl_remaining.config(text=f"剩余牌副：{remaining_decks}")

        # 更新策略建议
        advice, color = self.get_strategy_advice(true_count)
        self.lbl_advice.config(text=f"建议：{advice}", fg=color)

    def get_strategy_advice(self, true_count):
        """根据真数获取策略建议"""
        if true_count <= 0:
            return "最小注（无优势）", "red"
        elif 1 <= true_count < 2:
            return "基础注（观察）", "orange"
        elif 2 <= true_count < 5:
            bet = 2 ** (int(true_count) - 1)
            return f"下注 {bet}倍 基础注", "green"
        else:
            return "最大注（高优势）", "darkgreen"

    def reset_count(self):
        """重置所有计数"""
        self.running_count = 0
        self.used_cards = 0
        self.update_displays()
        messagebox.showinfo("重置成功", "所有计数已重置！")

    def set_deck_count(self):
        """设置牌副数"""
        try:
            new_decks = simpledialog.askinteger("设置牌副数", "请输入总牌副数（n）：",
                                                minvalue=1, maxvalue=20, initialvalue=self.total_decks)
            if new_decks is not None:  # 用户未取消输入
                self.total_decks = new_decks
                self.used_cards = 0  # 重置已用牌数
                self.running_count = 0  # 重置流水数
                self.update_displays()
                messagebox.showinfo("设置成功", f"总牌副数已设置为 {self.total_decks} 副！")
        except Exception as e:
            messagebox.showerror("错误", f"输入无效：{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackCounterApp(root)
    root.mainloop()