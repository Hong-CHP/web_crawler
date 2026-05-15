import csv, os

def save_csv_content() :
	if not os.path.exists("data_csv"):
		os.mkdir("data_csv")
	# with open("data_csv/01.csv", "w", encoding="utf-8") as f:
	# 	f.write("name, age, sexe, hobby\n")
	# 	f.write("momo, 18, man, python\n")
	with open("data_csv/02.csv", "w", encoding="utf-8", newline="") as f:
		content_w = csv.DictWriter(f, fieldnames=["name", "age", "sexe", "hobby"])
		content_w.writeheader()
		content_w.writerow({"name" :"momo", "age": 18, "sexe": "man", "hobby": "python"})
	with open("data_csv/02.csv", "r", encoding="utf-8") as f:
		content_r = csv.DictReader(f)
		for r in content_r:
			print(f"{r}\n")