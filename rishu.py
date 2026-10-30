import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    try:
        df = pd.read_csv("Attendance.csv")
    except FileNotFoundError:
        print("No valid data to analyse.")
        return None

    required_columns = [
        "Name", "Subject", "Classes_Held", "Classes_Attended"
    ]

    if not all(col in df.columns for col in required_columns):
        print("Invalid CSV format. Required columns are missing.")
        return None

    valid_rows = []

    for index, row in df.iterrows():
        try:
            held = int(row["Classes_Held"])
            attended = int(row["Classes_Attended"])

            if (
                pd.isna(row["Name"])
                or pd.isna(row["Subject"])
                or held <= 0
                or attended < 0
                or attended > held
            ):
                raise ValueError

            valid_rows.append({
                "Name": row["Name"],
                "Subject": row["Subject"],
                "Classes_Held": held,
                "Classes_Attended": attended
            })

        except (ValueError, TypeError, OverflowError):
            print(
                f"Row {index + 1} invalid: attended "
                f"({row['Classes_Attended']}) cannot exceed "
                f"held ({row['Classes_Held']}). Row skipped."
            )

    if not valid_rows:
        print("No valid data to analyse.")
        return None

    df = pd.DataFrame(valid_rows)

    df["Percentage"] = (
        df["Classes_Attended"] / df["Classes_Held"]
    ) * 100

    return df


def show_percentage(df):
    for _, row in df.iterrows():
        print(f"{row['Name']}: {row['Percentage']:.2f}%")


def show_shortage(df):
    below_75 = df[df["Percentage"] < 75]

    if below_75.empty:
        print("No student below 75%.")

        for _, row in df.iterrows():
            if row["Percentage"] >= 75:
                print(
                    f"{row['Name']} ({row['Percentage']:.2f}%) "
                    "is eligible."
                )
    else:
        print("Students below 75% attendance:")

        for _, row in below_75.iterrows():
            print(f"{row['Name']}: {row['Percentage']:.2f}%")


def subject_average(df):
    averages = df.groupby("Subject")["Percentage"].mean()

    for subject, average in averages.items():
        print(f"{subject}: {average:.2f}%")

    averages.plot(kind="bar")
    plt.title("Subject-wise Average Attendance")
    plt.xlabel("Subject")
    plt.ylabel("Average Attendance (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()


def show_charts(df):
    student_average = df.groupby("Name")["Percentage"].mean()

    student_average.plot(kind="bar")
    plt.title("Student Attendance")
    plt.xlabel("Student")
    plt.ylabel("Attendance (%)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

    eligible = (df["Percentage"] >= 75).sum()
    below = (df["Percentage"] < 75).sum()

    plt.pie(
        [eligible, below],
        labels=["Eligible", "Below 75%"],
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Attendance Eligibility")
    plt.show()


def main():
    df = load_data()

    if df is None:
        return

    print("\nCollege Attendance Analyzer")
    print("1. Show attendance percentages")
    print("2. Show students below 75%")
    print("3. Subject-wise average")
    print("4. Display bar and pie charts")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid menu choice.")
        return

    if choice == 1:
        show_percentage(df)
    elif choice == 2:
        show_shortage(df)
    elif choice == 3:
        subject_average(df)
    elif choice == 4:
        show_charts(df)
    else:
        print("Invalid menu choice.")


if __name__ == "__main__":
    main()