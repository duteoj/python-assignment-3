import os
import csv
import sys
import json

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print()
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found.")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")

class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print()
        print("Loading data...")
        try:
            with open(self.filename, mode='r', encoding = 'utf-8') as f:
                reader = csv.DictReader(f)
                self.students = list(reader)
                print(f"Data loaded successfully: {len(self.students)} students")
                return self.students
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []

    def preview_data(self, n=5):
        if not self.students: return
        print()
        print(f"First {n} rows:")
        print("-" * 30)
        for row in self.students[:n]:
            sid = row['student_id']
            age = row['age']
            gender = row['gender']
            country = row['country']
            gpa = row['GPA']
            print(f"{sid} | {age} | {gender} | {country} | GPA: {gpa}")
        print("-" * 30)

class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        try:

            top_scorers = list(filter(lambda s: float(s['final_exam_score']) > 95, self.students))
            
            gpa_values = list(map(lambda s: float(s['GPA']), self.students))
            
            good_assignments = list(filter(lambda s: float(s['assignment_score']) > 90, self.students))
            
            print("\n" + "-" * 30)
            print("Lambda / Map / Filter")
            print("-" * 30)
            print(f"final_exam_score > 95 : {len(top_scorers)}")
            print(f"GPA values (first 5) : {gpa_values[:5]}")
            print(f"assignment_score > 90 : {len(good_assignments)}")
            print("-" * 30)
            
            sorted_list = sorted(
                self.students, 
                key=lambda x: float(x['final_exam_score']), 
                reverse=True
            )[:10]
            
            top_10_json = []
            for i, s in enumerate(sorted_list):
                top_10_json.append({
                    "rank": i + 1,
                    "student_id": s['student_id'],
                    "country": s['country'],
                    "major": s['major'],
                    "final_exam_score": float(s['final_exam_score']),
                    "GPA": float(s['GPA'])
                })

            self.result = {
                "analysis": "Top 10 Students by Exam Score",
                "total_students": len(self.students),
                "top_10": top_10_json
            }
            return self.result
        except Exception as e:
            print(f"Analysis error: {e}")
            return {}

    def print_results(self):
        if not self.result: return
        print("-" * 30)
        print(self.result["analysis"])
        print("-" * 30)
        for s in self.result["top_10"]:
            print(f"{s['rank']}. {s['student_id']} | {s['country']} | {s['major']} | Score: {s['final_exam_score']} | GPA: {s['GPA']}")
        print("-" * 30)

class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, mode = 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"Result saved to {self.output_path}")
        except Exception as e:
            print(f"Error saving JSON: {e}")

def main():
    input_filename = 'global_university_students_performance_habits_10000.csv'
    output_filename = 'output/result.json'

    filename = FileManager(input_filename)
    if not filename.check_file():
        print('Stopping program.')
        sys.exit()
    filename.create_output_folder()

    dl = DataLoader(input_filename)
    dl.load()
    dl.preview_data()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result, output_filename)
    saver.save_json()

if __name__ == "__main__":
    main()
