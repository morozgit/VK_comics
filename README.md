# Постим комиксы в группе VK
Публикует комиксы на стене группы VK 
## Установка 

### Установка python
   
#### Для Linux 
```
sudo apt-get install python3
```
#### Для Mac OC
```
brew install python3
```
## Репозиторий
Клонируйте репозиторий в удобную папку.

## Настройки для VK
* [Получение](https://vk.com/dev/implicit_flow_user) ключа VK
* Создайте группу (создается через профиль VK)
* [Создайте приложение](https://vk.com/dev) VK во вкладке "Мои приложения"
* Получение App_ID (Manage -> Settings)
## Окружение
В терминале перейдите в папку с репозиторием.
### Переменные окружения 

#### Запись App_ID
```python
echo VK_App_ID=ваш ID > .env
```

#### Запись ключа VK
```python
echo VK_ACCESS_TOKEN=ваш ключ >> .env
```

#### Запись ключа ID группы
```python
echo VK_GROUP_ID=ваш ID группы >> .env
```

### Установка библиотек

```python 
pip3 install -r requirements.txt
```

## Запуск 


```python
python3 main.py
```
