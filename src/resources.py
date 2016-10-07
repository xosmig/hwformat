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

\def\Q{\mathbb{Q}}
\def\Z{\mathbb{Z}}
\def\N{\mathbb{N}}
\def\R{\mathbb{R}}

\def\inf{\t{+}\infty}    % +inf
\def\O{\mathcal{O}}      %
\def\xor{\text{ {\raisebox{-2pt}{\ensuremath{\Hat{}}}} }}

\def\set{\binom}
\def\mset#1#2{\ensuremath{\left(\kern-.3em\left(\genfrac{}{}{0pt}{}{#1}{#2}\right)\kern-.3em\right)}}

\def\bs{\textbackslash{}}

\def\suml#1#2#3{\sum\limits_{{#1}={#2}}^{#3}}
\def\sumi#1#2{\suml{#1}{#2}{\inf}}
\def\sumin#1#2{\sum\limits_{{#1} \in {#2}}}

\def\mul{\prod}
\def\mull#1#2#3{\mul\limits_{{#1}={#2}}^{#3}}
\def\muli#1#2{\mull{#1}{#2}{\inf}}
\def\mulin#1#2{\mul\limits_{{#1} \in {#2}}}

\def\u{\cup}
\def\U{\bigcup}
\def\Ul#1#2#3{\U\limits_{{#1}={#2}}^{#3}}
\def\Ui#1#2{\Ul{#1}{#2}{\inf}}
\def\Uin#1#2{\U\limits_{{#1} \in {#2}}}

\def\i{\cap}
\def\I{\bigcap}
\def\Il#1#2#3{\I\limits_{{#1}={#2}}^{#3}}
\def\Ii#1#2{\Il{#1}{#2}{\inf}}
\def\Iin#1#2{\I\limits_{{#1} \in {#2}}}

\def\ms{\medskip}
\def\bs{\bigskip}

\def\l{\lambda}
\def\e{\varepsilon}
\def\d{\delta}
\def\m{\mu}
\def\p{\phi}

\def\L{\Lambda}
\def\D{\Delta}
\def\M{\Mu}
\def\P{\Phi}

\def\A{\forall}
\def\E{\exists\;}
"""