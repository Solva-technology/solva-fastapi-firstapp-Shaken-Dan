from email.policy import default
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.params import Query, Path

from db import MOVIES

app = FastAPI(
    title = "Мини-каталог фильмов на FastAPI",
    description= "Показывает список фильмов по жанру или году выпуска"
)


genres = {item['genre'] for item in MOVIES}

MovieGenre = Enum(
    "MovieGenre",
    {g.upper().replace("-", "_"): g for g in genres},
    type=str
)


@app.get("/movies",
         tags=['Movies'],
         summary="Можно выбрать интересный вам фильм по жанру и году выпуска",
         response_description="Результат поиска по параметрам фильтрации"
         )
async def home(
        genre: MovieGenre | None = Query(None, description="Жанр фильма"),
        year: str | None = Query(None, description="Год выпуска фильма"),
        limit: int | None = Query(None, description="Ограничение количества выдачи", ge=1),
        sort: str | None = Query(None, description="Сортировка по году")
) -> list[dict]:
    """
    Возвращает фильм по параметрам:

    - **genre**: жанр фильма
    - **year**: год выпуска фильма
    """
    result = MOVIES

    if genre:
        result = [m for m in result if m["genre"] == genre.value]

    if year:
        result = [m for m in result if str(m["year"]) == str(year)]

    if sort is not None:
        result = sorted(result, key=lambda m: m["year"])

    if limit:
        result = result[:2]

    return result

@app.get("/movies/{movie_id}",
         tags=['Movie ID'],
         summary="Можно выбрать интересный вам фильм по ID фильма",
         response_description="Результат поиска по ID"
         )
async def get_by_id(
        movie_id: int = Path(..., description="Выдает фильм по ID")
):
    for movie in MOVIES:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(status_code=404, detail='Movie not found')
