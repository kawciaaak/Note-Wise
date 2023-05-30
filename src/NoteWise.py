import os
import ctypes
import sys
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
import openai
from decouple import config
sys.path.append(str(Path(__file__).resolve().parent.parent))
import setup

class Backend(QObject):
    processingFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize filenames
        self.note_filename = b"user_note.txt"
        self.save_filename = b"generated_notes.txt"
        # Load the DLL
        dll_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "fileManager.dll")
        self.dll = ctypes.CDLL(dll_path)

    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]
    
    def __json__(self):
        serialized_data = {
            'note_filename': self.note_filename,
            'save_filename': self.save_filename
        }
        return serialized_data

    @Slot(str)
    def setInputFileName(self, filename):
        self.note_filename = filename.encode()

    @Slot(str)
    def setSaveFileName(self, filename):
        self.save_filename = filename.encode()

    @Slot()
    def startProcessing(self):
        # Initialize OpenAI GPT-3.5
        openai.api_key = config('API_KEY')
        command = f"""
        You are a helpful assistant. Your task is to generate comprehensive notes based on the input.\
                  If the input contains mathematical formulas, the assistant should provide a detailed explanation for \
                    each of them. It should not omit any relevant information and ensure that the generated notes \
                        are informative and concise, closely aligned with the provided text.
        """

        # Get function pointer
        read_text = self.dll.read_text
        read_text.argtypes = [ctypes.c_char_p]
        read_text.restype = ctypes.c_char_p

        save_text = self.dll.write_text
        save_text.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        save_text.restype = None

        # Load user's note
        note = read_text(self.note_filename)

        # Prepare prompt to send
        prompt = f"""
        ```{command}```
        ```{note}```
        """

        # Use GPT-3.5 to generate notes
        response = self.get_completion(prompt)

        # Save generated notes
        save_text(self.save_filename, ctypes.c_char_p(str(response).encode()))

        # Emit signal to inform QML about finished processing
        self.processingFinished.emit()

   


setup.set_API_key()

# Initialize main window and QML engine
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

# Register the Python type. 
qmlRegisterType(Backend, 'Backend', 1, 0, 'Backend')

# Get path to UI file 
qml_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", "noteWiseUI.qml")

# Load QML engine
engine.load(qml_file)

# Check root objects
if not engine.rootObjects():
    sys.exit(-1)

# Aplication start
sys.exit(app.exec())