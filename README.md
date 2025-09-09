# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory (frontend folder), you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.


# To Run Backend

In the backend directory activate your venv:

`.\venv\Scripts\activate'

Do the following installs:
1. `pip install Flask'
2. `pip install pycountry'
3. `pip install webcolors'

Then to run the backend:

`python server.py'

## Notes from the developer

There are several things that I understand are not perfect in this project and given more time I'd fix the following:

1. The function that splits the text from the preview to insert divs with the highlighted piece, does not work with the HTML lang missing error (currently bandaided to work)
2. I would like to change the 'Submit to see Results' placeholder to be an empty class while nothing has been submitted instead
3. Regarding the Color Contrast error, I am unsure of what consistitutes 'large text' so if given more robust requirements there, I could update the list of things it's checking for
4. Similarly for the Generic Link Text error, the only thing it's checking for is whether or not the link text is Click Here because I did not create a list of generic text options
5. Currently clicking on an error card analyzes one thing for markup-- If I had more time, I'd want to make it so that they stack (i.e. you click the Alternative Text error card and it highlights the img tag in yellow, then you click the Low Contrast error card and it highlights the tag in green so you have both highlights added to it and in different colors)
6. If I could do it all over from the start I'd change the design a bit:
    I'd want it to be a textarea, you enter in some html as text
    You hit submit, and the preview has all the errors pre-highlighted
    Then you can hover over those to see a small bubble with the details
    If you clicked the highlight, you could see the full error card on the right side

## Innovative Features

1. Dynamic Error Highlighting
    Each error card dynamically highlights its associated content in the preview area without disrupting the surrounding HTML structure.
    Where to find: frontend/src/App.js (see ErrorCard onClick function).

2. CSS Selector-Based Targeting
    Errors are mapped to precise elements in the DOM using CSS selectors, ensuring accurate and context-aware highlighting.
    Where to find: backend/errors.py (see build_selector) and frontend/src/app.js (see ErrorCard onClick function)

3. Modular and Reusable Architecture
    Functions like build_error() and build_selector() are designed to be modular, allowing easy integration into other accessibility tools.
    Where to find: backend/errors.py

4. Loading and Error Handling
    The system provides user feedback during data processing with a loading state (setLoading(true/false)) and clear error messages using setError(), which ensures the interface stays responsive and users are informed when issues occur during HTML analysis.
    Where to find: frontend/app.js (see App handleSubmit function)