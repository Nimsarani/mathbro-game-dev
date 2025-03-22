import sys
import random
import datetime
import webbrowser
import os

#Initialize global variable

global session_id
session_id = 0

def mode_selector():
    mode = ""
    
    if len(sys.argv) < 2:
        mode = "demo"
    else:
        #Map the arguments to respective modes
        if sys.argv[1] == "-e":
            mode = "easy"
        elif sys.argv[1] == "-m":
            mode = "medium"
        elif sys.argv[1] == "-h":
            mode = "hard"
        else:
            print("Invalid mode selected.")
            sys.exit() 
    
    return mode

def sys_configurations(mode):
    
    arithmatics = ["+"]
    start_range = 0
    end_range = 0
    number_of_questions = 0
    
    match mode:
        case "demo":
            start_range = 0
            end_range = 5
            number_of_questions = 3
        case "easy":
            start_range = 0
            end_range = 10
            number_of_questions = 5
            arithmatics.append("-")
        case "medium":
            start_range = 0
            end_range = 10
            number_of_questions = 10
            arithmatics.append("-")
        case "hard":
            start_range = 0
            end_range = 20
            number_of_questions = 10
            arithmatics.append("-")
            arithmatics.append("*")
            
    return arithmatics, start_range, end_range, number_of_questions,mode

def quection_generator(arithmatics, start_range, end_range, number_of_questions, mode):
    
    all_sessions = []
    global session_id
    
    while True:
        session_id = session_id + 1
        session = {"sessionId": session_id, "sessionData": [], "mode": mode,"Correct": 0, "Wrong": 0}
        correct = 0
        wrong = 0
        
        
        print(f"\n\nSession {session_id} Mathbro.\n\n")
        
        
        for i in range(number_of_questions):
            
            num1 = random.randint(start_range, end_range)
            num2 = random.randint(start_range, end_range)
            operator = random.choice(arithmatics)
            
            quection = f" | {i+1}) {num1} {operator} {num2} = ? "
            answer = answer_generator(num1, num2, operator)
            
            while True:
                try:
                    user_answer = int(input(quection))
                    break
                except ValueError:
                    print("Invalid input! Please enter a numeric value.")
                    
            if user_answer == (answer):
                result = "(√) You're answer is Correct! \n"
                mark = "√"
                txt_result = f"{mark} {quection} ={user_answer}"
                correct = correct + 1
                
            else:
                result = f"(X) You're answer is Wrong! correct answer is {str(answer)} \n"
                mark = "X"
                txt_result = f"{mark} {quection} = {user_answer}  Correct answer is {answer}"
                wrong = wrong + 1
            
            print(result)
            session["sessionData"].append([txt_result])
        #Update session status
        session["mode"] = mode
        session["Correct"] = correct
        session["Wrong"] = wrong
        
        all_sessions.append(session)
        print(f"Session {session_id} completed. Correct: {correct}, Wrong: {wrong}")
        
        
        another_session = input("Do you want to play another session? (y/n)")
        
        if another_session != "y":
            print("Thanks for playing!")
            break
        
    save_session_txt(all_sessions)
  
# Function to save session data to a text file
def save_session_txt(all_sessions):
    file_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{random.randint(100, 999)}.txt"

    with open(file_name, "w", encoding="utf-8") as file:
        file.write("MathBro Session\n")
        file.write("--------------------\n\n")
        
        file.write("Date : " + datetime.datetime.now().strftime("%Y-%m-%d") + "\n")
        file.write("Time : " + datetime.datetime.now().strftime("%H:%M") + "\n\n")
        
        # Write session details
        for session in all_sessions:
            
            file.write(f"Session ID: {session['sessionId']}\n")
            file.write("Results Sheet\n\n")
            
            for data in session['sessionData']:
                file.write(data[0] + "\n")
            
            file.write(f"\n\nMode: {session['mode']}\n")
            file.write(f"Total Questions: {len(session['sessionData'])}\n")
            file.write(f"Correct: {session['Correct']}\n")
            file.write(f"Wrong: {session['Wrong']}\n")
            file.write(f"Score: {session['Correct']*100 / len(session['sessionData']):.2f}\n")
            file.write("\n\n")
        
        print(f"Session saved as {file_name}")
        
    save_html_body(all_sessions)
    
# Function to save session data to an HTML file
def save_html_body(all_sessions):
    file_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{random.randint(100, 999)}.html"
    
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("<html>\n")
        file.write("<head>\n")
        file.write("<title>MathBro Session</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        
        file.write("<h1>MathBro Session</h1>\n")
        file.write("<hr>\n")
        
        file.write("<h2>Results</h2>\n")
        
        for session in all_sessions:
            file.write(f"<h3>Session ID: {session['sessionId']}</h3>\n")
            
            file.write("<h4>Results Sheet</h4>\n")
            file.write("<hr>\n")
            
            file.write(f"<p><b>Date : {datetime.datetime.now().strftime("%Y-%m-%d")}</b></p>\n")
            file.write(f"<p><b>Time : {datetime.datetime.now().strftime('%H:%M')}</b></p>\n")
                  
            
            file.write("<table border='1'>\n")
            file.write("<tr><th>Results</th></tr>\n")
            for data in session['sessionData']:
                file.write(f"<tr><td>{data[0]}</td></tr>\n")
            
            file.write("</table>\n")
            
            file.write(f"<p>Mode: {session['mode']}</p>\n")
            file.write(f"<p>Total Questions: {len(session['sessionData'])}</p>\n")
            file.write(f"<p>Correct: {session['Correct']}</p>\n")
            file.write(f"<p>Wrong: {session['Wrong']}</p>\n")
            file.write(f"<p>Score: {session['Correct']*100 / len(session['sessionData']):.2f}</p>\n")
            file.write("<hr>\n")
        
        file.write("</body>\n")
        file.write("</html>\n")
        
        file.close()
        
        # Ask if the user wants to open the file in a browser
        openHtmlDoc = input("Do you want to open the session in browser? (y/n)")
        if openHtmlDoc == "y":
            webbrowser.open(f"file://{os.path.realpath(file_name)}")
        
        
        print(f"Session saved as {file_name}")
        
# Function to calculate the answer for a question      
def answer_generator(num1, num2, operator):
    return eval(f"{num1} {operator} {num2}")

# Main function to start the program
def main():
    mode = mode_selector()
    arithmatics, start_range, end_range, number_of_questions, mode = sys_configurations(mode)
    quection_generator(arithmatics, start_range, end_range, number_of_questions, mode)
    
# Entry point of the program

if __name__ == "__main__":
    main()