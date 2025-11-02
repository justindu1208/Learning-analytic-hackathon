# Option A – Live Collaboration (Visual Studio Code Live Share)

This guide explains how to set up and work together in real-time using **Visual Studio Code Live Share** (Google Docs-like workflow)

Pick one person in the team who is the most comfortable with GitHub and Python; they will be acting as the **host**. Others are **guests**.

---

## 1️. Install Visual Studio Code [🧑‍💻👥 ALL - Host + Guests]

Everyone in the team must have VS Code installed.

1. Download VS Code → [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

2. Open VS Code and click on the **Extensions** icon on the left sidebar:

   <img width="277" height="405" alt="image" src="https://github.com/user-attachments/assets/6a1f1e69-0ffb-4284-a845-2ec2205ee4f5" />

3. In the search bar, install the following extensions:
   - **Live Share** — enables real-time collaborative coding  
     
     <img width="360" height="183" alt="image" src="https://github.com/user-attachments/assets/bfa6c426-4a20-4a2e-be0a-5b5724b6988c" />
   - **Python** (by Microsoft)
   - **Jupyter** (for working with notebooks)

---


## 2️. Complete the environment setup [🧑‍💻 Host only]

The **Host** is responsible for preparing the coding environment.  
Follow **all steps** described in [`Setup/SETUP_ENVIRONMENT.md`](SETUP_ENVIRONMENT.md):

This includes:
- Installing **Python** and **Git**  
- **Cloning** your team’s repository  
- Creating and activating a **virtual environment** (`myvenv`)  
- Installing dependencies from `requirements.txt`  
- Adding the **`.env`** file to the root of the repo  
- Downloading and placing the **dataset** in the `data/` folder  

---

## 3️. Open the repository in VS Code [🧑‍💻 Host only]

1. Open **VS Code** → `File → Open Folder...` → choose your team’s repository (e.g., `team-A`).
2. Open the **Command Palette** (`Ctrl + Shift + P` or `Cmd + Shift + P` on Mac).
3. Type and select:
```text
Python: Select Interpreter
```
4. Click on _Enter interpreter path_ and choose the interpreter located inside your virtual environment:
- Windows: `myvenv\Scripts\python.exe`
- Mac/Linux: `myvenv/bin/python`
5. Open the notebook:
```text
notebooks/explore.ipynb
```
6. Verify that you can run a cell using **Shift + Enter**. If it doesn't work, make sure that you have installed the **Jupyter** extension in VS Code (step 1.3).

---

## 4️. Start the Live Share session [🧑‍💻 Host only]

Once your environment is set up and you can run notebooks locally:

1. In **VS Code**, click the **Live Share** icon located **in the bottom status bar (bottom-left corner of the window)**.

   <img width="559" height="113" alt="image" src="https://github.com/user-attachments/assets/885c891c-bf28-4064-bcd6-c2ca5d0140bf" />

2. If prompted, sign in using your **Microsoft** Imperial account.

3. After a few seconds, a **sharing link** will be generated automatically and copied to your clipboard.

4. Send the link to your teammates via your team's channel on Teams.

5. When a teammate clicks your link, you’ll see a **popup notification on the right side**. Click **Accept** ✅ to let them join your session.


### Manage collaboration settings

While hosting, you can manage your session directly from the **Explorer panel** on the **left-hand side**.  
Click the **Explorer** icon, then scroll down to the **Live Share** section.

<img width="447" height="500" alt="image" src="https://github.com/user-attachments/assets/b8aa026e-052c-4f8d-9235-0b434e0e9182" />

From here, you can control:
- **Editing permissions** – Choose whether guests can *edit* or *view only*.  
- **Shared terminals** – Disable sharing if you don’t want guests to access your terminal.  
- **Comments and chat** – Open “Session chat” to communicate with your team directly inside VS Code.
- etc.


---

## 5️. Join the session [👥 Guests only]

1. **Copy** the invitation **link** shared by your host.
2. Open **Visual Studio Code**.
3. Click the **Live Share** icon on the **left-hand sidebar**.
4. In the panel that opens, click **Join**.
   
<img width="525" height="780" alt="image" src="https://github.com/user-attachments/assets/01fff363-4aa8-431c-b1e6-9ff94ed374f0" />

5. Paste the link you received from your host.*
6. When prompted to sign in, choose  
   **“Join as Anonymous”** (**Do not** sign in with Microsoft or GitHub).  
   This is faster and avoids login or permission delays/bugs during the hackathon.

7. Wait for the **host to accept your connection** — a small pop-up will appear on the **right-hand side** of the host’s screen.
   


8. You can now:
   - **View and edit** files live  
   - **Chat** or comment within VS Code’s Live Share chat panel  
   - **See the host’s cursor and follow their view**
    
---
## 🚨 IMPORTANT: Keep the session active and save progress
### Keep the session active

- The Live Share session will automatically **end** if:
  - The host **closes VS Code**  
  - The host’s **laptop sleeps or shuts down**  
  - The host **loses internet connection**

If this happens, simply reopen VS Code and redo step 4 to start a new session.  A **new link** will be generated; share it with your teammates so they can re-join.

---

### Save and back up progress

During the session:
- All edits made by guests are saved **locally on the host’s computer**.  
- Guests do **not** retain a local copy once the session ends.

To prevent data loss:
1. The **host** should regularly **save all files** in VS Code (`Ctrl + s` / `Cmd + s`).
2. Every few hours (or after major edits), the host should push changes to GitHub online team repo:
   ```bash
   git add .    # or specify a file if you prefer, e.g., git add notebooks/explore.ipynb
   git commit -m "Describe the changes here"
   git push
   ```
