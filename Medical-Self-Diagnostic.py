from kivy.app import App
from kivy.core.window._window_sdl2 import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
import sklearn
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pandas as pd
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
import numpy as np
import mysql.connector
import mysql
import webbrowser
from sklearn.metrics import classification_report, confusion_matrix

from kivy.core.window import Window
Window.size = (360, 680)

Builder.load_file("Medical Self-Diagnostic.kv")




mydb =mysql.connector.Connect(
    host="localhost",
    user="root",
    password="root1234567",
    database="user_inf"
 )


cur = mydb.cursor()



#
class ScreenManagement(ScreenManager):
     pass

class LoginWindow(Screen):

        def Login_pressed(self):
            username_text = self.username_input.text
            password_text = self.password_input.text



            cur.execute(
                "SELECT username,pass FROM user WHERE username='" + username_text + "' AND pass ='" + password_text + "'")
            count = cur.fetchone()

            if count is None:
                self.ids.error_1.text = Label(text=" Enter a valid username and password").text


            else:
                self.parent.current='screen_1'




class Register(Screen):
    def register_pressed(self):

        username_text = self.username_input.text
        email_text = self.email_input.text
        conf_email = self.con_email.text
        password_text = self.password_input.text


        cur.execute("SELECT * FROM user WHERE username='" + username_text + "'")
        count = cur.fetchone()


        if count is not None:
            self.ids.error.text = Label(text=" Username is already exists").text

        elif len(username_text) < 8:
            self.ids.error.text = Label(text=" Username must be at least 8 characters").text

        elif not username_text or not email_text or not password_text:
            self.ids.error.text = Label(text="Must fill all blank").text


        elif len(password_text) < 8:
            self.ids.error.text = Label(text="password must have more 8 character").text

        elif email_text != conf_email:
            self.ids.error.text = Label(text="invalid email" ).text


        else:
            cur.execute(
                "INSERT INTO user (username, email, pass) VALUES('" + username_text + "' , '" + email_text + "', '" + password_text + "')"
            )

            self.parent.current = 'screen_1'

            mydb.commit()
            cur.close()
            mydb.close()
        return Register()

#
new_arr_symp = []
symp_arr = []

class FirstScreen(Screen):
    def select(self):

        self.ids.sym_text.bind(text=self.spinner_clicked + self.touch_multiselect)

    def spinner_clicked(self, Spinner):

        self.sym_label = Label(text=" ")
        self.ids.sym_label.text = (
            self.ids.sym_label.text + "\n " + " %s " % self.ids.sym_text.text
        )

    def delete_button(self):
        self.ids.sym_label.text = "  "

    def encoding(self):
        global new_arr_symp
        for i in self.ids.sym_text.values:
            if i in self.ids.sym_label.text:
                symp_arr.append(1)
            else:
                symp_arr.append(0)


class Screen_1(Screen):
    Question_1= 0
    Question_24 = 0
    Question_25 = 0
    Question_2 = 0
    Question_3 = 0
    Question_4 = 0
    def traslate(self, text):


        if text == "Yes":
                return 1
        elif text == "No":
                return 0


    def add_results(self):
        global new_arr_symp

        # age
        textinput_age = self.tinput_age.text
        Question_1 = int(textinput_age)

        #Number of sexual partners per month
        textinput_24 = self.tinput_24.text
        if textinput_24:
            Question_24 = int(textinput_24)
        else:
            Question_24 = 0

            #First sexual intercourse
        textinput_25 = self.tinput_25.text
        if textinput_25:
            Question_25 = int(textinput_25)
        else:
            Question_25 = 0

        #number of pregnancies
        textinput_preg = self.tinput_preg.text
        Question_2 = int(textinput_preg)

            # Are you smoking
        Question_3 = self.traslate(self.Question_3)


            # how many year you smoke
        textinput_4 = self.tinput_year.text
        if textinput_4:
            Question_4 = int(textinput_4)
        else:
            Question_4 = 0

        new_arr_symp = new_arr_symp +[
            Question_1,
            Question_24,
            Question_25,
            Question_2,
            Question_3,
            Question_4,
            ]
        if Question_3 == 1 or Question_3 == 0:
            self.manager.current = 'screen_2'
        else:
            self.ids.error_1.text = Label(text="Must select one 'yes' or 'no'").text



class Screen_2(Screen):
    Question_5 = 0
    Question_6 = 0
    Question_7 = 0
    Question_8 = 0
    Question_9 = 0
    Question_10 = 0
    def traslate(self, text):
        if text == "Yes":
            return 1
        elif text == "No":
            return 0


    def add_results(self):
        global new_arr_symp

        # Do you use Hormonal Contraceptives
        Question_5 = self.traslate(self.Question_5)

        # years to use Hormonal Contraceptives
        textinput_6 = self.tinput_year_6.text

        if textinput_6:
            Question_6 = int(textinput_6)
        else:
            Question_6 = 0

        # Do you use IUD
        Question_7 = self.traslate(self.Question_7)

        #  How many years use IUD?
        textinput_8 = self.tinput_year_8.text
        if textinput_8:
            Question_8 = int(textinput_8)
        else:
            Question_8 = 0

        # Do you have STDs
        Question_9 = self.traslate(self.Question_9)

        # How many years have STDs
        textinput_10 = self.tinput_year_10.text
        if textinput_10:
            Question_10 = int(textinput_10)
        else:
            Question_10 = 0

        new_arr_symp = new_arr_symp+ [
            Question_5,
            Question_6,
            Question_7,
            Question_8,
            Question_9,
            Question_10,
            ]

        if (Question_5 == 1 or Question_5 == 0) and(Question_7 == 1 or Question_7 == 0) and (Question_9 == 1 or Question_9 == 0):
            self.manager.current = 'screen_3'
        else:
            self.ids.error_2.text = Label(text="Must select one 'yes' or 'no'").text

class Screen_3(Screen):
    Question_11=0
    Question_12=0
    Question_13=0
    Question_14=0
    Question_15=0
    Question_16=0
    def traslate(self, text):
        if text == "Yes":
            return 1
        elif text == "No":
            return 0


    def add_results(self):
        global new_arr_symp

        # Do you have condylomatosis?
        Question_11 = self.traslate(self.Question_11)

        # Do you have cervical condylomatosis
        Question_12 = self.traslate(self.Question_12)

        #Do you have vaginal condylomatosis

        Question_13 = self.traslate(self.Question_13)

        #Do you have vulvo-perineal condylomatosis
        Question_14 = self.traslate(self.Question_14)

        #Do you have syphilis?
        Question_15 = self.traslate(self.Question_15)

        #Do you have pelvic inflammatory disease?
        Question_16 = self.traslate(self.Question_16)

        new_arr_symp = new_arr_symp+[
            Question_11,
            Question_12,
            Question_13,
            Question_14,
            Question_15,
            Question_16,
        ]
        if (Question_11 == 1 or Question_11 == 0) and(Question_12 == 1 or Question_12 == 0) and (Question_13 == 1 or Question_13 == 0)and (Question_14 == 1 or Question_14 == 0) and(Question_15 == 1 or Question_15 == 0) and (Question_16 == 1 or Question_16 == 0):
            self.manager.current = 'screen_4'
        else:
            self.ids.error_3.text = Label(text="Must select one 'yes' or 'no'").text

class Screen_4(Screen):
    Question_17 = 0
    Question_18 = 0
    Question_19 = 0
    Question_20 = 0
    Question_21 = 0
    Question_22 = 0
    def traslate(self, text):
        if text == "Yes":
                return 1
        elif text == "No":
                return 0


    def add_results(self):
        global new_arr_symp


        #Do you have genital herpes?
        Question_17 = self.traslate(self. Question_17)

        #Do you have molluscum contagiosum?
        Question_18 = self.traslate(self. Question_18)

        #Do you have AIDS?
        Question_19 = self.traslate(self. Question_19)

        #Do you have HIV?
        Question_20 = self.traslate(self. Question_20)

        #Do you have Hepatitis B
        Question_21 = self.traslate(self. Question_21)

        #Do you have HPV?
        Question_22 = self.traslate(self. Question_22)

        #Number of diagnosis HPV
        textinput_23 = self.tinput_23.text
        if textinput_23:
            Question_23 = int(textinput_23)
        else:
            Question_23= 0

        new_arr_symp = new_arr_symp+ [
            Question_17,
            Question_18,
            Question_19,
            Question_20,
            Question_21,
            Question_22,
            Question_23,
            ]+ symp_arr
        if (Question_17 == 1 or Question_17 == 0) and(Question_18 == 1 or Question_18 == 0) and (Question_19 == 1 or Question_19 == 0)and (Question_20 == 1 or Question_20 == 0) and(Question_21 == 1 or Question_21 == 0) and (Question_22 == 1 or Question_22 == 0):
            self.manager.current = 'prediect'
        else:
            self.ids.error_4.text = Label(text="Must select one 'yes' or 'no'").text




class Prediect(Screen):
    def pred_(self):
        print ("array of all screen:", new_arr_symp)

        #result_ = self.result_Label.text
        predect_result = ''

        #
        # #raeult is 1
        # new_arr = [[46,1,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0]]
        # # raeult is 1
        # arr_test=[[45, 1, 20, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #
        #
        #            1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,1, 1, 1, 0]]
        # arrr = [[14,12,16,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,1]]
        # #arr= [[40, 1, 20, 2, 0, 0, 1, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0]]
        caancer__ = pd.read_csv('/Users/sundus/Desktop/phase 1/phase 2/project_code/cervical-cancer2.csv')
        le = sklearn.preprocessing.LabelEncoder()
        caancer__ = caancer__.apply(le.fit_transform)
        X = caancer__.iloc[:, :40].values
        Y = caancer__.iloc[:, 40].values
        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
        mlp = MLPClassifier(hidden_layer_sizes=(100, 100, 100))
        mlp.fit(X_train, y_train)
        predect_result = mlp.predict([new_arr_symp])
        print("predect:",predect_result)
        #print(new_arr)
        #predect_result = self.result_input.text
        if predect_result == [0] :
            self.ids.result_input.text = "Negative \n Congratulation, you are not a Cervical cancer patient"
        else:
            self.ids.result_input.text = " Positive \n  It is suspected that you have  Cervical cancer"





        # cur.execute(
        #         "INSERT INTO user (Result) VALUES('" + self.ids.result_input.text +"')"
        #     )
        #
        # mydb.commit()
        # cur.close()
        # mydb.close()

        # print(caancer__.groupby('Dx:Cancer').size())








#print(caancer__.groupby('Dx:Cancer').size())
#         #mlp2 = mlp.fit(X_train, y_train)
#         #predect_result = mlp2.predict(new_arr)
#         #print(predect_result)
   #print(caancer__.groupby('Dx:Cancer').size())
#
#
#
#         #print (mlp2.predict(X_test))
# #         #print('Accuracy on the test subset of NN: {:.3f}'.format(mlp.score(X_test, y_test)))
# #         #print('Accuracy on the training subset OF NN: {:.3f}'.format(mlp.score(X_train, y_train)))
# #         #print(new_arr.groupby('Dx:Cancer').size())
# #         #add in database
# #         #Result =





class RefrenceScreen(Screen):
    def select(self):
        self.ids.sym_text.bind(text=self.spinner_clicked + self.touch_multiselect)

    def spinner_clicked(self, Spinner):
        self.sym_label = Label(text=" ")
        self.ids.sym_label.text = self.ids.sym_label.text + '\n ' + " %s " % self.ids.sym_text.text
    def delete_button(self):
        self.ids.sym_label.text = "  "
    def print__(self):

        Dr_info_Riyadh = ["Dr.name:"," ","Dr.Mohamad","\n ","Hospital name:"," ","King Faisal specialist","\n","phone number:"," ","016333333"]
        Dr_info_Jeddah = ["Dr.name:"," ","Dr.Ahmad","\n","Hospital name:"," ","Princess Noorah Oncology Center","\n","phone number:"," ","016333333"]
        Dr_info_Qassim = ["Dr.name:"," ","Dr.Abdullah","\n","Hospital name:"," ","Prince Faisal Bin Bandar Center","\n","phone number:"," ","016333333"]
        for i in self.ids.sym_text.values:
            if "Riyadh" in  self.ids.sym_label.text:
                self.ids.sym_label.text = (' '.join(Dr_info_Riyadh))
            elif "Jeddah" in  self.ids.sym_label.text:
                self.ids.sym_label.text = (' '.join(Dr_info_Jeddah))
            elif "Qassim" in self.ids.sym_label.text:
                self.ids.sym_label.text = (' '.join(Dr_info_Qassim))

    def link_(instance):
        webbrowser.open('https://www.healthline.com/health/cervical-cancer-symptoms')

    class mainapp(App):
        def build(self):
            return Link_()




class CervicalCancer(App):
    def build(self):
        return RefrenceScreen()


CervicalCancer().run()

