# The Destiny Resume #
## Summary ##
This is a tool to create a resume based on various destiny 2 stats, such as raids, dungeons, and titles. It was made as a fun side project.
The tool leverages the bungie API to get information about the player, translates and formats it, then sends it to gemini to create a summary.
It now includes an actual GUI for the user to use instead of just creating a text file.
This is the version I aim to use for a frontend; it has been reconfigured from the original to not require a login.

## Necessities ##
You will have to get an API Key from bungie in order to make requests. To do this:
1. Go to Bungie.net and sign in.
2. Scroll down and go to the developer portal.
3. Press "Create New App"
5. Set the following environmental variables (left is environmental variable name, right is what you should set it to from the page):
* bungie_token=your API Key
Next, you will need to also get an API Key for gemini.
1. Follow this link: https://ai.google.dev/gemini-api/docs/api-key.
2. Press "Get an API Key."
3. Set the following environmental variable: 
* GOOGLE_API_KEY=your api key
This assumes you have the knowledge to create a python environment using the included environment.yml file and use it to run the program.
4. Finally, set the redirect URL. The redirect URL in grabbers.py is set as google.com. If you want to use that, just set the redirect URL in your application page to google.com.
5. If you want to use a different one you will also have to change the "placeholder_redirect" variable in grabbers.py to match.

## Using the Tool ##
Once you have all of the environmental variables set, simply run main.py; it will host in your browser at localhost:8080 (by default).

## Misc ##
The code isn't perfect; the translator.py file function is very rough. There are a few adjustments and additions I would like to make and will try to make in the future. I currently want to add:
* A function to generate endpoint urls instead of just calling the url specifically in each grabber function.
* Cleaner code... (always)
