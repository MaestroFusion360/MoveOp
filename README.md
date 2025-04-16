<h1 align="center">
  <img src="icon.svg" height="28"/>
  MoveOp for Fusion 360
</h1>

<p align="center">
  <strong>Fixes locked operation order after Import CAM Data</strong>
</p>

<p align="center">
  <a href="LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
  </a>
</p>

---

## Table of Contents
- [Overview](#overview)
- [Installation \& Usage](#installation--usage)
- [License \& Disclaimer](#license--disclaimer)
- [Contact Me](#contact-me)

---

## Overview

#### **Problem**  
After using **Import CAM Data** in Fusion 360:  
- CAM operations **lock in the Operations Tree** (not the timeline)  
- Drag-and-drop reordering becomes impossible  
- Operations stay **bound to their Setup** (can only reorder within one Setup)  

#### **Solution**  
The **MoveOp** add-in adds **Move Up/Down** buttons to the CAM panel, allowing:  
- Reordering **within the same Setup** (Fusion’s native restriction)  
- No manual parameter editing required  
- Full preservation of operation settings  

⚠️ **Note**:  
- This add-on is only useful if you use Import Cam Data—otherwise, native drag-and-drop works fine without it.
- Moving operations **between Setups** is impossible.

---

## Installation & Usage

- ### Setup
1. Download latest `.zip` release.
2. Extract the archive.
3. Copy the add-on folder to the following directory:  
**`%appdata%\Autodesk\Autodesk Fusion 360\API\AddIns`**.
4. Open **Fusion 360**.
5. Press **`Shift + S`** or go to **Tools → Scripts and Add-Ins**.
6. In the upper part of the window, click on the **plus** (**`+`**).
7. In the Add-Ins dialog, choose `Link an App from Local` to load your add-on directly from a local folder. Navigate to the folder where your add-on is located and select it.
8. Select the add-on from the list and click **`Run`**.
9. To have the add-on run automatically at startup, check the **`Run on Startup`** box.

**⚠️ Important:**
- **MoveOp** works **only on Windows**.
- If the **AddIns** folder doesn't exist, create it manually.
- If the add-on doesn't run, try restarting Fusion 360.

---

## License & Disclaimer

This project is licensed under the **MIT License** - see the [LICENSE.md](LICENSE.md) file for full details.

---

### Contact Me

**Let's connect!**

**Email:** [maestrofusion360@gmail.com](mailto:maestrofusion360@gmail.com)
**Telegram:** [@MaestroFusion360](https://t.me/MaestroFusion360) 

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=MaestroFusion360-MoveOp&label=Project+Views&color=blue" alt="Project Views" />
</p>
