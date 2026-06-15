import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from screens import theme

class IosToggleButton(tk.Canvas):
    def __init__(self, parent, command=None, width=50, height=28, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.command = command
        self.is_on = False  
        
        self.width = width
        self.height = height
        
        # iOS 순정 색상 정의
        self.color_on = theme.PRIMARY   
        self.color_off = theme.GRAY_LIGHT  
        self.color_knob = theme.GHOST_BG 
        
        # 마우스 클릭 이벤트 바인딩
        self.bind("<Button-1>", self.toggle)
        
        # 이미지 가비지 컬렉션을 막기 위한 참조 변수
        self.rendered_image = None
        
        self.draw_widget()

    def draw_widget(self):
        self.delete("all")
        
        # 1. 4배율 고해상도로 캔버스 이미지 생성 (안티앨리어싱 핵심)
        scale = 4
        sw = self.width * scale
        sh = self.height * scale
        r = sh // 2  # 캡슐형 둥글기 반지름
        
        # 투명한 베이스 이미지 생성
        img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # ON/OFF 상태에 따른 배경색 결정
        bg_color = self.color_on if self.is_on else self.color_off
        
        # 2. 고해상도로 둥근 캡슐 배경 그리기
        draw.ellipse([0, 0, sh, sh], fill=bg_color)
        draw.ellipse([sw - sh, 0, sw, sh], fill=bg_color)
        draw.rectangle([r, 0, sw - r, sh], fill=bg_color)
        
        # 3. 고해상도로 흰색 원(Knob) 그리기
        padding = 2 * scale
        knob_size = sh - (padding * 2)
        
        if self.is_on:
            x1 = sw - sh + padding
        else:
            x1 = padding
            
        y1 = padding
        x2 = x1 + knob_size
        y2 = y1 + knob_size
        
        draw.ellipse([x1, y1, x2, y2], fill=self.color_knob)
        
        # 4. 이미지 크기를 다시 원래대로 축소 (LANCZOS 필터로 가장자리를 아주 부드럽게 뭉개줌)
        img_smooth = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        
        # 5. Tkinter Canvas에 그리기
        self.rendered_image = ImageTk.PhotoImage(img_smooth)
        self.create_image(0, 0, image=self.rendered_image, anchor="nw")

    def toggle(self, event=None):
        self.is_on = not self.is_on
        self.draw_widget()
        if self.command:
            self.command(self.is_on)
            
    def get_state(self):
        return self.is_on

    def set_state(self, state):
        self.is_on = state
        self.draw_widget()
