# Full Stack API Final Project


## Start Backend
1, First, install dependencies at the backend folder using the command below

```bash
pip install -r requirements.txt
```

2, Then, from the backend folder, set up a database
```bash
psql trivia < trivia.psql
```

3, Running the server
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Frontend

Run frontend using these commnad at the frontend directory
```bash
npm install
npm start
```

## Endpoint
Use @app.route('/categories') to get all categories

Use @app.route('/questions') to get all questions

Use @app.route('/questions/<int:question_id>') to delete a question with DELETE method

Use @app.route('/questions') to post new question or search a question with POST method

Use @app.route('/categories/<int:category_id>/questions') to get questions based on a category

Use @app.route('/quizzes') to get quizzes with POST method
