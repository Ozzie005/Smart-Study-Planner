import os

# Load previously saved study sessions from the file
def load_sessions():
    sessions = []
    if not os.path.exists("study_log.txt"):
        return sessions
    try:
        with open("study_log.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) == 4:
                        session = {
                            "subject": parts[0],
                            "topic": parts[1],
                            "day": parts[2],
                            "duration": float(parts[3])
                        }
                        sessions.append(session)
    except (IOError, ValueError):
        print("Error loading saved sessions.")
    return sessions

# Save all study sessions to the text file
def save_sessions(sessions):
    try:
        with open("study_log.txt", "w") as file:
            for session in sessions:
                file.write(
                    session["subject"] + "|" +
                    session["topic"] + "|" +
                    session["day"] + "|" +
                    str(session["duration"]) + "\n"
                )
        print("\nStudy sessions saved successfully.")
    except IOError:
        print("Error saving study sessions.")

# Classify a study session according to its duration
def classify_session(duration):
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"

# Add a new study session to the list
def add_session(sessions):
    print("\n--- ADD A STUDY SESSION ---")
    subject = input("Enter subject name: ")
    topic = input("Enter topic covered: ")
    day = input("Enter date or day label: ")
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))
            if duration > 0:
                break
            else:
                print("Duration must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a positive number.")
    session = {
        "subject": subject,
        "topic": topic,
        "day": day,
        "duration": duration
    }
    sessions.append(session)
    print("\nStudy session added successfully!")

# Display all recorded study sessions
def view_sessions(sessions):
    print("\n--- ALL STUDY SESSIONS ---")
    if not sessions:
        print("No study sessions have been recorded yet.")
        return
    print("-" * 85)
    print(f"{'Subject':<20}{'Topic':<25}{'Duration':<15}{'Classification':<15}")
    print("-" * 85)
    for session in sessions:
        classification = classify_session(session["duration"])
        print(f"{session['subject']:<20}{session['topic']:<25}{session['duration']:<15.1f}{classification:<15}")
    print("-" * 85)

# Search for study sessions using the subject name
def search_by_subject(sessions, subject):
    found_sessions = []
    for session in sessions:
        if session["subject"].lower() == subject.lower():
            found_sessions.append(session)
    print("\n--- SEARCH RESULTS ---")
    if not found_sessions:
        print(f"No study sessions found for '{subject}'.")
        return
    total_minutes = 0
    print("-" * 85)
    print(f"{'Subject':<20}{'Topic':<25}{'Duration':<15}{'Classification':<15}")
    print("-" * 85)
    for session in found_sessions:
        classification = classify_session(session["duration"])
        total_minutes += session["duration"]
        print(f"{session['subject']:<20}{session['topic']:<25}{session['duration']:<15.1f}{classification:<15}")
    print("-" * 85)
    print(f"Total time spent on {subject}: {total_minutes:.1f} minutes")
    print(f"Total hours: {total_minutes / 60:.2f} hours")

# Calculate and display overall study statistics
def study_statistics(sessions):
    print("\n--- STUDY STATISTICS ---")
    if not sessions:
        print("No study sessions available for statistics.")
        return
    total_minutes = 0
    subject_totals = {}
    for session in sessions:
        total_minutes += session["duration"]
        subject = session["subject"]
        if subject in subject_totals:
            subject_totals[subject] += session["duration"]
        else:
            subject_totals[subject] = session["duration"]
    total_hours = total_minutes / 60
    print(f"\nTotal study time overall: {total_hours:.2f} hours")
    print("\nTotal study time per subject:")
    for subject, minutes in subject_totals.items():
        hours = minutes / 60
        print(f"{subject}: {minutes:.1f} minutes ({hours:.2f} hours)")
    weakest_subject = min(subject_totals, key=subject_totals.get)
    weakest_time = subject_totals[weakest_subject]
    print(f"\nWeakest area: {weakest_subject} ({weakest_time:.1f} minutes)")
    longest_session = max(sessions, key=lambda session: session["duration"])
    print("\nLongest single study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Duration: {longest_session['duration']:.1f} minutes")
    print(f"Classification: {classify_session(longest_session['duration'])}")

# Main function that controls the menu and program flow
def main():
    sessions = load_sessions()
    print("=" * 45)
    print("       WELCOME TO SMART STUDY PLANNER")
    print("=" * 45)
    while True:
        print("\nMENU")
        print("1. Add a Study Session")
        print("2. View All Sessions")
        print("3. Search Sessions by Subject")
        print("4. View Statistics")
        print("5. Save and Exit")
        choice = input("\nEnter your choice (1-5): ")
        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject = input("Enter the subject to search for: ")
            search_by_subject(sessions, subject)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("\nThank you for using the Smart Study Planner!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 5.")

# Run the main program
if __name__ == "__main__":
    main()