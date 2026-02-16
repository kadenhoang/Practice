# Student & Teacher Info — Application

Desktop app: sign in, add and look up students and teachers.

## Run with Python

From this folder (`oop`):

```bash
python gui.py
```

Or double‑click **RUN_APP.bat** (runs the built exe if present, otherwise `python gui.py`).

## Build a standalone .exe (Windows)

1. Install PyInstaller (once):  
   `pip install pyinstaller`
2. Build:  
   Double‑click **build.bat**, or run:
   ```bash
   pyinstaller --noconfirm gui.spec
   ```
3. The executable is created at:  
   **dist\Student Teacher Info.exe**

You can copy **Student Teacher Info.exe** to any folder (or another PC). The first time you run it there, it will create `users.txt`, `student.txt`, and `teacher.txt` in that same folder. No Python installation is required to run the .exe.

## Data files

- **users.txt** — accounts (passwords are hashed)
- **student.txt** — student records
- **teacher.txt** — teacher records

When run as a script, these live in the `oop` folder. When run as the built exe, they are created next to the exe.
