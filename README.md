# INF119-FP
# Team Members (Group 10): 
- Emily Liang 79453973
- Kristen Chung 42617410
- Kaomi Booker 85786904
- Angie Xetey 44067973 

## Dependencies
Please install these dependencies if you haven't already to run our UI:
- OpenAI
- Gradio
- Cryptography (might be needed for UI if LLM generates code that imports this library)

You can install them by running the following command:
```pip install openai gradio cryptography```

## How to Run the Program
The system should be run by either providing an OpenAI API key or setting the OpenAI API key as an environment variable to run all of the LLM processes. Once that is done, users can start the application by running main.py in their local terminal. This should start the Gradio UI running on a local url, specified in the terminal. 

After clicking on the local url link, the application UI should appear. This application UI should ask you for the app requirements, which are inputted by the user. Since our program is tailored specifically for the CyberDefender app, the UI will only work for that specific app. Once that is done, the requirements are submitted through the "Run Cyber Defender" button at the bottom, which then conducts the processes simulatenously to generate the parsed input, the app's code, the comprehensive test suite, the test results, and the tracking report. All you have to do to view those is to click on each tab as you need it, as the program will generate the items simultaneously.

## Returning the Code & Test Cases
Given that our system is automated since as soon as the user enters the requirements and clicks the run button, it runs all the processes, there are no separate tasks that the user must do to get the returned code and test cases. 
