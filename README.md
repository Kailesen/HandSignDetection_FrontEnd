# HandSignDetection_FrontEnd
The front end layout for a sign language interpreter

To run the app you'll need to create a virtual environment, run the Backend "app.py", and then run the front-end dev. 
Make sure you're using a version of python between 3.9.0 to 3.11.09 (and have node.js and npm installed).

List of commands to run the app (and make sure everything is installed properly):

1. python -m venv .venv
2. .venv\Scripts\activate

(must be in "HandSignDetection_FrontEnd" from here on)

3. pip install --upgrade pip setuptools wheel
4. pip install -r requirements.txt

5. python Backend/app.py

(now in another terminal, still in the "HandSignDetection_FrontEnd" folder)

6. npm i
7. npm run dev