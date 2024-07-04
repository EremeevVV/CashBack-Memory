Краткое описание микросервиса CashBack-Memory: Memorize all available cahback.


## Начало работы

Чтобы настроить среду разработки, выполните следующие действия:

1. Клонируйте этот репозиторий на свою локальную машину:
   ```bash
   git clone https://gitlab.adm.ggr.gazprom.ru/EremeevVV/cashback_memory.git
   cd cashback_memory
   ```
2. Инциализируйте среду
   ```bash 
   poetry env use python3.11
   ```
3. Настройте в Pycharm интерпретатор: `alt+ctrl+s`, `Project: cashback_memory`, `Python interpreter`,
`Add Interpreter`, `Add local Interpreter`, `poetry environment`, `existing interpreter`, поле напротив должно быть заполнено, `ok`
4. Установите разработческие зависимости проекта
   ```bash 
   poetry install 
   ```
5. Включите систему контроля версий  File, VCS, Enable Version control integration, Git.
6. Включите автоматизацию проверки кода при commit.
   ```bash 
   pre-commit install
   ```
7. Настройте переменную, связанную с локальным запуском контейнера RabbitMQ, 
в Pycharm Run/Debug configuration для скрипта `main.py` впишите в поле `Environment Variables` `PYTHONUNBUFFERED=1;BROKER__HOSTNAME=localhost`.
Обратите внимание, чтобы в строке не было никаких лишних пробелов.
8. Настройте для всех запускаемых тестов рабочую папку: в Pycharm Run/Debug configuration `Edit configuration templates...`
`Python tests`, `pytest` в поле `working directory` выберите путь до корневой папки проекта

## Разработка

Код приложения находится в каталоге `cashback_memory`. В этом каталоге можно добавлять новые возможности или исправлять ошибки. Однако помните, что изменения кода должны сопровождаться соответствующими обновлениями тестов, расположенных в каталоге `tests/`.


## Перед запуском приложения
Если эти пункты выполнялись в другом проекте из группы, то их выполнять не надо.
1. Создайте нового пользователя document_indexer
```bash
useradd -m EremeevVV/
```
2. Активируйте пользователя, задав ему пароль
```bash
passwd EremeevVV/
```

## Запуск тестов

После обновления тестов их можно запустить с помощью [`pytest`](https://pytest.org/):

   ```bash 
  ./scripts/testsing.sh
   ```

## Локальный запуск приложения

Чтобы запустить приложение локально, выполните следующие действия:

1. Запустите приложение  следующей командой:

   ```bash 
   poetry run python3 main.py
   ```

2. Чтобы остановить приложение нажмите `Ctrl+C`.


## Сборка и тестирование образа Docker локально


Если вы хотите собрать и протестировать образ [`Docker`](https://www.docker.com/) локально, выполните следующие действия:


1. Запустите предоставленный скрипт для локальной сборки образа [`Docker`](https://www.docker.com/). Используйте следующую команду:


   ```bash 
   ./scripts/docker_build.sh
   ```


   Этот скрипт построит локально образ [`Docker`](https://www.docker.com/) с тем же именем, что и образ, построенный в `CI`.

2. Можно запустить локальный контейнер [`Docker`](https://www.docker.com/) с помощью следующей команды:

   ```bash 
      ./scripts/docker_run.sh 
   ```

3. Чтобы остановить локальный контейнер [`Docker`](https://www.docker.com/) выполните команду
   ```bash 
    ./scripts/docker_stop.sh 
   ```
 
## Линтинг кода

После внесения изменений в код необходимо убедиться в том, что он соответствует стандартам кодирования. Мы предоставляем скрипт, который поможет вам с форматированием и линтингом кода. Запустите следующий скрипт для автоматического исправления проблем с линтингом:

   ```bash 
   ./scripts/lint.sh
   ```

## Статический анализ

Инструменты статического анализа [`mypy`](https://mypy.readthedocs.io/en/stable/) и [`bandit`](https://bandit.readthedocs.io/en/latest/) помогут выявить потенциальные проблемы в коде. Для запуска статического анализа используйте следующий скрипт:

   ```bash 
   ./scripts/static-analysis.sh
   ```

Если обнаружены ошибки статического анализа, устраните их в коде и повторите запуск скрипта до его успешного прохождения.

## Использование системы контроля версий

После успешного выполнения всех описанных выше шагов вы можете вносить свои изменения:

1. Добавьте и зафиксируйте свои изменения:

   ```bash 
   git add .
   git commit -m "Your commit message"
   ```
Перед применением commit срабатывает pre-commit, где выполняются линтеры, статические анализаторы и тесты. Если хоть один этап обвалится commit не произойдет.
2. Отправьте изменения на GitLab:

   ```bash 
   git push origin your-branch
   ```

3. Создайте запрос на слияние на GitLab.

## Непрерывная интеграция (CI)

Данный репозиторий оснащен GitLab CI/CD, который автоматизируют статический анализ, линтеры и pytest в конвейере CI. Даже если вы забудете выполнить какой-либо из необходимых шагов, CI выявит все проблемы до слияния изменений.

В этом репозитории есть три рабочих процесса, каждый из которых запускается при размещении кода:

1. **Настройка тестовой среды**: Этот рабочий процесс называется "Venv". Настраивается среда и устанавливаются все библиотеки.

1. **Тесты**: Этот рабочий процесс называется "Tests" и состоит из двух заданий. Первое задание запускает инструменты статического анализа [`mypy`](https://mypy.readthedocs.io/en/stable/) и [`bandit`](https://bandit.readthedocs.io/en/latest/) для выявления потенциальных проблем в кодовой базе. Второе задание запускает тесты с помощью [`pytest`](https://pytest.org/) для проверки работоспособности приложения. Оба задания выполняются одновременно для ускорения процесса `CI`.
 
2. **Создание образа Docker**: Этот рабочий процесс называется "Build Docker Image" и имеет одно задание. В ходе выполнения этого задания на основе предоставленного Dockerfile создается образ [`Docker`](https://www.docker.com/). Затем созданный образ размещается в [**GitHub Container Registry**](https://ghcr.io), что делает его доступным для развертывания или других целей.
