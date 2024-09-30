import csv
import sqlite3


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            car_number, fee_date = row

            delete_query = """
                        DELETE FROM table_fees
                        WHERE truck_number = ? AND timestamp = ?;
                        """
            cursor.execute(delete_query, (car_number, fee_date))
if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
