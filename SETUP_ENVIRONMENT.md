# Setting up the coding environment

### 1. Open the terminal
   - **Windows**: Use Windows PowerShell
   - **Mac**: Use the built-in Terminal app
   - **Linux**: Use your default terminal

### 2. Install Python (if not already installed)

Verify if Python is installed on your machine. On your terminal, run this command:
```bash
python --version
```
If your system uses python3 instead:
```bash
python3 --version
```
Your terminal should display the Python version installed on your machine:
<img width="1116" height="148" alt="image" src="https://github.com/user-attachments/assets/140dd7f1-0d3a-453e-8a3f-09e0fb23aef1" />

This project works best with Python 3.11.
If you already have Python installed but it’s 3.12 or 3.13 (like shown on the screenshot above), that’s fine, you do not need to uninstall anything.
Just install Python 3.11 side-by-side.

#### Windows

1. Download Python 3.11 from: https://www.python.org/downloads/windows/
2. Important: During installation, **check the box** that says: ✅ Add Python to PATH
3. Run this in Terminal to check:
```bash
py -3.11 --version
```

<img width="427" height="64" alt="image" src="https://github.com/user-attachments/assets/be12d27f-06ae-4833-915f-8fa99cecb28c" />



#### MacOS

1. Download Python 3.11 from: https://www.python.org/downloads/macos/
2. Install normally.
3. Run this in Terminal to check:
```bash
python3.11 --version
```

#### Linux
1. Run this in the terminal:
```bash
sudo apt update                                   # refreshes package list
sudo apt install python3.11 python3.11-venv python3.11-dev   # installs Python 3.11 + venv support
python3.11 --version                               # verifies installation
```

### 3. Install git (if not already installed)

Verify if git is installed on your machine. On your terminal, run this command:
```bash
git --version
```

Your terminal should display the git version installed on your machine:
<img width="1120" height="111" alt="image" src="https://github.com/user-attachments/assets/79639067-ffb0-4c74-9ff8-e100a4a0f938" />

If git is not installed on your machine:

1. Install git
   - Windows:
      - Download from https://git-scm.com/download/win
      - Run the installer (you can keep the default settings)

   - macOS:
      - Option A: Install Git via Xcode command line tools
        run this in the terminal:
        ```bash
         xcode-select --install
         ```

      - Option B: Use Homebrew (if already installed)
        run this in the terminal:
         ```bash
         brew install git
         ```

   - Linux (Debian/Ubuntu):
      run this in the terminal:
      ```bash
      sudo apt update
      sudo apt install git
      ```

2. Restart the terminal and run this command again to confirm installation:
   ```bash
   git --version
   ```


### 4. Create the folder on your local machine where you want to store  your team's work locally
1. Create your project folder on your Desktop
2. On the terminal, use the `cd` (change directory) to move to where you want to work:
   ```bash
   cd path/to/your/project/folder
   ```
   For example:
   ```bash
   cd Desktop/hackathon-project
   ```
Your terminal should look like this:
<img width="1110" height="95" alt="image" src="https://github.com/user-attachments/assets/bf10a6fb-8790-48ae-94c5-05ff1ab43b23" /> 

### 5. Clone your team's repository on your local machine
Follow these steps to clone your team's repository on your computer:

1. Click on the green button "Code" in the top right corner of your team's GitHub repo page. Click on the HTTPS tab and copy the URL displayed: <br> 
   <img width="910" height="437" alt="image" src="https://github.com/user-attachments/assets/62c6d297-3f51-4232-a66c-5c847a51639c" />


2. Run this command on the terminal. Make sure that your terminal indicates that you are in the folder you created in the previous step:

   <img width="1725" height="166" alt="image" src="https://github.com/user-attachments/assets/53cb85ca-7f7e-4c0d-b5aa-0f9e231f00b1" />

   Run this command:
   ```bash
   git clone paste-the-link-you-have-copied-in-the-first-step
   ```
   If this command doesn't work, try running this command instead:

   ```bash
   git clone https://[insert-your-github-username]@github.com/LA-hackathon-test/team-[your-team-name].git
   ```

   Team names are all lowercase with hyphens (e.g., `team-A`, `team-B`, etc.)

4. If prompted by Git in the terminal:
   - Username → your GitHub username
   - Password → This is a Personal Access Token (PAT) instead of your GitHub password

   To generate a PAT, follow these steps:
   Go to: https://github.com/settings/tokens

   1. Click "Generate new token" → Choose "Fine-grained token" (or "Classic" if needed)
      - Name (text input): e.g., Hackathon Access
      - Resource owner (Dropdown): LA-hackathon-test
      - Expiration (Dropdown): Set to 7 days or the duration of the hackathon
      - Under Repository Access, select: All repositories
      - Under Permissions → Repository permissions: Set Contents: Read and Write

   2. Click "Generate Token" and copy it immediately somewhere safe (you won’t see it again!)
### 6. Change directory to be in your team's repository that you just cloned:
Run this command in the terminal:
```bash
cd team-[your-team-name]
```
Your terminal should look like this (your team repo instead of team-A's one):
<img width="1716" height="163" alt="image" src="https://github.com/user-attachments/assets/197be7cb-3bef-4f3c-90c7-bbc2a841b153" />


### 7. Set up a Python environment and download the necessary libraries
In the terminal (on the same tab, make sure you're inside your team's repository)

1. Create the python environnement (using Python3.11):
- On Windows:
   ```bash
   py -3.11 -m venv myvenv  #Create a virtual environnements called myvenv
   ```
- On MacOs/Linux:
  ```bash
  python3.11 -m venv myvenv #Create a virtual environnements called myvenv
  ```
  
2. Activate the Python environment:
   Depending on your machine, follow these instructions:
   <br>
   <br>
   - On Linux/Mac:
      ```bash
      source myvenv/bin/activate      
      ```
   - On Windows:
      ```bash
      myvenv\Scripts\activate
      ```
      Or run this command instead if you're having an error related to Windows' script execution policy. You might need to run Windows PowerShell Terminal as an administrator. 
      ```bash
      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
      myvenv\Scripts\activate
      ``` 

Your terminal should look like this:
<img width="1725" height="150" alt="image" src="https://github.com/user-attachments/assets/3dd7acc1-2f44-4c6c-b045-d8d14d2c3bcd" />

### 8. Download libraries
In the terminal (on the same tab, make sure you're inside your team's repository and that myvenv is activated)
1. To install the list of libraries available in requirements.txt
   ```bash
   pip install -r requirements.txt #install all libraries that are in requirements.txt
   ```
2. To install any further libraries that you would need in the future:
   ```bash
   pip install libary-name
   ```
   Replace library-name with the library name available on: https://pypi.org/
3. (Optional) If you install new libraries, to update the requirements.txt file, run in the terminal (make sure that you are in the folder that contains requirements.txt):
   ```bash
   pip freeze > requirements.txt
   ```
