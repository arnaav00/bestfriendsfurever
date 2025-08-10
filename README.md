#  Best Friends Furever – A Pet Catalog

**Team Members**  
- **Arnaav Anand** (Team Lead)  
- Andrew Fair  
- Dev Patel  

---

## Deployed Web App

We used **Streamlit Cloud** to host and deploy our application:  
🔗 **[Best Friends Furever App](https://bestfriendsfurever.streamlit.app/)**

---

## Purpose

The goal of this project is to create a **comprehensive pet adoption website** that streamlines the adoption process through:  

- A **user-friendly interface** to browse available pets, add new pets for adoption, and manage data.  
- Normalizing raw CSV pet adoption data into a **structured SQLite database**.  
- **LangChain integration** for natural language queries, allowing users to search the pet catalog intuitively.  

This project demonstrates **practical skills** in database management, web development, and applied AI.

---

## Tools & Technologies

1. **Database**: SQLite – lightweight, simple, and Python-friendly.  
2. **Password Hashing**: SHA256 for secure password storage.  
3. **Frontend**: Streamlit (Python) for building interactive web interfaces quickly.  
4. **Natural Language Querying**: OpenAI GPT-3.5 via **LangChain** to query the SQLite database using everyday language.  
5. **Deployment**: Streamlit Cloud for direct GitHub integration and hosting.

---

## Data

**Source**: Downloaded from Kaggle *(link placeholder)*  

**Tables**:  
- **intake** – Intake types (Owner Surrender, Stray, Foster, etc.)  
- **adoption_status** – Boolean flag for adoption status.  
- **pet_size** – Pet size categories (Small, Medium, Large).  
- **sex_type** – Sex types (Male, Female, Unidentified, Neutral, Spayed).  
- **animal** – Main pet details (type, name, breed, intake date, age, color, size, sex, URL, notes).

**Key Database Details**:  
- Preloaded data for `pet_size`, `intake_type`, and `sex_type`.  
- Adoption status defaults to **0** (not adopted).  
- CSV data is processed and inserted into `animal`.  
- Foreign keys ensure referential integrity.  
- Primary key: `animal_id`.

---

## Functionalities

### 1. Sign Up
- Enter **First Name, Last Name, Email, Username, Password**.  
- Email validated via regex.  
- Username uniqueness check.  
- Password hashing with SHA256 and visibility toggle.

### 2. Log In
- Validates username and password.  
- Stores credentials in **Streamlit session state**.

### 3. Landing Page
- Navigation buttons for:
  - Pet Catalog
  - Update Account Details
  - Submit New Pet
  - Log Out

### 4. Update Account Details
- Edit account information with full validation.  
- Option to **delete account** from the database.

### 5. Pet Catalog
- **3xN card grid** of pets showing:
  - Picture, Name, Age, Breed, Sex.  
- **"View Details"** button for more info.  
- LangChain-powered natural language queries.  
  Example queries:
  - `Show me foster pets`  
  - `Blue or Yellow pets`  
  - `Black dogs`  
  - `Show me female birds that are blue`  

### 6. Pet Details
- Full pet information display.  
- Adoption button updates status to “**ALREADY ADOPTED**”.

### 7. Submit New Pet
- Fill in all pet details with widgets (dropdowns, numeric fields, image upload).  
- Intake date set to submission date.  
- Image stored as BLOB in SQLite.

---

##  Issues & Challenges

1. Limited CSS & UI customization options in Streamlit.  
2. Difficulty with pixel-based component positioning.  
3. Button click events overwriting each other in Streamlit.  
4. Complex prompt engineering for **natural language → SQL** mapping.  
5. Data type casting for fields like AGE to improve AI query accuracy.

---

##  Individual Contributions

### **Arnaav Anand**
- Designed main `animal` table & reference tables.  
- Added check constraints for pet size & intake type.  
- Wrote `CREATE`, `INSERT`, and `UPDATE` statements for multiple tables.  
- Designed UI styles, wallpapers, and diagrams.  
- Implemented **Landing**, **Submit New Pet**, **Pet Details**, and **Update Account Details** pages.  
- Integrated all pages & deployed app.

### **Andrew Fair**
- Assisted database design for `animal` and attribute tables.  
- Built **Catalog page** with filtering and column layout.  
- Created ERD diagram.  
- Implemented adoption status system.  
- Converted dataset URLs to images in Streamlit.

### **Dev Patel**
- Designed keys for certain tables.  
- Created `sex_type` and `animal_type` tables with constraints.  
- Built **Login/Signup** functionality with Streamlit & Python.  
- Integrated LangChain SQL chain for GPT-3.5 natural language queries.  
- Assisted with deployment.


## Installation & Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/best-friends-furever.git
cd best-friends-furever

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
