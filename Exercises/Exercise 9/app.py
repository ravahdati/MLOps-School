from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize Data
student_details = {
    'name': 'Rasool Vahdati',
    'email': 'ra.vahdati@gmail.com',
    'major': 'MLOps School'
}

courses = [
    {
        'id': 1,
        'name': 'Introduction to Programming',
        'description': 'Learn the basics of programming using Python.',
        'teacher': 'Dr. Alice Smith',
        'category': 'Programming'
    },
    {
        'id': 2,
        'name': 'Web Development',
        'description': 'Build websites using HTML, CSS, and JavaScript.',
        'teacher': 'Mr. Rasool Vahdati',
        'category': 'Web'
    },
    {
        'id': 3,
        'name': 'WordPress Developer',
        'description': 'WP Coding...',
        'teacher': 'Mr. Rasool Vahdati',
        'category': 'Web'
    },
    {
        'id': 4,
        'name': 'Data Science',
        'description': 'Explore data analysis, visualization, and machine learning concepts.',
        'teacher': 'Dr. Carol Evans',
        'category': 'AI'
    },
    {
        'id': 5,
        'name': 'MLOps School',
        'description': 'Filoger MLOps for AI lovers',
        'teacher': 'Mr. Alipour',
        'category': 'AI'
    },
    {
        'id': 6,
        'name': 'Cybersecurity Fundamentals',
        'description': 'Understand the basics of cybersecurity practices and principles.',
        'teacher': 'Mr. Daniel Brown',
        'category': 'Security'
    }
]

# Get Unique Categories for filter in courses list
def get_unique_categories(courses):
    # Using a set to store unique categories
    unique_categories = set()

    for course in courses:
        # Add category to the set
        unique_categories.add(course['category'])

    # Convert the set back to a list if needed and return
    return list(unique_categories)

# Custom filter to limit words
def limit_words(text, num_words):
    words = text.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return text

# create jinja custom filter
app.jinja_env.filters['limit_words'] = limit_words

@app.route('/')
def Main():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def Profile():
    result = False
    if request.method == "POST":
        # Retrieve updated data from the form
        student_details['name'] = request.form['name']
        student_details['email'] = request.form['email']
        student_details['major'] = request.form['major']
        result = True

    # Redirect back to the profile page after updating
    return render_template('profile.html', student=student_details, result=result )

@app.route('/courses')
def Courses():
    return render_template('courses.html', courses=courses, categories=get_unique_categories(courses))

@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    # Finding the course with the given course_id
    course = next((course for course in courses if course['id'] == course_id), None)

    if course is None:
        # If the course is not found, return a 404 error
        abort(404)

    return render_template('course_detail.html', course=course)

@app.route('/add-course', methods=['GET', 'POST'])
def Add_Course():
    if request.method == 'POST':
        name = request.form.get('name').strip()  # Get name from form and strip whitespace
        teacher = request.form.get('teacher').strip()  # Get email from form and strip whitespace
        course_id = request.form.get('course')  # Get course ID from form
        description = request.form.get('description').strip()  # Get course ID from form

        # Validate input
        if not name or not teacher or not course_id or not description:
            error = "All fields are required."
            return render_template('add_course.html', courses=courses, categories=get_unique_categories(courses), error=error)

        # Create a new course entry (for demonstration; might require additional info)
        new_course = {
            'id': len(courses) + 1,
            'name': name,
            'description': description,  # You can also add these details
            'teacher': teacher,  # Using the email as the teacher for this example
            'category': course_id  # This should be associated with category (update logic based on your requirements)
        }

        # Add the new course to the courses list
        courses.append(new_course)

        return render_template('add_course.html', courses=courses, categories=get_unique_categories(courses), result=True)

    return render_template('add_course.html', courses=courses, categories=get_unique_categories(courses))

if __name__ == "__main__":
    app.run(debug=True)
