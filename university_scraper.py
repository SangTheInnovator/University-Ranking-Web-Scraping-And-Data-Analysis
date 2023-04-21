import requests
import csv
import sys
from bs4 import BeautifulSoup as Soup
from itertools import islice


def scraping_data():
    url = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3740566_indicators.txt?1637817445" \
          "?v=1637823042256 "

    response = requests.get(url)
    response.raise_for_status()

    def generate_csv(entry):
        rank = entry["overall_rank"]
        name = Soup(entry["uni"], "html.parser").select_one(".uni-link").get_text(strip=True)
        region = entry["region"]
        location = entry["location"]
        city = entry["city"]
        overall_score = Soup(entry["overall"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)
        international_students_ratio = Soup(entry["ind_14"], "html.parser").select_one(".td-wrap-in").get_text(
            strip=True)
        international_faculty_ratio = Soup(entry["ind_18"], "html.parser").select_one(".td-wrap-in").get_text(
            strip=True)
        faculty_student_ratio = Soup(entry["ind_36"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)
        academic_reputation = Soup(entry["ind_76"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)
        citations_per_faculty = Soup(entry["ind_73"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)
        employer_reputation = Soup(entry["ind_77"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)

        record = [rank, name, region, location, city, overall_score, international_students_ratio,
                  international_faculty_ratio, faculty_student_ratio, academic_reputation, citations_per_faculty,
                  employer_reputation]

        return record

    yield from map(generate_csv, response.json()["data"])


def main():
    with open('university_ranking.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Rank', 'Name', 'Region', 'Location', 'City', 'Overall Score',
                         'International Students Ratio', 'International Faculty Ratio', 'Faculty Student Ratio',
                         'Academic Reputation', 'Citations Per Faculty', 'Employer Reputation'])
        for entry in islice(scraping_data(), 200):
            writer.writerow(entry)


if __name__ == "__main__":
    sys.exit(main())
