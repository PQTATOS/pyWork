## Практика 2.3.3
### 1)
```Python
def time_test_1(str):
    return f"{str[8:10]}.{str[5:7]}.{str[:4]}"
```
![image](https://user-images.githubusercontent.com/55985434/210114747-9e9c9983-ea68-43a7-8ac8-ff9dbba175c1.png)

### 2)
```Python
def time_test_2(str):
    date = str.split('-')
    return f'{date[0]}.{date[1]}.{date[2]}'
```
![image](https://user-images.githubusercontent.com/55985434/210114811-49c1bfb7-5689-4793-bb95-ae0a6ff29cde.png)

### 3)
```Python
def time_test_4(str):
    date = datetime.strptime(str, "%Y-%m-%dT%H:%M:%S+%f")
    return f"{date.year}.{date.month}.{date.day}"
```
![image](https://user-images.githubusercontent.com/55985434/210114870-84ebfee2-9280-4343-9319-24878b083e1c.png)

### 4)
```Python
def time_test_3(str):
    return datetime.strptime(str, "%Y-%m-%dT%H:%M:%S+%f").strftime("%Y.%m.%d")
```
![image](https://user-images.githubusercontent.com/55985434/210115015-1ed36af0-efa3-49a2-ba02-62a8d3fbcf6f.png)


## Практика 3.2.1
![image](https://user-images.githubusercontent.com/55985434/209869478-d282e815-dfe7-46f5-85d5-2581a3d42b1a.png)

## Практика 3.2.2
### Без многопроцессорной обработки
![Снимок экрана 2022-12-30 233111](https://user-images.githubusercontent.com/55985434/210101914-e09b650e-f27f-43f8-b44c-d509788dad17.png)
### Multiprocessing
![Снимок экрана 2022-12-30 232921](https://user-images.githubusercontent.com/55985434/210101907-022194e4-b8ad-4a04-b0f2-698c990884d4.png)

## Практика 3.2.3
### Concurrent futures
![image](https://user-images.githubusercontent.com/55985434/210115840-2d8c139c-d98b-4456-bcac-0417fa13fd9f.png)


## Практика 3.3.1
![image](https://user-images.githubusercontent.com/55985434/210151141-05cdb794-6578-4da5-a6b7-8896f37f6226.png)
![image](https://user-images.githubusercontent.com/55985434/210151429-cd364807-3796-4703-b2d9-4b391a82c6d9.png)
![image](https://user-images.githubusercontent.com/55985434/210151544-cb8d6f38-10f4-45a7-8528-5f4a3c2baf3a.png)


