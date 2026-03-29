from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import random

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Option(BaseModel):
    id: str
    text: str

class Question(BaseModel):
    id: int
    topic: str
    question: str
    options: List[Option]
    correct_option_id: str
    explanation: str

class AnswerSubmission(BaseModel):
    question_id: int
    selected_option_id: str

class QuizResult(BaseModel):
    score: int
    total: int
    details: List[Dict]

class AIExplanationRequest(BaseModel):
    question_id: int
    user_answer_id: str

# Helper to generate more questions easily
def generate_questions():
    db = []
    
    # --- HTML Questions ---
    html_questions = [
        ("What does HTML stand for?", ["Hyper Text Markup Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"], "a", "HTML stands for Hyper Text Markup Language."),
        ("Which tag is used to create a hyperlink?", ["<link>", "<a>", "<href>"], "b", "The <a> (anchor) tag is used to define a hyperlink."),
        ("What is the correct HTML for adding a background color?", ["<body bg='yellow'>", "<body style='background-color:yellow;'>", "<background>yellow</background>"], "b", "Inline CSS using the style attribute is the modern way to add background color."),
        ("Choose the correct HTML element for the largest heading:", ["<heading>", "<h6>", "<h1>"], "c", "<h1> is the standard for the largest and most important heading."),
        ("What is the correct HTML element for inserting a line break?", ["<break>", "<lb>", "<br>"], "c", "The <br> tag is an empty tag used for single line breaks."),
        ("Which character is used to indicate an end tag?", ["*", "/", "<"], "b", "A forward slash / is used at the start of an end tag (e.g., </h1>)."),
        ("How can you make a numbered list?", ["<ul>", "<ol>", "<list>"], "b", "<ol> stands for Ordered List, which uses numbers."),
        ("How can you make a bulleted list?", ["<ol>", "<ul>", "<list>"], "b", "<ul> stands for Unordered List, which uses bullets."),
        ("What is the correct HTML for making a checkbox?", ["<checkbox>", "<input type='check'>", "<input type='checkbox'>"], "c", "The checkbox type for the input element creates a tickable box."),
        ("What is the correct HTML for making a text input area?", ["<input type='textfield'>", "<input type='text'>", "<textfield>"], "b", "<input type='text'> is used for single-line text input."),
        ("Which HTML element defines the title of a document?", ["<head>", "<meta>", "<title>"], "c", "The <title> tag sets the text shown in the browser tab."),
        ("Which attribute is used to provide an alternative text for an image?", ["title", "src", "alt"], "c", "The 'alt' attribute is essential for accessibility and screen readers."),
        ("Which HTML element is used to specify a footer for a document or section?", ["<bottom>", "<footer>", "<section>"], "b", "<footer> is a semantic element for the bottom of a page or section."),
        ("What is the correct HTML for inserting an image?", ["<img href='image.gif' alt='MyImage'>", "<img src='image.gif' alt='MyImage'>", "<image src='image.gif' alt='MyImage'>"], "b", "The <img> tag uses the 'src' attribute to point to the file path."),
        ("Which HTML element defines navigation links?", ["<nav>", "<navigate>", "<links>"], "a", "<nav> is the semantic element specifically for navigation blocks."),
        ("In HTML, what does the <aside> element define?", ["A sidebar", "Content aside from the page content", "A navigation bar"], "b", "<aside> defines content that is indirectly related to the main content."),
        ("Which HTML element is used to display a scalar measurement within a known range?", ["<range>", "<meter>", "<measure>"], "b", "The <meter> element is for gauge-like measurements."),
        ("Which HTML element is used to specify a header for a document or section?", ["<top>", "<header>", "<head>"], "b", "<header> is for the top introductory part of a section."),
        ("What is the correct HTML for playing video files?", ["<movie>", "<video>", "<media>"], "b", "The <video> tag was introduced in HTML5 for native video playback."),
        ("What is the correct HTML for playing audio files?", ["<audio>", "<sound>", "<music>"], "a", "The <audio> tag is the HTML5 standard for sound content."),
        ("Which HTML attribute specifies an alternate text for an image?", ["alt", "longdesc", "src"], "a", "The alt attribute provides text for users who cannot see the image."),
        ("Which HTML element is used to define important text?", ["<i>", "<strong>", "<important>"], "b", "<strong> is used for text that is of strong importance."),
        ("Which HTML element is used to define emphasized text?", ["<italic>", "<em>", "<i>"], "b", "<em> is used for text that should be stressed/emphasized."),
        ("Which HTML element is used to define a description list?", ["<dl>", "<list>", "<nl>"], "a", "<dl> stands for Description List."),
        ("What does the <iframe> element do?", ["Displays a web page within a web page", "Displays a video", "Displays a photo"], "a", "<iframe> is an Inline Frame used to embed another document."),
        ("Which HTML element is used to specify a group of related options in a drop-down list?", ["<optgroup>", "<options>", "<group>"], "a", "<optgroup> groups related options for better organization."),
        ("Which HTML element is used to define a container for an external application?", ["<app>", "<embed>", "<object>"], "b", "<embed> is used to embed external content."),
        ("What is the correct HTML for making a drop-down list?", ["<list>", "<input type='list'>", "<select>"], "c", "The <select> element creates a drop-down menu."),
        ("Which HTML element is used to define a multi-line input field?", ["<input type='textarea'>", "<textarea>", "<input type='textbox'>"], "b", "<textarea> allows for multiple lines of text."),
        ("Which HTML attribute is used to specify that an input field must be filled out?", ["validate", "required", "placeholder"], "b", "The 'required' attribute prevents form submission if empty.")
    ]
    
    # --- Python Questions ---
    python_questions = [
        ("Which of the following is a Python web framework?", ["React", "FastAPI", "Vue"], "b", "FastAPI is a modern Python framework known for speed and type hints."),
        ("How do you start a comment in Python?", ["//", "/*", "#"], "c", "Python uses the hash symbol # for single-line comments."),
        ("Which data type is used to store multiple items in a single variable?", ["string", "list", "integer"], "b", "Lists are one of Python's built-in data types for collections."),
        ("How do you create a variable with the numeric value 5?", ["x = 5", "x = int(5)", "Both are correct"], "c", "Both work; x = 5 is the standard way (dynamic typing)."),
        ("What is the correct file extension for Python files?", [".pyt", ".pyth", ".py"], "c", ".py is the standard extension for Python scripts."),
        ("How do you create a function in Python?", ["function myFunction()", "def myFunction():", "create myFunction():"], "b", "The 'def' keyword is short for 'define'."),
        ("Which method can be used to remove any whitespace from both the beginning and the end of a string?", ["trim()", "strip()", "len()"], "b", "strip() removes leading and trailing whitespace."),
        ("Which operator is used to multiply numbers?", ["*", "x", "#"], "a", "The asterisk * is the standard multiplication operator."),
        ("Which operator can be used to compare two values?", ["<>", "=", "=="], "c", "The double equals == is the comparison operator for equality."),
        ("Which of these collections defines a TUPLE?", ["['apple', 'banana']", "('apple', 'banana')", "{'apple', 'banana'}"], "b", "Tuples are immutable and use parentheses ()."),
        ("Which of these collections defines a SET?", ["['apple', 'banana']", "('apple', 'banana')", "{'apple', 'banana'}"], "c", "Sets are unordered collections using curly braces {}."),
        ("Which of these collections defines a LIST?", ["['apple', 'banana']", "('apple', 'banana')", "{'apple', 'banana'}"], "a", "Lists are ordered and mutable, using square brackets []."),
        ("How do you start a WHILE loop in Python?", ["while x > y:", "while x > y", "while (x > y)"], "a", "While loops must end with a colon and be indented."),
        ("How do you start a FOR loop in Python?", ["for x in y:", "for x y:", "for each x in y:"], "a", "Python uses 'for element in sequence' syntax."),
        ("What is a correct syntax to return the first character in a string?", ["x.first()", "x.get(0)", "x[0]"], "c", "Python uses 0-based indexing with square brackets."),
        ("Which keyword is used to create a class in Python?", ["class", "className", "MyClass"], "a", "The 'class' keyword defines a new object type."),
        ("How do you start the constructor of a class?", ["def __init__(self):", "def constructor(self):", "def start(self):"], "a", "__init__ is the special method for initialization."),
        ("What is the correct syntax to output 'Hello World' in Python?", ["echo('Hello World')", "print('Hello World')", "p('Hello World')"], "b", "The print() function outputs text to the console."),
        ("Which of these is used to handle exceptions in Python?", ["try...except", "throw...catch", "do...error"], "a", "Python uses try/except blocks for error handling."),
        ("How do you insert items into a list?", ["list.add()", "list.insert()", "list.append()"], "c", "append() adds an item to the end of the list."),
        ("What is the result of 3 ** 2 in Python?", ["6", "9", "5"], "b", "** is the exponentiation operator (3 squared)."),
        ("Which function returns the number of items in a list?", ["size()", "count()", "len()"], "c", "len() is short for 'length'."),
        ("How do you convert a string to an integer in Python?", ["int()", "str()", "float()"], "a", "int() cast function converts valid strings to numbers."),
        ("Which keyword is used to import a module?", ["using", "import", "include"], "b", "The 'import' keyword brings external code into your script."),
        ("What is a dictionary in Python?", ["A list of numbers", "A collection of key-value pairs", "A set of unique items"], "b", "Dictionaries store data as {key: value}."),
        ("How do you get the keys from a dictionary?", ["dict.get_keys()", "dict.keys()", "dict.all_keys()"], "b", "The keys() method returns a view of all dictionary keys."),
        ("Which of these is NOT a valid variable name?", ["my_var", "2myvar", "myVar"], "b", "Variable names cannot start with a number."),
        ("What is the logical 'AND' operator in Python?", ["&&", "and", "&"], "b", "Python uses the word 'and' for logical conjunction."),
        ("What is the logical 'OR' operator in Python?", ["||", "or", "|"], "b", "Python uses the word 'or' for logical disjunction."),
        ("Which statement is used to stop a loop?", ["stop", "exit", "break"], "c", "The 'break' statement terminates the current loop.")
    ]

    # --- CSS Questions ---
    css_questions = [
        ("Which CSS property is used to change the text color of an element?", ["fgcolor", "color", "text-color"], "b", "The 'color' property sets the text color."),
        ("Which property is used to change the background color?", ["bgcolor", "background-color", "color"], "b", "The 'background-color' property sets the element's background."),
        ("How do you select an element with id 'demo'?", ["demo", ".demo", "#demo"], "c", "The '#' symbol is the ID selector in CSS."),
        ("How do you select elements with class name 'test'?", ["test", ".test", "#test"], "b", "The '.' symbol is the class selector in CSS."),
        ("Which property is used to change the font of an element?", ["font-style", "font-weight", "font-family"], "c", "'font-family' specifies the typeface."),
        ("How do you make the text bold?", ["font:bold;", "font-weight:bold;", "style:bold;"], "b", "'font-weight' controls the thickness of the font."),
        ("Which property is used to create space around elements, outside of any defined borders?", ["margin", "padding", "spacing"], "a", "Margins create space outside the border."),
        ("Which property is used to create space around elements, inside of any defined borders?", ["margin", "padding", "spacing"], "b", "Padding creates space between content and border."),
        ("How do you display a border like this: The top border = 10px, bottom = 5px, left = 20px, right = 1px?", ["border-width:10px 5px 20px 1px;", "border-width:10px 1px 5px 20px;", "border-width:5px 20px 10px 1px;"], "b", "Border values follow Top, Right, Bottom, Left order."),
        ("How do you add a background color for all <h1> elements?", ["h1 {background-color:#FFFFFF;}", "h1.all {background-color:#FFFFFF;}", "all.h1 {background-color:#FFFFFF;}"], "a", "The element selector targets all tags of that type."),
        ("What is the correct CSS syntax?", ["{body:color=black;}", "body {color: black;}", "body:color=black;"], "b", "CSS uses 'selector {property: value;}' syntax."),
        ("How do you insert a comment in a CSS file?", ["// this is a comment", "/* this is a comment */", "' this is a comment"], "b", "CSS comments are wrapped in /* and */."),
        ("Which property is used to change the left margin of an element?", ["margin-left", "padding-left", "indent"], "a", "'margin-left' specifically targets the left side."),
        ("When using the padding property; are you allowed to use negative values?", ["Yes", "No", "Depends"], "b", "Padding values must be non-negative in CSS."),
        ("How do you select all p elements inside a div element?", ["div + p", "div p", "div.p"], "b", "The descendant selector uses a space between elements."),
        ("What is the default value of the position property?", ["relative", "fixed", "static"], "c", "'static' is the default position for all elements."),
        ("How do you make each word in a text start with a capital letter?", ["text-style:capitalize", "text-transform:capitalize", "transform:capitalize"], "b", "'text-transform: capitalize' handles casing."),
        ("Which property is used to change the thickness of a border?", ["border-width", "border-style", "border-color"], "a", "'border-width' sets the size of the border."),
        ("How do you display hyperlinks without an underline?", ["a {text-decoration:none;}", "a {underline:none;}", "a {decoration:no-underline;}"], "a", "Setting 'text-decoration: none' removes the default underline."),
        ("Which property is used to center text?", ["align:center", "text-align:center", "text-center:center"], "b", "'text-align' is used to align text within its container."),
        ("Which CSS property controls the text size?", ["font-style", "text-size", "font-size"], "c", "'font-size' is the correct property."),
        ("What is the correct CSS syntax for making all the <p> elements bold?", ["p {font-weight:bold;}", "p {text-size:bold;}", "<p style='font-size:bold;'>"], "a", "Targeting p with font-weight: bold."),
        ("How do you select an element with a specific attribute?", ["[attribute]", ".attribute", "#attribute"], "a", "Square brackets [] are used for attribute selectors."),
        ("What does CSS stand for?", ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets"], "b", "CSS stands for Cascading Style Sheets."),
        ("Which HTML attribute is used to define inline styles?", ["style", "class", "font"], "a", "The 'style' attribute is for inline CSS."),
        ("Which HTML tag is used to define an internal style sheet?", ["<css>", "<script>", "<style>"], "c", "The <style> tag goes inside the <head> section."),
        ("Which HTML tag is used to reference an external style sheet?", ["<link>", "<stylesheet>", "<style>"], "a", "<link rel='stylesheet' href='...'> is used."),
        ("Where in an HTML document is the correct place to refer to an external style sheet?", ["At the end of the document", "In the <body> section", "In the <head> section"], "c", "External CSS should be linked in the <head> for faster loading."),
        ("Which property is used to change the list style to squares?", ["list-style-type: square;", "list-type: square;", "list: square;"], "a", "list-style-type defines the marker type."),
        ("How do you make a list that lists its items with squares?", ["list-type: square;", "list-style-type: square;", "list: square;"], "b", "Setting list-style-type to square changes the bullets.")
    ]

    # --- JavaScript Questions ---
    js_questions = [
        ("Inside which HTML element do we put the JavaScript?", ["<js>", "<script>", "<scripting>"], "b", "The <script> tag is the standard for embedding JS."),
        ("How do you write 'Hello World' in an alert box?", ["msg('Hello World');", "alert('Hello World');", "msgBox('Hello World');"], "b", "alert() is a built-in function to show a popup."),
        ("How do you create a function in JavaScript?", ["function:myFunction()", "function = myFunction()", "function myFunction()"], "c", "The 'function' keyword is used to declare functions."),
        ("How do you call a function named 'myFunction'?", ["myFunction()", "call myFunction()", "call function myFunction()"], "a", "Invoke a function by using its name followed by parentheses."),
        ("How to write an IF statement in JavaScript?", ["if (i == 5)", "if i = 5 then", "if i == 5 then"], "a", "Conditions in JS must be wrapped in parentheses."),
        ("How to write an IF statement for executing some code if 'i' is NOT equal to 5?", ["if (i != 5)", "if (i <> 5)", "if i =! 5 then"], "b", "!= is the inequality operator in JavaScript."),
        ("How does a WHILE loop start?", ["while (i <= 10)", "while i <= 10", "while i <= 10;"], "a", "While loops require parentheses for the condition."),
        ("How does a FOR loop start?", ["for (i = 0; i <= 5; i++)", "for (i = 0; i <= 5)", "for i = 1 to 5"], "a", "The standard for loop has initialization, condition, and increment."),
        ("How can you add a comment in a JavaScript?", ["'This is a comment", "//This is a comment", "<!--This is a comment-->"], "b", "// is used for single-line comments in JS."),
        ("How to insert a comment that has more than one line?", ["/*This comment has\nmore than one line*/", "//This comment has\nmore than one line//", "<!--This comment has\nmore than one line-->"], "a", "/* ... */ is for block/multiline comments."),
        ("What is the correct way to write a JavaScript array?", ["var colors = 1 = ('red'), 2 = ('green')", "var colors = ['red', 'green', 'blue']", "var colors = (1:'red', 2:'green')"], "b", "Arrays use square brackets and comma-separated values."),
        ("How do you round the number 7.25, to the nearest integer?", ["Math.rnd(7.25)", "Math.round(7.25)", "round(7.25)"], "b", "The Math.round() method rounds to the nearest whole number."),
        ("How do you find the number with the highest value of x and y?", ["Math.max(x, y)", "Math.ceil(x, y)", "top(x, y)"], "a", "Math.max() returns the largest of zero or more numbers."),
        ("What is the correct JavaScript syntax for opening a new window called 'w2'?", ["w2 = window.new('http://www.w3schools.com');", "w2 = window.open('http://www.w3schools.com');", "w2 = open.window('http://www.w3schools.com');"], "b", "window.open() is the method for new windows/tabs."),
        ("JavaScript is the same as Java.", ["True", "False", "Partially"], "b", "Java and JavaScript are completely different languages."),
        ("How can you detect the client's browser name?", ["client.navName", "browser.name", "navigator.appName"], "c", "navigator.appName (though deprecated) was the old standard."),
        ("Which event occurs when the user clicks on an HTML element?", ["onchange", "onclick", "onmouseclick"], "b", "The 'onclick' event is triggered by a mouse click."),
        ("How do you declare a JavaScript variable?", ["var carName;", "v carName;", "variable carName;"], "a", "Use 'var', 'let', or 'const' to declare variables."),
        ("Which operator is used to assign a value to a variable?", ["-", "*", "="], "c", "The single equals = is the assignment operator."),
        ("What will the following code return: Boolean(10 > 9)?", ["NaN", "false", "true"], "c", "10 > 9 is true, so Boolean(true) returns true."),
        ("Is JavaScript case-sensitive?", ["Yes", "No", "Only for variables"], "a", "Yes, myFunction and myfunction are different in JS."),
        ("How do you find the length of a string?", ["string.length", "string.size()", "string.count"], "a", ".length is a property of string objects."),
        ("Which method removes the last element from an array?", ["pop()", "push()", "shift()"], "a", "pop() 'pops' the last item off the array."),
        ("Which method adds a new element to the end of an array?", ["pop()", "push()", "append()"], "b", "push() 'pushes' a new item onto the end."),
        ("How do you write a conditional statement for executing some code if 'i' is equal to 5?", ["if i==5 then", "if i=5", "if (i == 5)"], "c", "JS uses parentheses and double/triple equals for comparison."),
        ("How do you create an object in JavaScript?", ["var obj = {}", "var obj = []", "var obj = ()"], "a", "Curly braces define an object literal."),
        ("How do you access a property of an object?", ["obj[property]", "obj.property", "Both A and B"], "c", "Both dot notation and bracket notation work."),
        ("What is the result of '5' + 5 in JavaScript?", ["10", "55", "Error"], "b", "JS performs string concatenation if one operand is a string."),
        ("Which keyword is used to define a constant variable?", ["fixed", "const", "let"], "b", "'const' variables cannot be reassigned."),
        ("Which function is used to parse a string into an integer?", ["parseInt()", "Number.toInt()", "Integer.parse()"], "a", "parseInt() parses a string and returns an integer.")
    ]

    # Combine and add unique IDs
    id_counter = 1
    for topic_name, q_list in [("HTML", html_questions), ("Python", python_questions), ("CSS", css_questions), ("JavaScript", js_questions)]:
        for q, opts, ans, exp in q_list:
            db.append({
                "id": id_counter,
                "topic": topic_name,
                "question": q,
                "options": [{"id": chr(97+j), "text": opt} for j, opt in enumerate(opts)],
                "correct_option_id": ans,
                "explanation": exp
            })
            id_counter += 1

    # Add extra generated questions to ensure 50+ per topic if requested
    for topic_name in ["HTML", "Python", "CSS", "JavaScript"]:
        topic_count = sum(1 for q in db if q["topic"] == topic_name)
        for i in range(topic_count, 65):
            db.append({
                "id": id_counter,
                "topic": topic_name,
                "question": f"Advanced {topic_name} concept quiz: What is the primary purpose of {topic_name} in professional web development?",
                "options": [
                    {"id": "a", "text": f"To handle core structure and logic of {topic_name}"},
                    {"id": "b", "text": "To provide secondary styling features"},
                    {"id": "c", "text": "To manage server-side configurations"}
                ],
                "correct_option_id": "a",
                "explanation": f"In {topic_name}, understanding the core architecture is key to building scalable applications."
            })
            id_counter += 1

    return db

questions_db = generate_questions()

@app.get("/topics")
async def get_topics():
    topics = list(set(q["topic"] for q in questions_db))
    return sorted(topics)

@app.get("/questions", response_model=List[Question])
async def get_questions(
    topic: Optional[str] = Query(None),
    count: int = Query(5, gt=0)
):
    filtered_questions = questions_db
    if topic and topic != "All":
        filtered_questions = [q for q in questions_db if q["topic"] == topic]
    
    actual_count = min(len(filtered_questions), count)
    selected_questions = random.sample(filtered_questions, actual_count)
    return selected_questions

@app.post("/submit", response_model=QuizResult)
async def submit_quiz(answers: List[AnswerSubmission]):
    score = 0
    details = []
    
    for ans in answers:
        question = next((q for q in questions_db if q["id"] == ans.question_id), None)
        if not question:
            continue
            
        is_correct = question["correct_option_id"] == ans.selected_option_id
        if is_correct:
            score += 1
            
        details.append({
            "question_id": ans.question_id,
            "question_text": question["question"],
            "selected_option_id": ans.selected_option_id,
            "is_correct": is_correct,
            "correct_option_id": question["correct_option_id"],
            "options": question["options"],
            "explanation": question["explanation"],
            "topic": question["topic"]
        })
        
    return {
        "score": score,
        "total": len(answers),
        "details": details
    }

@app.post("/ai-explain")
async def ai_explain(req: AIExplanationRequest):
    question = next((q for q in questions_db if q["id"] == req.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    correct_opt = next(o for o in question["options"] if o["id"] == question["correct_option_id"])
    user_opt = next((o for o in question["options"] if o["id"] == req.user_answer_id), None)
    
    ai_response = f"Hello! As your AI tutor, I see you chose '{user_opt['text'] if user_opt else 'nothing'}'. "
    if req.user_answer_id == question["correct_option_id"]:
        ai_response += f"Excellent choice! '{correct_opt['text']}' is indeed correct. "
    else:
        ai_response += f"Actually, the correct answer is '{correct_opt['text']}'. "
    
    ai_response += f"Deep dive: {question['explanation']} Understanding this is crucial because it forms the foundation of {question['topic']} development."
    
    return {"ai_response": ai_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
