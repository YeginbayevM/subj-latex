import os
import sys

# Путь к виртуальному окружению
venv_path = "/home/tyleks/subj-latex/template/myenv"  # Замените на ваш путь

# Активация виртуального окружения
if not os.path.exists(venv_path):
    print(f"Виртуальное окружение не найдено: {venv_path}")
    sys.exit(1)

activate_script = os.path.join(venv_path, "bin", "activate_this.py")
with open(activate_script) as f:
    exec(f.read(), {"__file__": activate_script})

# Теперь можно импортировать psycopg2
import psycopg2

# Параметры подключения к базе данных
db_params = {
    'dbname': 'course_gen',
    'user': 'tyleks',
    'host': 'localhost',
    'port': 5432
}

# Шаблон для генерации .tex файла
tex_template = r"""
\documentclass[a4paper,12pt]{article}

% 🔹 Базовые настройки
\usepackage[utf8]{inputenc}
\usepackage[T2A]{fontenc}
\usepackage[russian]{babel}
\usepackage{geometry}
\geometry{top=1.5cm, bottom=1.5cm, left=1.5cm, right=2cm}
\usepackage{enumitem}
% 🔹 Цвет фона и текста
\usepackage{xcolor}
\usepackage{pagecolor}
\definecolor{lightbeige}{rgb}{0.99, 0.98, 0.97} % Более светлый фон, ближе к белому
\definecolor{darkgreen}{rgb}{0, 0.4, 0.2} % Новый цвет для заголовков
\definecolor{darkblue}{rgb}{0,0.2,0.6}
\pagecolor{lightbeige} % Используем светло-бежевый фон
\color{black}
\usepackage{float}
% 🔹 Улучшенное форматирование
\usepackage{titlesec}
\titleformat{\section}
{\fontsize{12}{15}\selectfont\bfseries\color{darkblue}}{\thesection}{1em}{} % Зеленые заголовки
\titlespacing*{\section}{0pt}{0.9em}{0.4em}  % Меньше расстояние между заголовком и текстом

% 🔹 Переопределение \maketitle
\renewcommand{\maketitle}{%
  \noindent{\Large\bfseries\color{darkblue}\CourseName\par} % Зеленый заголовок курса
}

% 🔹 Колонтитулы
\usepackage{transparent} % Для прозрачности
\usepackage{fancyhdr}
\newcommand{\ctfont}{\fontsize{10}{11}\selectfont} % Шрифт без засечек
\newcommand{\coloredtext}[2][0.5]{\transparent{#1}\textcolor{black}{#2}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\ctfont\textcolor{darkblue}{Описание дисциплины} — {\textcolor{darkblue}{\CourseName}}} % Обычный текст
\fancyfoot[L]{\ctfont\coloredtext{\FooterName}} % Зеленый текст в колонтитуле
\fancyfoot[R]{\ctfont\coloredtext{\CourseName}} % Зеленый текст в колонтитуле

\setlength{\headheight}{15.5pt}

\renewcommand{\footrulewidth}{0.5pt}  % Толщина линии в нижнем колонтитуле

% 🔹 Таблицы
\usepackage{longtable, array, booktabs, colortbl, tabularx, makecell, multirow, hhline}
\renewcommand{\arraystretch}{1.}

% 🔹 Красивые блоки
\usepackage{tcolorbox}
\tcbset{colback=white, colframe=darkblue, arc=3pt} % Зеленая рамка с тенью

% 🔹 Дополнительное форматирование
\usepackage{ragged2e} % Выравнивание текста
\usepackage{ulem} % Подчеркивание
\usepackage{setspace}
\setstretch{0.8}
\pagenumbering{gobble}

% 🔹 Переменные
\renewcommand{\textbullet}{$\cdot$}
{course_commands}

\begin{document}
\maketitle % Отображаем заголовок
\vspace{0.5em}
\begin{tcolorbox}
	\textbf{Код курса:} \CourseCode\\
	\textbf{Семестр:} \Semester\\
	\textbf{Кредитная стоимость:} \Credits
\end{tcolorbox}

\section*{Краткое содержание}
\CourseDescription

\section*{Цель}
\CourseGoal

\section*{Результаты обучения}
\LearningOutcomes

\section*{Пререквизиты}
\Prerequisites

\section*{Содержание курса}
% Файл table.tex
\begin{table}[H] % Используем [H] для фиксации таблицы
    \centering
    \renewcommand{\arraystretch}{1.1} % Уменьшаем межстрочный интервал
    \arrayrulecolor{darkblue} % Синие линии таблицы
    \rowcolors{2}{darkblue!10}{white} % Чередование цветов строк
    \fontsize{9}{11}\selectfont % Уменьшаем размер шрифта
    \begin{tabular}{|c|p{5.5cm}|c|c|c|}
        \hline
        \rowcolor{darkblue!20} 
        \textbf{№} & \textbf{Наименование тем} & \textbf{Лекции} & \textbf{Практики} & \textbf{СРО} \\
        \hline
        {course_topics}
        \hline
        \rowcolor{darkblue!20} 
        \textbf{Всего} & & \LectureCount & \PracticeCount & \SelfLearnCount \\
        \hline
    \end{tabular}
\end{table}

\section*{Литература}
\begin{tcolorbox}[colback=darkblue!10, colframe=darkblue, sharp corners=south, boxrule=0.5mm]
    \fontsize{10}{11}\selectfont\textbf{Основные книги:}  
    \begin{itemize}[label=\textbullet, itemsep=0.5em, left=1em]
        \item \footnotesize\LiteratureMainOne
    \end{itemize}
    \vspace{0.5em}
    \fontsize{10}{11}\selectfont\textbf{Дополнительные ресурсы:}  
    \begin{itemize}[label=\textbullet, itemsep=0.5em, left=1em]
        \item \footnotesize\LiteratureAdditionalOne
    \end{itemize}
\end{tcolorbox}

\section*{Координатор курса}
\CoordinatorName, \CoordinatorPosition

\section*{Использование компьютеров}
\ComputersUsage

\section*{Лабораторные работы}
\LaboratoryWork

\vspace{0.2em}
\end{document}
"""

def fetch_course_summary(cursor):
    cursor.execute("SELECT * FROM course_summary")
    return cursor.fetchall()

def fetch_course_topics(cursor, course_id):
    cursor.execute("SELECT * FROM course_topics WHERE course_id = %s ORDER BY topic_number", (course_id,))
    return cursor.fetchall()

def generate_tex_file(course_summary, topics):
    course_id = course_summary[0]
    course_commands = "\n".join(course_summary[1:16])  # Команды LaTeX из course_summary
    course_topics = "\n".join(
        f"{topic[2]} & {topic[3]} & {topic[4]} & {topic[5]} & {topic[6]} \\\\"
        for topic in topics
    )
    tex_content = tex_template.format(
        course_commands=course_commands,
        course_topics=course_topics
    )
    with open(f"generated_course_{course_id}.tex", "w", encoding="utf-8") as f:
        f.write(tex_content)

def main():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    courses = fetch_course_summary(cursor)
    for course in courses:
        topics = fetch_course_topics(cursor, course[0])
        generate_tex_file(course, topics)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()