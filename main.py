import mysql.connector
from datetime import date,datetime

# Database connection
def connect():
    return mysql.connector.connect(
        host='localhost',
        database='production_media',
        user='root',
        password=''
    )

# Define existing functions here: add_series, add_employee, etc., from the previous code
# Function to add a new series
def add_series(series_name, reviews, budget, production_id, genre_type):
    conn = connect()
    cursor = conn.cursor()
    sql = """INSERT INTO Series (SeriesName, Reviews, Budget, production_id, genre_type)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (series_name, reviews, budget, production_id, genre_type))
    conn.commit()
    print(f"Series '{series_name}' added successfully.")
    conn.close()

# Function to add a new employee to a department
def add_employee(first_name, last_name, middle_name, dob, department_id, series_id=None):
    conn = connect()
    cursor = conn.cursor()
    sql = """INSERT INTO Employees (first_name, last_name, middle_name, DOB, department_id, SeriesId)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (first_name, last_name, middle_name, dob, department_id, series_id))
    conn.commit()
    print(f"Employee '{first_name} {last_name}' added successfully.")
    conn.close()

# Function to assign an employee to a specific series
def assign_employee_to_series(emp_id, series_id):
    conn = connect()
    cursor = conn.cursor()
    sql = "UPDATE Employees SET SeriesId = %s WHERE emp_id = %s"
    cursor.execute(sql, (series_id, emp_id))
    conn.commit()
    print(f"Employee ID {emp_id} assigned to Series ID {series_id}.")
    conn.close()

# Function to manage grievances for employees
def add_grievance(emp_id, grievance_text):
    conn = connect()
    cursor = conn.cursor()
    sql = """INSERT INTO Grievances (emp_id, grievances_text)
             VALUES (%s, %s)"""
    cursor.execute(sql, (emp_id, grievance_text))
    conn.commit()
    print(f"Grievance added for Employee ID {emp_id}.")
    conn.close()

# Function to view all grievances for a production team
def view_grievances():
    conn = connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM Grievances"
    cursor.execute(sql)
    grievances = cursor.fetchall()
    print("Grievances List:")
    for grievance in grievances:
        print(f"Employee ID: {grievance[0]}, Grievance: {grievance[1]}")
    conn.close()

# Function to manage a series release
def release_series(series_id, platform, release_date):
    try:
        # Validate date format
        try:
            # Convert release_date to a proper date format (if it's a string)
            release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use 'YYYY-MM-DD'.")
            return
        
        # Connect to the database
        conn = connect()
        cursor = conn.cursor()

        # Insert into ReleaseGroup table
        sql = """INSERT INTO releaSegroup (SeriesID, Platform, ReleaseDate)
                 VALUES (%s, %s, %s)"""
        cursor.execute(sql, (series_id, platform, release_date))
        conn.commit()
        
        print(f"Series ID {series_id} scheduled for release on {platform} at {release_date}.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Close the connection
        conn.close()

# Function to get a summary of series production
def series_summary():
    conn = connect()
    cursor = conn.cursor()
    sql = """SELECT Series.SeriesId, Series.SeriesName, Productions.production_firm, Series.Budget, Series.genre_type
             FROM Series
             INNER JOIN Productions ON Series.production_id = Productions.production_id"""
    cursor.execute(sql)
    series = cursor.fetchall()
    print("Series Summary:")
    for s in series:
        print(f"Series ID: {s[0]}, Name: {s[1]}, Production Firm: {s[2]}, Budget: {s[3]}, Genre: {s[4]}")
    conn.close()

# Function to find employees in a specific department
def find_employees_by_department(department_id):
    conn = connect()
    cursor = conn.cursor()
    sql = """SELECT emp_id, first_name, last_name
             FROM Employees
             WHERE department_id = %s"""
    cursor.execute(sql, (department_id,))
    employees = cursor.fetchall()
    print(f"Employees in Department ID {department_id}:")
    for emp in employees:
        print(f"ID: {emp[0]}, Name: {emp[1]} {emp[2]}")
    conn.close()

# Function to update series budget
def update_series_budget(series_id, new_budget):
    conn = connect()
    cursor = conn.cursor()
    sql = "UPDATE Series SET Budget = %s WHERE SeriesId = %s"
    cursor.execute(sql, (new_budget, series_id))
    conn.commit()
    print(f"Series ID {series_id} budget updated to {new_budget}.")
    conn.close()

# New Function to add a new series along with its initial cast
def add_series_with_cast():
    series_name = input("Enter series name: ")
    reviews = input("Enter series reviews: ")
    budget = float(input("Enter series budget: "))
    production_id = int(input("Enter production ID: "))
    genre_type = input("Enter genre type: ")

    conn = connect()
    cursor = conn.cursor()

    # Insert the new series
    sql_series = """INSERT INTO Series (SeriesName, Reviews, Budget, production_id, genre_type)
                    VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql_series, (series_name, reviews, budget, production_id, genre_type))
    series_id = cursor.lastrowid  # Get the ID of the newly added series

    # Adding initial cast members
    while True:
        add_cast = input("Do you want to add a cast member for this series? (y/n): ").strip().lower()
        if add_cast == 'n':
            break
        emp_id = int(input("Enter employee ID for cast member: "))
        num_of_episodes = int(input("Enter number of episodes: "))
        name_in_series = input("Enter character name in series: ")

        sql_cast = """INSERT INTO Cast (emp_id, num_of_episodes, name_in_series) 
                      VALUES (%s, %s, %s)"""
        cursor.execute(sql_cast, (emp_id, num_of_episodes, name_in_series))

    conn.commit()
    print(f"Series '{series_name}' added successfully with initial cast members.")
    conn.close()

# Function to add crew members to a series
def add_crew_member():
    emp_id = int(input("Enter employee ID for crew member: "))
    contract_duration = int(input("Enter contract duration in months: "))
    designation = input("Enter crew member designation (e.g., Director, Producer): ")
    
    conn = connect()
    cursor = conn.cursor()
    sql = """INSERT INTO CrewMembers (emp_id, contract_duration, designation)
             VALUES (%s, %s, %s)"""
    cursor.execute(sql, (emp_id, contract_duration, designation))
    conn.commit()
    print(f"Crew member with Employee ID {emp_id} added successfully as '{designation}'.")
    conn.close()

# Function to view the full cast and crew of a series
def view_series_cast_crew():
    series_id = int(input("Enter series ID: "))
    conn = connect()
    cursor = conn.cursor()
    
    print("\n--- Cast Members ---")
    sql_cast = """SELECT c.cast_id, e.first_name, e.last_name, c.name_in_series, c.num_of_episodes
                  FROM Cast c
                  JOIN Employees e ON c.emp_id = e.emp_id
                  WHERE e.SeriesId = %s"""
    cursor.execute(sql_cast, (series_id,))
    cast_members = cursor.fetchall()
    for cast in cast_members:
        print(f"ID: {cast[0]}, Name: {cast[1]} {cast[2]}, Character: {cast[3]}, Episodes: {cast[4]}")
    
    print("\n--- Crew Members ---")
    sql_crew = """SELECT cr.crew_member_id, e.first_name, e.last_name, cr.designation, cr.contract_duration
                  FROM CrewMembers cr
                  JOIN Employees e ON cr.emp_id = e.emp_id
                  WHERE e.SeriesId = %s"""
    cursor.execute(sql_crew, (series_id,))
    crew_members = cursor.fetchall()
    for crew in crew_members:
        print(f"ID: {crew[0]}, Name: {crew[1]} {crew[2]}, Designation: {crew[3]}, Contract: {crew[4]} months")
    
    conn.close()

# Function to update the release status of a series
def update_release_status():
    series_id = int(input("Enter series ID: "))
    platform = input("Enter platform name (e.g., Netflix, HBO): ")
    release_date = input("Enter release date (yyyy-mm-dd): ")

    conn = connect()
    cursor = conn.cursor()
    sql = """UPDATE ReleaseGroup
             SET Platform = %s, ReleaseDate = %s
             WHERE SeriesID = %s"""
    cursor.execute(sql, (platform, release_date, series_id))
    conn.commit()
    print(f"Release status updated for Series ID {series_id} on {platform} at {release_date}.")
    conn.close()

# Function to search for series by genre
def search_series_by_genre():
    genre = input("Enter genre to search for (e.g., Fantasy, Drama): ")
    conn = connect()
    cursor = conn.cursor()
    sql = """SELECT SeriesId, SeriesName, Budget, Reviews
             FROM Series
             WHERE genre_type = %s"""
    cursor.execute(sql, (genre,))
    series = cursor.fetchall()
    print(f"Series under genre '{genre}':")
    for s in series:
        print(f"ID: {s[0]}, Name: {s[1]}, Budget: {s[2]}, Reviews: {s[3]}")
    conn.close()

# Function to view all series by a particular production firm
def view_series_by_production_firm():
    production_firm = input("Enter production firm name: ")
    conn = connect()
    cursor = conn.cursor()
    sql = """SELECT s.SeriesId, s.SeriesName, s.Budget, s.genre_type
             FROM Series s
             JOIN Productions p ON s.production_id = p.production_id
             WHERE p.production_firm = %s"""
    cursor.execute(sql, (production_firm,))
    series = cursor.fetchall()
    print(f"Series produced by '{production_firm}':")
    for s in series:
        print(f"ID: {s[0]}, Name: {s[1]}, Budget: {s[2]}, Genre: {s[3]}")
    conn.close()

# Display the menu to the user
def show_menu():
    print("\nProduction Media Management System")
    print("1. Add a new series with initial cast")
    print("2. Add a new employee")
    print("3. Assign an employee to a series")
    print("4. Add an employee grievance")
    print("5. View all grievances")
    print("6. Schedule or update a series release")
    print("7. Show series summary")
    print("8. Find employees by department")
    print("9. Update a series budget")
    print("10. Add crew member to a series")
    print("11. View full cast and crew of a series")
    print("12. Search series by genre")
    print("13. View all series by production firm")
    print("0. Exit")

# Main function to drive the menu
def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            add_series_with_cast()

        elif choice == '2':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            middle_name = input("Enter middle name: ")
            dob = input("Enter date of birth (yyyy-mm-dd): ")
            department_id = int(input("Enter department ID: "))
            series_id = input("Enter series ID (optional, leave blank if not assigned): ")
            series_id = int(series_id) if series_id else None
            add_employee(first_name, last_name, middle_name, dob, department_id, series_id)

        elif choice == '3':
            emp_id = int(input("Enter employee ID: "))
            series_id = int(input("Enter series ID to assign: "))
            assign_employee_to_series(emp_id, series_id)

        elif choice == '4':
            emp_id = int(input("Enter employee ID: "))
            grievance_text = input("Enter grievance text: ")
            add_grievance(emp_id, grievance_text)

        elif choice == '5':
            view_grievances()

        elif choice == '6':
            update_release_status()

        elif choice == '7':
            series_summary()

        elif choice == '8':
            department_id = int(input("Enter department ID: "))
            find_employees_by_department(department_id)

        elif choice == '9':
            series_id = int(input("Enter series ID: "))
            new_budget = float(input("Enter new budget: "))
            update_series_budget(series_id, new_budget)

        elif choice == '10':
            add_crew_member()

        elif choice == '11':
            view_series_cast_crew()

        elif choice == '12':
            search_series_by_genre()

        elif choice == '13':
            view_series_by_production_firm()

        elif choice == '0':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the main menu
if __name__ == "__main__":
    main() 

   
