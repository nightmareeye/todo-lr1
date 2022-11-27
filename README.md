# fastapi-todo-lr1
## Режим работы пользователя

```bash 
docker build -t todo_lr1 .
docker run -rm -p 80:80 todo_lr1
```

## Запуск генерации
### Генерация по умолчанию (20 записей)
```bash
sudo docker run --network=host todo_lr1 python3 scripts/generate.py 
```
### Генерация с параметром (пример, 50 записе)
```bash
sudo docker run --network=host todo_lr1 python3 scripts/generate.py --number <num>

sudo docker run --network=host todo_lr1 python3 scripts/generate.py --number 50
```

## С сохранением базы данных
```bash
sudo docker run -rm -p 80:80 -v ${PWD}:/data todo_lr1
```

## Режим работы разработчика

```bash 
sudo docker run --rm -v ${PWD}:/app -v ${PWD}:/data -p 80:80 todo_lr1
```

