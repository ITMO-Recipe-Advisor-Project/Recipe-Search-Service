# Recipe Search Service

## Описание

**Recipe Search** - это сервис, который предоставляет API для поиска рецептов по входной строке, содержащей список ингредиентов.

Сервис использует [Modified RecipeNLG Dataset](https://github.com/ITMO-Recipe-Advisor-Project/Recipes-Dataset) для индексации эмбеддингов рецептов с помощью FAISS и их последующего поиска в датасете.

### Преобразование входных данных в эмбеддинги
Для преобразования входящих данных в эмбеддинги доступны две опции:
1. **Использование Runpod API**:
   - Требуется указать API-ключ и endpoint вашего serverless проекта в Runpod.
2. **Локальный сервис**:
   - Поднимается модель [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) и API для работы с моделью.
   - Используется [образ Docker](https://hub.docker.com/layers/semitechnologies/transformers-inference/sentence-transformers-all-mpnet-base-v2-1.9.7/images/sha256-e9b9f418e64ac8f810a57c3c611c044dfab51a4215fb6908d9b7447bb102f20f).

## Установка и запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Создайте файл `env/.env` со следующими переменными:
   ```env
   RUNPOD_API_KEY=<ключ от вашего Runpod аккаунта, если для расчета эмбеддингов выбран этот способ>
   RUNPOD_ENDPOINT=<endpoint конкретного serverless проекта в Runpod, если для расчета эмбеддингов выбран этот способ>
   DATASET=<локальный путь до датасета>
   LOWER_THRESHOLD=<нижняя граница близости для ингредиентов и рецепта>
   K_NEIGHBORS=<количество соседей при поиске по индексу>
   ```

3. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

4. (Опционально) Используйте Docker Compose для запуска сервиса.

## Примеры запросов к API

### Пример запроса:
```bash
curl -X POST http://localhost:8000/recipes/search/ \  \
-H "Content-Type: application/json" \
-d '{"query": "Show me some recipes with berries and cream"}'
```

### Пример ответа:
```json
[
  {
    "title": "Chilled Strawberry Soup",
    "ingredients": [
      "2 cups frozen strawberries",
      "2 cups milk",
      "1 cup heavy cream",
      "1/2 cup sour cream",
      "2 tablespoons white sugar, or to taste"
    ],
    "link": "https://www.allrecipes.com/recipe/26393/chilled-strawberry-soup/"
  },
  {
    "title": "Blueberry Fruit Smoothie",
    "ingredients": [
      "1 cup reduced-fat vanilla ice cream",
      "1 cup fresh or frozen blueberries",
      "1/2 cup chopped peeled fresh peaches or frozen unsweetened sliced peaches",
      "1/2 cup pineapple juice",
      "1/4 cup vanilla yogurt"
    ],
    "link": "https://www.tasteofhome.com/recipes/blueberry-fruit-smoothie/"
  }
]
```
