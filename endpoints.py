from limits import UserRegistration, UserResponse
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from db import find_user, create_new_user, show_all_persons
from typing import List
from cache import delete_user_from_cache

def endpoints_register(app: FastAPI):
    @app.get("/")
    async def main_root():
        return {"message": "Hello World"}

    @app.get("/users/", response_class=HTMLResponse)
    async def show_registration_form():
        html_content = """
        <html>
            <head><title>Регистрация</title></head>
            <body>
                <h2>Форма регистрации</h2>
                <form method="post" action="/users/">
                    <label>Имя: <input type="text" name="name" required></label><br>
                    <label>Возраст: <input type="number" name="age" required></label><br>
                    <label>Пароль: <input type="password" name="password" required></label><br>
                    <button type="submit">Отправить</button>
                </form>
            </body>
        </html>
        """
        return html_content

    # POST-маршрут обрабатывает данные из формы
    @app.post("/users/")
    async def register_user(
            name: str = Form(...),
            age: int = Form(...),
            password: str = Form(...)
    ):
        user = UserRegistration(name=name, age=age, password=password)
        return await create_new_user(user)

    @app.get("/users/all_users", response_model=List[UserResponse])
    async def users_me():
        return await show_all_persons()

    @app.get("/users/{user_name}", response_model=UserResponse)
    async def user_echo(user_name: str):
         return await find_user(user_name)

    @app.get("/users/{user_name}/cache")
    async def clear_user_cache(user_name: str):
        await delete_user_from_cache(user_name)
        return {"message": f"Cache for {user_name} is cleared"}
