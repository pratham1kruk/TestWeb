# Static Test Website

This repository contains a **testing static website** created for experimenting with deployment, hosting, and asset handling on **AWS Amplify**.

The project is purely frontend-based and includes basic HTML, CSS, and static assets such as images.

---

## 📁 Project Structure
smart_parking/
├── index.html
├── profile.html
├── signin.html
├── signup.html
├── SmartPrediction.html
├── MyBooking.html
├── Booking_parking.html
├── static/
│ ├── css/
│ │ └── style.css
│ ├── images/
└── README.md

> Note: During deployment, files are arranged so that Amplify can serve them as static assets.

---

## 🚀 Deployment

This project is deployed using **AWS Amplify Hosting**.

- No backend or server-side rendering is used
- No framework build process (React, Angular, etc.)
- Files are served as static content

Below is `amplify.yml` which defines Amplify configuration
-------------------------------------------------------------------
version: 1
frontend:
  phases:
    build:
      commands: []
  artifacts:
    baseDirectory: smart_parking
    files:
      - '**/*'
  cache:
    paths: []
--------------------------------------------------------------------

---

## 🛠 Technologies Used

- HTML5  
- CSS3  
- Static Images  
- AWS Amplify (Hosting)

---

## 🎯 Purpose

- Testing static website deployment on AWS Amplify
- Understanding folder structure and asset resolution
- Learning how Amplify serves HTML, CSS, and images

---

## ⚠️ Important Notes

- This is **not** a production application
- No backend, database, or authentication is included
- Intended only for testing and learning purposes

---

## 📌 How to Use

1. Clone the repository
2. Open `index.html` locally **or**
3. Deploy the repository to AWS Amplify

---

## 📄 License

This project is for educational and testing purposes only.
