# Yandex Disk Uploader

### Данные скрипты выполняют следующие задачи:
### encrypt.py:
+ Обходит заданную папку и добавляет произвольную цифру
к расширению файлов используя мультипоточность;
+ Добавляет данную папку в zip архив;
+ Меняет расширение архива на `.kek_zip`
+ Загружает полученный архив на Яндекс Диск.

**Для своей работы скрипт потребует:**
+ Путь к целевой директории. Может быть указан абсолютный 
`/home/user/Projects/Test/test/subdirectory`
или относительный (директории со скриптом) `test`.
+ Логин от сервисов Яндекса `your_email@yandex.ru`
+ Пароль приложения для доступа к Яндекс Диску по протоколу WebDAV. 
Инфомрацию о паролях приложений можно получить здесь: 
[https://yandex.ru/support/id/authorization/app-passwords.html](https://yandex.ru/support/id/authorization/app-passwords.html)

### decrypt.py:
+ Переименовывает и разархивирует предоствленный архив `.kek_zip`, 
созданный с помощью `encrypt.py`;
+ Рекурсивно обходит разархивированную папку и удаляет ранее 
добавленную в `encrypt.py` цифру.

**Для своей работы скрипт потребует:**
+ Пусть к файлу с архивом `.kek_zip`. Может быть указан абсолютный 
`/home/user/Projects/Test/backup_2022-10-10.kek_zip`
или относительный (директории со скриптом) `backup_2022-10-10.kek_zip`.

### Sripts implement the following:
### encrypt.py:
+ Walking through the `target_directory` and adding 
a random digit to the file extension (using multithreading).
+ Zipping 'target_directory' with modified files.
+ Changing the archive extension to `.kek_zip`.
+ Uploading the archive to Yandex Disk.

**The script requires:** 
+ Path to target folder. It can be specified either in an 
absolute (UNIX-style) `/home/user/Projects/Test/test/subdirectory`
or a relative (from the script directory) `test` way.
+ Login to Yandex services `your_email@yandex.ru`
+ The password for Yandex Disk **for applications**.
How to set it: 
[https://yandex.ru/support/id/authorization/app-passwords.html](https://yandex.ru/support/id/authorization/app-passwords.html)

### decrypt.py:
+ Renaming the provided zip archive with `kek_zip` extension
created by `encrypt.py`.
+ Unzipping it to the cwd.
+ Normalizing the extension of the files in unzipped folder (removing the random number from extension
    added in `encrypt.py`)

**The script requires:** 
+ The path to `.kek_zip` archive. It can be specified either in
an absolute (UNIX-style) `/home/user/Projects/Test/backup_2022-10-10.kek_zip`
or a relative (from the script directory) `backup_2022-10-10.kek_zip` way.