import flet as ft
import json

class person:
    def __init__(self,name,age,gender,answer_list):
        self.name =  name
        self.age = age
        self.gender = gender
        self.answer_list = answer_list


def main(page: ft.Page):
    page.title = "subaru dating sim"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll=ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.TRANSPARENT
    #if you wish to use background images, you must set the background color to transparent first

    #this is how you can set background image
    page.decoration = ft.BoxDecoration(
        image = ft.DecorationImage(
            src="star.webp",
            fit= ft.BoxFit.FILL,
            #ft.BoxFit.FILL distorts the image to fit the entire screen.
        )
    )

    def main_page():
        page.theme_mode = ft.ThemeMode.DARK
        page.controls.clear()
        title=ft.Text("Subaru dating sim",size=50 , weight=ft.FontWeight.W_600)
        username = ft.TextField(label = "Name", hint_text="Please enter your user name")
        password = ft.TextField(label = "Password", password=True,can_reveal_password=True)
       
        def submit_click(e):
            data = {}
            try:
                with open("data.json", 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}
            if username.value in data and data[username.value]["password"] == password.value:
                print("Login successfully")
                question_page(username.value)

        def register_click(e):
            register_page()

        page.theme_mode = ft.ThemeMode.DARK
        register_button = ft.Button("Register", on_click=register_click)
        Login = ft.Button(content = "Login", on_click=submit_click)
        page.add(
            ft.Container(
                content = ft.Column(
                    controls = [
                        title,   
                    ]
                )
            ),
            username,
            password,
            Login,
            register_button
        )
        page.update()


    

    

    def register_page():
        page.controls.clear()
        page.floating_action_button = None


        greeting = ft.Text(value="Please register for a new account")
        username = ft.TextField(label="Name", hint_text="Please enter your user name")
        password = ft.TextField(label="Password", password=True, can_reveal_password=True)
        passwordconfirm = ft.TextField(label="Confirm your Password", password=True, can_reveal_password=True)
        age = ft.TextField(label="Age")


        gender = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="male", label="Male"),
                    ft.Radio(value="female", label="Female"),
                    ft.Radio(value="other", label="Other")
                ]
            )
        )


        feedback = ft.Text(size=16)


        def register_click(e):
            if password.value != passwordconfirm.value:
                feedback.value = "Passwords do not match"
                page.update()
                return


            if not username.value or not password.value or not age.value or gender.value is None:
                feedback.value = "Please fill in all fields"
                page.update()
                return


            if not age.value.isdigit() or int(age.value) <= 0:
                feedback.value = "Please enter a valid age"
                page.update()
                return


            data = {}


            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}


            if username.value in data:
                feedback.value = "Username already exists"
                page.update()
                return


            data[username.value] = {
                "password": password.value,
                "age": int(age.value),
                "gender": gender.value
            }


            with open("data.json", "w") as f:
                json.dump(data, f)


            main_page()


        proceed_button = ft.Button("Proceed", on_click=register_click)


        page.add(
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[
                        greeting,
                        username,
                        password,
                        passwordconfirm,
                        age,
                        ft.Text("Select your gender:"),
                        gender,
                        feedback,
                        proceed_button
                    ],
                    alignment=ft.Alignment.CENTER
                )
            )
        )


        page.update()


       #use radio groups to make the multiple choice questions
    
    def question_page(current_user):
        global user_data
        questions = [
            "pineapple on pizza?",
            "do you sing in the shower?",
            "are you a morning person?",
            "Do you believe in love at first sight?",
            "Do you believe everything happens for a reason?",
            "Do you think people can truly change?",
            "Can you eat pizza cold straight from the fridge?",
            "Do you still rely on GPS to get around your own city?",
            "Do you buy things you don't need just because they are on sale?",
            "do you like this quiz?"
        ]
        page.controls.clear()
        radio_groups={}

        for i in range(len(questions)):
            
            question_text_string=questions[i]
            ui_text= ft.Text(value=question_text_string,size=16,weight="bold",text_align=ft.TextAlign.CENTER)
            key=f"q_{i}"
            radio_groups[key]=ft.RadioGroup(
                    content=ft.Row(
                        controls=[
                            ft.Radio(value="strong disagree", label="strong disagree"),
                            ft.Radio(value="somewhat disagree", label="somewhat disagree"),
                            ft.Radio(value="neutral", label="neutral"),
                            ft.Radio(value="somewhat agree", label="somewhat agree"),
                            ft.Radio(value="strong agree", label="strong agree"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
            page.add(ui_text,radio_groups[key],ft.Text("\n"))

       
        def submit(e):
            answers=[]
            for key in radio_groups:
                answers.append(radio_groups[key].value)

            data={}

            try:
                with open("answers.json","r") as f:
                    data=json.load(f)
            except FileNotFoundError:
                data={}
            data[current_user]=answers
            with open("answers.json","w") as f:
                json.dump(data,f)
            score_page(current_user)       

        submit_button=ft.Button("Submit",on_click=submit)
        page.add(submit_button)




#maybe use rows to show who you have stuff in common with and what when u match
#this does absolutely nothing rn
    def score_page(current_user):
        page.controls.clear()
        page.floating_action_button = None
               
        score_text = ft.Text(value=("Your answers have been saved"), size=30, weight=ft.FontWeight.BOLD)

        match_button=ft.Button("find a match",on_click=lambda e: match_page(current_user))
        page.add(
                ft.Container(
                    content=ft.Column(
                        controls=[score_text],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment.CENTER,
                )
            )
        page.add(match_button)
        page.update()

    def match_page(current_user):
        page.controls.clear()
        feedback=ft.Text(size=25)
        try:
            with open("answers.json","r") as f:
                data=json.load(f)
        except FileNotFoundError:
            data={}

        my_answers=data[current_user]
        best_match=None
        best_score=-1
        for user in data:
            if user !=current_user:
                other_answers=data[user]
                score=0
                for i in range(len(my_answers)):
                    if my_answers[i]==other_answers[i]:
                        score+=1
                if score>best_score:
                    best_score=score
                    best_match=user
        if best_match==None:
            feedback.value="no other users to match with yet"
        else:
            feedback.value=(f"your best match is {best_match}\n"f"compatibility: {best_score}/10")
        page.add(ft.Container(content=ft.Column(controls=[ft.Text("Your Match",size=45), feedback],horizontal_alignment=ft.CrossAxisAlignment.CENTER),alignment=ft.Alignment.CENTER ))
        page.update()

    main_page()   


ft.run(main)

#add second json file
#finish register and login page 

#leave matching till last