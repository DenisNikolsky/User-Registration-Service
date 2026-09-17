from urllib.error import HTTPError

from limits import UserRegistration, UserResponse
from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from db import find_user, create_new_user, show_all_persons
from typing import List
from cache import delete_user_from_cache
from asyncio import sleep
from load_service import generate_load

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

    @app.get("/users/all_users", response_model=List[UserResponse])
    async def users_me():
        return await show_all_persons()

    @app.post("/users/test_add_users/")
    async def add_user_test(background_tasks: BackgroundTasks, q: int = 100):
        background_tasks.add_task(generate_load, q)
        return {"Status": "Load started"}

    @app.get("/users/{user_name}", response_model=UserResponse)
    async def user_echo(user_name: str):
         return await find_user(user_name)

    @app.get("/users/{user_name}/cache")
    async def clear_user_cache(user_name: str):
        await delete_user_from_cache(user_name)
        return {"message": f"Cache for {user_name} is cleared"}

    @app.get("/test/error")
    async def raise_error_test():
        raise HTTPException(status_code=500, detail="Add error message")

    @app.get("/test/delay")
    async def delay_test():
        await sleep(3)
        return {"message": "Delay test",
                "Status": "Done"}

    # POST-маршрут обрабатывает данные из формы
    @app.post("/users/")
    async def register_user(
            name: str = Form(...),
            age: int = Form(...),
            password: str = Form(...)
    ):
        user = UserRegistration(name=name, age=age, password=password)
        return await create_new_user(user)


