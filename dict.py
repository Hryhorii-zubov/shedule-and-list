import kivy

kivy.require('1.9.0') # Kivy ver where the code has been tested!
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, NoTransition, FadeTransition, FallOutTransition, RiseInTransition


import sqlite3
import json     

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.november_grid = GridLayout(cols=3, rows=12)
        self.december_grid = GridLayout(cols=3, rows=13)

        self.november_screen = Screen(name="11")
        self.december_screen = Screen(name="12")
        self.screen_first_part = Screen(name="first")
        self.screen_second_part = Screen(name="second")
        
        

        self.db = sqlite3.connect("dicts.db")

        self.sql = self.db.cursor()

        self.sql.execute("""CREATE TABLE IF NOT EXISTS dicts (
            november TEXT,
            december TEXT
        )""")

        self.db.commit()

        self.current_month = 11
        self.first_dict()

        for i in self.sql.execute("select november from dicts"):
            self.november = i[0]
        
        
        for i in self.sql.execute("select december from dicts"):
            self.december = i[0]
        
        self.november = json.loads(self.november.replace("'",'"'))
        self.buttons(self.november, self.november_grid, self.november_screen)
        self.december = json.loads(self.december.replace("'",'"'))
        self.buttons(self.december, self.december_grid, self.december_screen)


        self.sm.add_widget(self.november_screen)
        self.sm.add_widget(self.december_screen)
        self.sm.add_widget(self.screen_first_part)
        self.sm.add_widget(self.screen_second_part)
        
        
        size_of_text_of_textinput = 20
        self.first_screen_layout = FloatLayout()
        self.second_screen_layout = FloatLayout()

        self.text_input = TextInput(font_size=size_of_text_of_textinput, size_hint=(1, 0.1), pos_hint={"x": 0, "center_y": 0.95})
        self.text_input.bind(text=self.on_text)
        self.first_screen_layout.add_widget(self.text_input)

        size_of_label = 20
        self.label = Label(text="", font_size=size_of_label, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.first_screen_layout.add_widget(self.label)

        self.button_back = Button(text="Назад", size_hint=(0.5, 0.1))
        self.back_screen = None
        self.button_back.bind(on_press=self.back)

        self.first_screen_layout.add_widget(self.button_back)

        self.button_save = Button(text="Зберегти", size_hint=(0.5, 0.1), pos_hint = {"center_x": 0.75, "center_y": 0.05})
        self.button_save.bind(on_press=self.save)
        self.first_screen_layout.add_widget(self.button_save)

        self.screen_first_part.add_widget(self.first_screen_layout)


        self.button_back2 = Button(text="Назад", size_hint=(0.5, 0.1))
        self.back_screen = None
        self.button_back2.bind(on_press=self.back)

        self.second_screen_layout.add_widget(self.button_back2)

        self.button_list = Button(text="Записничок", size_hint=(0.5, 0.1), pos_hint = {"center_x": 0.75, "center_y": 0.05})
        self.back_screen = None
        self.button_list.bind(on_press=self.list)

        self.second_screen_layout.add_widget(self.button_list)

        size_of_label_shedule = 20
        self.label_shedule = Label(text="", font_size=size_of_label_shedule, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.second_screen_layout.add_widget(self.label_shedule)


        self.screen_second_part.add_widget(self.second_screen_layout)

        
        self.textt = ""
        self.number = ""
        self.before_letters = ""

        self.sm.current = "11"
        
        return self.sm
    
    
    
    def buttons(self, dict, grid, screen):
        
        size_of_names_of_month = 30

        if screen == self.november_screen:
            grid.add_widget(Label(text=""))
            grid.add_widget(Label(text="Листопад", size_hint=(0.5, 0.5), font_size=size_of_names_of_month))
            grid.add_widget(Label(text=""))

        elif screen == self.december_screen:
            grid.add_widget(Label(text=""))
            grid.add_widget(Label(text="Грудень", size_hint=(0.5, 0.5), font_size=size_of_names_of_month))
            grid.add_widget(Label(text=""))


        for key, value in dict.items():
            but = Button(text=f"""     {str(key)}
{value[0]}""")
            grid.add_widget(but)
            
            but.bind(on_press=self.first)
            
        
        if screen == self.december_screen:
            grid.add_widget(Button(text=""))
            grid.add_widget(Button(text=""))


        
        but = Button(text="Назад")
        grid.add_widget(but)
        but.bind(on_press=self.behind)
        grid.add_widget(Label(text=""))
        
        but = Button(text="Вперед")
        grid.add_widget(but)
        but.bind(on_press=self.next)

        screen.add_widget(grid)
    

    def next(self, d):
        try:
            self.current_month += 1
            self.sm.transition = SlideTransition(direction="left")
            self.sm.current = str(self.current_month)
        except:
            pass

    def behind(self, d):
        try:
            self.current_month -= 1
            self.sm.transition = SlideTransition(direction="right")
            self.sm.current = str(self.current_month)
        except:
            pass
    
    def list(self, d):
        self.sm.transition = SlideTransition(direction="left")
        self.sm.current = "first"
    
    def save(self, d):
        letters_on_screen = 50
        if self.back_screen == "11":
            num = -1
            text = ""
            for i in self.textt:
                if num == letters_on_screen:
                    text += "\n"
                    text += i
                    num = 0
                else:
                    text += i
                    num += 1
            self.november[self.number][1] = text
            self.label.text = self.november[self.number][1]
            
        elif self.back_screen == "12":
            num = -1
            text = ""
            for i in self.textt:
                if num == letters_on_screen:
                    text += "\n"
                    text += i
                    num = 0
                else:
                    text += i
                    num += 1
            self.december[self.number][1] = text
            self.label.text = self.december[self.number][1]
        
        if self.back_screen == "11":
            self.sql.execute(f'UPDATE dicts SET november = "{self.november}"')
            self.db.commit()
        if self.back_screen == "12":
            self.sql.execute(f'UPDATE dicts SET december = "{self.december}"')
            self.db.commit()

    def on_text(self, d, v):
        self.textt = d.text
        
    def back(self, d):
        self.text_input.text = ""
        self.text = ""
        self.number = ""
        self.label.text = ""
        self.label_shedule.text = ""
        
        self.sm.transition = FallOutTransition()
        self.sm.current = str(self.back_screen)
        
    def first(self, d):
        
        for i in d.text:
            try:
                self.number += str(int(i))
            except:
                pass
        
        self.back_screen = self.sm.current

        if self.back_screen == "11":
            self.label.text = self.november[self.number][1]
            self.text_input.text = self.november[self.number][1]

            if self.november[self.number][0] == "Понеділок":
                self.label_shedule.text = self.november[self.number][2]["Понеділок"][0]

        elif self.back_screen == "12":
            self.label.text = self.december[self.number][1]
            self.text_input.text = self.december[self.number][1]
        

        self.sm.transition = RiseInTransition()
        self.sm.current = "second"
        
    def first_dict(self):
        self.sql.execute("SELECT * FROM dicts")
        if self.sql.fetchone() == None:
            
            november = {}
            december = {}

            days_in_november = 30
            days_in_december = 31
            shedule_dict = {"Понеділок": ["Matem\nUrk_mova", ""], "Вівторок": ["", ""], "Середа": ["", ""], "Четвер": ["", ""], "Пятниця": ["", ""], "Субота": ["", ""]}
            month = [[november, days_in_november], [december, days_in_december]]
            
            days_in_week = ["Понеділок", "Вівторок", "Середа", "Четвер", "Пятниця", "Субота", "Неділя"]
            current_day = 1
            for m in month:
                i = 1
                while i <= m[1]:
                    m[0][str(i)] = [days_in_week[current_day], "", shedule_dict]
                    
                    i += 1
                    if current_day < 6:
                        current_day += 1
                    else:
                        current_day = 0


            self.sql.execute(f"INSERT INTO dicts VALUES (?, ?)", (str(november), str(december)))
            self.db.commit()

            """ for i in self.sql.execute("select november from dicts"):
                print(i) """

if __name__ == "__main__":
    MyApp().run()
