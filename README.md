# Mouse Controller

by Will :)
-
 a Python-based tool designed for precision mouse movement automation, ideal for use in scenarios such as recoil control in FPS games (**Siege**, CSGO, Etc.) or custom mouse behaviors for accessibility.
  Real-time mouse movement controlled by holding the left mouse button.

   - Per-profile X and Y movement speeds with independent acceleration curves.

   - Intuitive web interface (built with Flask) for creating, editing, and managing profiles.
  
   - Live configuration reload using watchdog, so changes to profiles take effect instantly.
  
   - Designed to be lightweight and responsive, with real-time keyboard toggling and profile switching.

Key Features
- Toggle activation with G key

- Adjustable speed and acceleration for X/Y separately

- Create/delete profiles via web UI

- Auto-loads active profile and reloads on file changes

- Two pages for different profile configurations

Requirements

**Only Works on Windows!!!!**
- flask, pynput, watchdog,

      pip install -r requirements.txt

How to Use
- Download .zip
- Install Requirements ^^^^^^^
- Run *run.bat* (two cmd prompts will open, one is the mouse script and the other is the web server)
- Navigate to http://localhost:5000/
- X and Y represent the speed
- XA and YA represent the acceleration

# Screenshots
![image](https://github.com/user-attachments/assets/081f5eb3-ac80-4367-9cef-6b2b5aab9200)

![image](https://github.com/user-attachments/assets/0a011354-5d90-478b-9674-6df3d132789c)



Credits
-
Me and ChatGPT
