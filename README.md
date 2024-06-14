# Приложение для знакомств

Программа-бот для знакомств, осуществляющая поиск на основе взаимодействия с базами данных социальной сети VK.
Бот предлагает различных людей для знакомств в социальной сети VK в виде диалога с пользователем.

## Функции 

Используя  полученные данные от пользователя VK, бот ищет подходящих людей под условия поиска.

#### Реализованные критерии поиска:

* возраст
* пол
* город
* семейное положение

#### Результат поиска:

* Топ-3 фотографии каждого человека, подошедшего под запрос пользователя, а также именем, фамилией и ссылкой на страницу VK (популярность определяется количеством лайков и комментариев).
```
- имя и фамилия,
- ссылка на профиль,
- три фотографии в виде attachment(https://dev.vk.com/method/messages.send).
```
* Результат программы записывается в БД.
* Люди не повторяются при повторном поиске.
* Есть возможность добавить пользователя в черный список.
* Есть возможность добавить пользователя в избранное.
* Есть возможность вывести список всех избранных людей.
