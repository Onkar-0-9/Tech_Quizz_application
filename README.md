# Technical Quiz Application

An interactive quiz platform built with Flask and MongoDB that allows students to test their knowledge while providing administrators with question management capabilities.

## Features

- **User Authentication**
  - Student and Admin role separation
  - Secure password hashing
  - Session management

- **Student Features**
  - Interactive quiz interface
  - Real-time score tracking
  - Progress indicator
  - Previous results history

- **Admin Features**
  - Question management dashboard
  - User management
  - Add/Edit quiz questions
  - View student results

## Technology Stack

- Backend: Flask (Python)
- Database: MongoDB
- Frontend: HTML, CSS, JavaScript
- Authentication: Session-based

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/[YOUR-USERNAME]/tech-quiz-app.git
cd tech-quiz-app
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure MongoDB**
- Install MongoDB locally or use MongoDB Atlas
- Update connection string in `app.py`

5. **Environment Variables**
Create a `.env` file:
```
MONGO_URI=mongodb://localhost:27017
SECRET_KEY=your_secret_key
```

6. **Run the Application**
```bash
python app.py
```

## Project Structure

```
tech_quiz_website_4488q9/
├── app.py              # Main application file
├── static/            
│   ├── style.css      # Stylesheet
│   └── script.js      # Frontend JavaScript
├── templates/
│   ├── admin_dashboard.html
│   ├── student_dashboard.html
│   ├── login.html
│   └── register.html
├── requirements.txt
└── README.md
```

## Usage

1. **Admin Access**
   - Login with admin credentials
   - Access `/admin` dashboard
   - Add/manage questions
   - View user progress

2. **Student Access**
   - Register/Login as student
   - Start quiz from dashboard
   - Answer questions
   - View results

## API Endpoints

- `GET /get_question` - Fetch quiz questions
- `POST /submit_answer` - Submit quiz answers
- `GET /get_score` - Retrieve quiz scores
- `POST /admin/add_question` - Add new questions (Admin only)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - Feel free to use and modify for your purposes.

## Contact

[Your Name] - [Your Email]
Project Link: https://github.com/[YOUR-USERNAME]/tech-quiz-app
