# Recipe-Bot
This is my first project . It will create a chatbot which will generate recipes of different dishes which the user will input
**What I learned:-**
1) I learnt how to use the streamlit library to create webpages.
2) I learned how to create chatbots and use multiple models in a single application
3) I learned how to give prompts to our models and generate structured outputs


**Which model performed better:-**
In a happy scenario , both models work fine and provide the correct recipes .
However if we enter any junk input or random input , Gemini recognizes the junk input and returns the recipe of a dish matching the keywords. It also displays that it is not a proper dish and is a visual thing only (if its not edible).
Meanwhile LlaMa 3 ignores the workds which are not relevant and prepares a dish based on the left words.