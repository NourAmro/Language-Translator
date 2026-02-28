from tkinter import *
from tkinter import ttk, filedialog
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import os

def get_languages():
    translator = GoogleTranslator()
    supported_languages = translator.get_supported_languages(as_dict=True)
    return sorted(supported_languages.values())

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        input_text.delete(0, END)
        input_text.insert(END, recognized_text)
        translate_text()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def translate_text():
    translator = GoogleTranslator(source='auto', target=dest_lang.get())
    translated = translator.translate(input_text.get())
    output_text.delete(1.0, END)
    output_text.insert(END, translated)

def text_to_speech():
    text = output_text.get(1.0, END)
    if text.strip() != "":
        tts = gTTS(text=text, lang=dest_lang.get())
        tts.save("output.mp3")
        os.system("start output.mp3")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            input_text.delete(0, END)
            input_text.insert(END, text)

root = Tk()
root.geometry('1100x400')  # Increased height to 400
root.resizable(0, 0)
root['bg'] = 'slategrey'
root.title("Language Translator")

Label(root, text="Language Translator", font="Arial 20 bold",fg='white', bg='slategrey').pack()

Label(root, text="Enter Text", font="arial 13 bold",fg='white',bg='slategrey').place(x=30, y=60)
input_text = Entry(root, width=60)
input_text.place(x=30, y=90)  
input_text.insert(0, "") 



Label(root, text="Output", font="arial 13 bold",fg='white',bg='slategrey').place(x=610, y=60)
output_text = Text(root, font="arial 10", wrap=WORD, padx=5, pady=5, width=50, height=8)
output_text.place(x=610, y=90)

scrollbar = Scrollbar(root, command=output_text.yview)
scrollbar.place(x=1080, y=90, height=165)
output_text.config(yscrollcommand=scrollbar.set)

dest_lang = ttk.Combobox(root, values=get_languages(), width=22)
dest_lang.place(x=30, y=130)
dest_lang.set("Choose Language")

voice_btn = Button(root, text="Voice Input", font="arial 12 bold", pady=5, command=recognize_speech, bg="pink", activebackground="lightgreen")
voice_btn.place(x=30, y=250)

translate_btn = Button(root, text="Translate", font="arial 12 bold", pady=5, command=translate_text,fg='white', bg="firebrick", activebackground="green")
translate_btn.place(x=260, y=250)

file_btn = Button(root, text="Open File", font="arial 12 bold", pady=5, command=open_file, bg="pink", activebackground="lightblue")
file_btn.place(x=150, y=250)

text_to_speech_btn = Button(root, text="Text to Speech", font="arial 12 bold", pady=5, command=text_to_speech, bg="pink", activebackground="lightblue")
text_to_speech_btn.place(x=610, y=250)

root.mainloop()
