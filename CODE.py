from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


def connect_to_database():
    return sqlite3.connect("MPT1.db")


def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY,
    Surname TEXT NOT NULL,
    email TEXT NULL,
    telephone TEXT NULL
    )
    ''')
    connection.commit()
    connection.close()


def insert_student(surname, email, telephone):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Students (Surname, email, telephone) VALUES (?, ?, ?)',(surname, email, telephone))
    connection.commit()
    connection.close()


def select_all_students():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()

    connection.close()
    return students


def select_student_by_surname(surname):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT Surname, email, telephone FROM Students WHERE Surname = ?', (surname,))
    results = cursor.fetchall()

    connection.close()
    return results


def update_email_by_surname(surname, new_email):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Students SET email = ? WHERE Surname = ?', (new_email, surname))
    connection.commit()
    connection.close()


def delete_student_by_surname(surname):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Students WHERE Surname = ?", (surname,))
    connection.commit()
    connection.close()


def main():
    create_table()

    while True:
        print('Выберите действие')
        print('1 - Добавить данные в бд')
        print('2 - Просмотреть всю таблицу')
        print('3 - Найти студента по фамилии')
        print('4 - Изменить почту по фамилии')
        print('5 - Удалить данные из бд')
        print('0 - Выйти')

        choise = int(input('Введите номер действия: '))

        match choise:
            case 1:
                surname = input('Укажите фамилию студента')
                email = input('Укажите почту студента')
                telephone = input('Укажите телефон студента')
                insert_student(surname, email, telephone)
                print('Данные успешно добавлены в бд')
            case 2:
                print('Таблица студенты: ')
                students = select_all_students()
                for student in students:
                    print(student)
            case 3:
                surname = input('Укажите данные для поиска: ')
                results = select_student_by_surname(surname)
                for row in results:
                    print(row)
            case 4:
                surname = input('Введите фамилию для изменения почты: ')
                new_email = input('Укажите новый почтовый адрес')
                update_email_by_surname(surname, new_email)
                print('Почта обновлена')
            case 5:
                surname = input('Укажите фамилию для удаления: ')
                delete_student_by_surname(surname)
                print('Данные удалены')
            case 0:
                print('Выход...')
                break



class StudentCreate(BaseModel):
    Surname: str
    email: str = None
    telephone: str = None


@app.post("/students/", response_model=StudentCreate)
async def create_student(student: StudentCreate):
    insert_student(student.Surname, student.email, student.telephone)
    return student


@app.get("/students/")
async def read_students():
    students = select_all_students()
    return {"Студенты": students}


@app.get("/students/{surname}")
async def read_student_by_surname(surname: str):
    results = select_student_by_surname(surname)
    return {"Студенты": results}


@app.put("/students/{surname}")
async def update_student_email(surname: str, new_email: str):
    update_email_by_surname(surname, new_email)
    return {"message": "Почта обновлена"}


@app.delete("/students/{surname}")
async def delete_student(surname: str):
    delete_student_by_surname(surname)


if __name__ == '__main__':
    main()
