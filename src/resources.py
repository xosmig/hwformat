HELP_MESSAGE = r"""
TODO:
Heeeeeelp!
"""

DEFAULT_HEADER = r"""
\documentclass[12pt,a4paper]{scrartcl}
\usepackage[utf8]{inputenc}
\usepackage[english,russian]{babel}
\usepackage{indentfirst}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{listings}


% Некоторые множества

\def\Q{\mathbb{Q}}
\def\Z{\mathbb{Z}}
\def\N{\mathbb{N}}
\def\R{\mathbb{R}}


% Бинарные операции над множествами

% xor
\def\xor{\text{ {\raisebox{-2pt}{\ensuremath{\Hat{}}}} }}
% объединение
\def\u{\cup}
% объединение
\def\i{\cap}


% Комбинаторика

% Биномиальный коэффициент : (из n  по k)
\def\set{\binom}
% ((из n по k))
\def\mset#1#2{\ensuremath{\left(\kern-.3em\left(\genfrac{}{}{0pt}{}{#1}{#2}\right)\kern-.3em\right)}}


% Опеации над несколькими множествами

% Сумма
\def\suml#1#2#3{\sum\limits_{{#1}={#2}}^{#3}}
\def\sumi#1#2{\suml{#1}{#2}{\inf}}
\def\sumin#1#2{\sum\limits_{{#1} \in {#2}}}

% Перемножение (знак П)
\def\mul{\prod}
\def\mull#1#2#3{\mul\limits_{{#1}={#2}}^{#3}}
\def\muli#1#2{\mull{#1}{#2}{\inf}}
\def\mulin#1#2{\mul\limits_{{#1} \in {#2}}}

% Объединение
\def\U{\bigcup}
\def\Ul#1#2#3{\U\limits_{{#1}={#2}}^{#3}}
\def\Ui#1#2{\Ul{#1}{#2}{\inf}}
\def\Uin#1#2{\U\limits_{{#1} \in {#2}}}

% Пересечение
\def\I{\bigcap}
\def\Il#1#2#3{\I\limits_{{#1}={#2}}^{#3}}
\def\Ii#1#2{\Il{#1}{#2}{\inf}}
\def\Iin#1#2{\I\limits_{{#1} \in {#2}}}


% Разделители

\def\ms{\medskip}
\def\bs{\bigskip}


% Греческий алфавит

\def\l{\lambda}
\def\e{\varepsilon}
\def\d{\delta}
\def\m{\mu}
\def\p{\phi}

\def\L{\Lambda}
\def\D{\Delta}
\def\M{\Mu}
\def\P{\Phi}


% Кванторы

\def\A{\forall}
\def\E{\exists\;}


% Что-то еще

\def\inf{\t{+}\infty}    % +inf
\def\O{\mathcal{O}}      %
\def\t{\text}
\def\bs{\textbackslash{}}

"""
